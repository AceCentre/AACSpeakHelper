"""
AACSpeakHelperServer.py - Windows Named Pipe Server for AACSpeakHelper

This server provides text-to-speech (TTS) and translation services through a Windows named pipe.
It runs as a system tray application and processes requests from client applications.

The server:
1. Creates a named pipe (\\\\.\\pipe\\AACSpeakHelper) to receive requests
2. Processes incoming JSON messages containing text to speak/translate
3. Performs translation if requested
4. Converts text to speech using the configured TTS engine
5. Optionally replaces clipboard content with translated text

Credentials:
- All API keys and credentials are read from the settings.cfg file
- No environment variables are required for normal operation
- The configuration file is typically located in the user's AppData folder

Usage:
- Run this script to start the server
- Use client.py to send requests to the server
- Configure settings using the GUI or CLI configuration tools

Note for developers:
- During development, credentials can be stored in .envrc
- These are used by test scripts, not by the server itself

Author: Ace Centre
"""

import configparser
import json
import logging
import os
import subprocess
import sys
import threading
import time
import warnings
import unicodedata

import pyperclip
import win32api
import win32event
import win32file
import win32pipe
from PySide6.QtCore import QThread, Signal, Slot, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QMessageBox
import deep_translator
from deep_translator import (
    ChatGptTranslator,
    DeeplTranslator,
    GoogleTranslator,
    LibreTranslator,
    LingueeTranslator,
    MicrosoftTranslator,
    MyMemoryTranslator,
    PapagoTranslator,
    PonsTranslator,
    QcriTranslator,
    YandexTranslator,
)

import tts_utils
import utils

BaiduTranslator = getattr(deep_translator, "BaiduTranslator", None)
if BaiduTranslator is None:
    # Some deep-translator versions expose the class under a different name
    BaiduTranslator = getattr(deep_translator, "Baidu", None)

warnings.filterwarnings("ignore")


def setup_logging():
    if getattr(sys, "frozen", False):
        # If the application is run as a bundle, use the AppData directory
        log_dir = os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Roaming",
            "Ace Centre",
            "AACSpeakHelper",
        )
    else:
        # If run from a Python environment, use the current directory
        log_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "app.log")

    logging.basicConfig(
        filename=log_file,
        filemode="a",
        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
        level=logging.DEBUG,
    )

    return log_file


logfile = setup_logging()


def log_debug_info():
    """Log comprehensive debug information for frozen vs development differences"""
    logging.info("=== AACSpeakHelper Server Debug Information ===")
    logging.info(f"Python executable: {sys.executable}")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Current working directory: {os.getcwd()}")
    logging.info(f"Script location: {__file__}")
    logging.info(f"Frozen executable: {getattr(sys, 'frozen', False)}")
    if hasattr(sys, "_MEIPASS"):
        logging.info(f"PyInstaller temp dir: {sys._MEIPASS}")
    logging.info(f"Python path: {sys.path}")

    # Log file system information
    current_dir = os.getcwd()
    try:
        files_in_dir = os.listdir(current_dir)
        logging.info(f"Files in current directory: {files_in_dir}")
    except Exception as e:
        logging.error(f"Error listing current directory: {e}")

    # Check for config files
    config_files = ["settings.cfg", "config.cfg", ".envrc"]
    for config_file in config_files:
        config_path = os.path.join(current_dir, config_file)
        if os.path.exists(config_path):
            try:
                size = os.path.getsize(config_path)
                logging.info(f"Found config file: {config_path} (size: {size} bytes)")
            except Exception as e:
                logging.error(f"Error checking config file {config_path}: {e}")
        else:
            logging.info(f"Config file not found: {config_path}")

    # Check environment variables
    important_env_vars = ["PATH", "PYTHONPATH", "APPDATA", "USERPROFILE"]
    for var in important_env_vars:
        value = os.environ.get(var, "Not set")
        logging.info(f"Environment {var}: {value}")

    logging.info("=== End Debug Information ===")


# Call debug logging immediately
log_debug_info()


def check_single_instance():
    """
    Check if another instance of AACSpeakHelper server is already running.
    Uses a named mutex to ensure only one instance can run at a time.

    Returns:
        bool: True if this is the only instance, False if another instance is already running
    """
    mutex_name = "Global\\AACSpeakHelperServerMutex"

    try:
        # Try to create a named mutex
        win32event.CreateMutex(None, True, mutex_name)

        if win32api.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            logging.warning(
                "Another instance of AACSpeakHelper server is already running!"
            )
            return False
        else:
            logging.info(
                "Single instance check passed - this is the only server instance"
            )
            return True

    except Exception as e:
        logging.error(f"Error checking single instance: {e}")
        # If we can't check, assume it's safe to continue
        return True


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        menu = QMenu(parent)
        self.config_path, self.audio_files_path = utils.get_paths(None)
        logging.info(f"Config path: {self.config_path}")
        logging.info(f"Audio files path: {self.audio_files_path}")

        openLogsAction = QAction("Open logs", self)
        menu.addAction(openLogsAction)
        openLogsAction.triggered.connect(self.open_logs)

        openCacheAction = QAction("Open Cache", self)
        menu.addAction(openCacheAction)
        openCacheAction.triggered.connect(self.open_cache)

        menu.addSeparator()

        self.lastRunAction = QAction("Last run info not available", self)
        self.lastRunAction.setEnabled(False)
        menu.addAction(self.lastRunAction)

        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)

        self.setContextMenu(menu)

    def exit(self):
        self.parent.pipe_thread.quit()
        os._exit(0)
        # QApplication.quit()

    def update_last_run_info(self, last_run_time, duration):
        self.lastRunAction.setText(
            f"Last run at {last_run_time} - took {duration} secs"
        )

    def open_logs(self):
        logging.info("Opening logs...")
        subprocess.Popen(["notepad", logfile])

    def open_cache(self):
        logging.info("Opening cache...")
        subprocess.Popen(["explorer", self.audio_files_path])
        # Implement cache opening logic here


class PipeServerThread(QThread):
    """
    Thread that handles the Windows named pipe communication.

    This thread:
    1. Creates a named pipe (\\\\.\\pipe\\AACSpeakHelper)
    2. Waits for client connections
    3. Reads data from clients
    4. Emits a signal with the received message
    5. Optionally returns voice list data to the client

    The pipe accepts JSON-formatted messages containing:
    - args: Command-line arguments from the client
    - config: Configuration settings
    - clipboard_text: Text to process

    Required Credentials (from settings.cfg):
    - For Azure TTS: key, location in [azureTTS] section
    - For Google TTS: creds in [googleTTS] section
    - For Microsoft Translator: microsoft_translator_secret_key in [translate] section
    - For Microsoft Translator: region in [translate] section
    """

    message_received = Signal(str)
    voices = None

    def run(self):
        pipe_name = r"\\.\pipe\AACSpeakHelper"
        while True:
            pipe = None
            try:
                # Create the named pipe
                pipe = win32pipe.CreateNamedPipe(
                    pipe_name,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE
                    | win32pipe.PIPE_READMODE_MESSAGE
                    | win32pipe.PIPE_WAIT,
                    win32pipe.PIPE_UNLIMITED_INSTANCES,
                    65536,
                    65536,
                    0,
                    None,
                )

                logging.info("Waiting for client connection...")
                # Wait for a client to connect
                win32pipe.ConnectNamedPipe(pipe, None)
                logging.info("Client connected.")

                # Read data from the client
                result, data = win32file.ReadFile(pipe, 64 * 1024)
                get_voices = False
                if result == 0:
                    # Decode and process the message
                    message = data.decode()
                    logging.info(f"PipeServerThread: Received data: {message[:50]}...")
                    logging.info(
                        f"PipeServerThread: Processing message in thread {threading.current_thread().name}"
                    )
                    # Emit signal to process the message in the main thread
                    self.message_received.emit(message)
                    try:
                        # Check if client is requesting voice list
                        parsed_message = json.loads(message)
                        get_voices = parsed_message.get("args", {}).get(
                            "listvoices", False
                        )
                    except Exception as e:
                        logging.error(f"Error parsing message: {e}")
                        get_voices = False
                logging.info("Processing complete. Ready for next connection.")
            except Exception as e:
                logging.error(f"Pipe server error: {e}", exc_info=True)
            finally:
                if pipe:
                    # If client requested voices and we have them, send them back
                    while get_voices:
                        if self.voices:
                            win32file.WriteFile(pipe, json.dumps(self.voices).encode())
                            self.voices = None
                            break
                    # Close the pipe handle
                    win32file.CloseHandle(pipe)
                logging.info("Pipe closed. Reopening for next connection.")


class CacheCleanerThread(QThread):
    def run(self):
        remove_stale_temp_files(utils.audio_files_path)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cache_timer = None
        self.cache_cleaner = None
        self.pipe_thread = None
        self.tray_icon = None
        self.icon = QIcon("assets/translate.ico")
        self.icon_loading = QIcon("assets/translate_loading.ico")
        self.init_ui()
        self.init_pipe_server()
        self.init_cache_cleaner()
        self.init_log_cleaner()
        self.tray_icon.setToolTip("Waiting for new client...")

    def init_ui(self):
        self.tray_icon = SystemTrayIcon(self.icon, self)
        self.tray_icon.setVisible(True)

    def init_pipe_server(self):
        self.pipe_thread = PipeServerThread()
        self.pipe_thread.message_received.connect(self.handle_message)
        self.pipe_thread.start()

    def init_cache_cleaner(self):
        self.cache_cleaner = CacheCleanerThread()
        self.cache_timer = QTimer(self)
        self.cache_timer.timeout.connect(lambda: self.cache_cleaner.start())
        self.cache_timer.start(24 * 60 * 60 * 1000)  # Run once a day

    def init_log_cleaner(self):
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.check_log_size)
        self.log_timer.start(3600000)  # Check every hour, adjust as needed

    def check_log_size(self):
        log_file = logfile
        size_limit_mb = 1  # Size limit in MB
        size_limit_bytes = size_limit_mb * 1024 * 1024  # Convert MB to bytes

        try:
            if (
                os.path.isfile(log_file)
                and os.path.getsize(log_file) > size_limit_bytes
            ):
                with open(log_file, "w"):  # Truncate the log file
                    logging.info("Log file exceeded size limit; log file truncated.")
        except Exception as e:
            logging.error(f"Error cleaning log file: {e}", exc_info=True)

    @Slot(str)
    def handle_message(self, message):
        """
        Process a message received from a client.

        This method:
        1. Parses the JSON message
        2. Extracts configuration and text data
        3. Initializes the TTS and translation engines
        4. Translates the text if requested
        5. Speaks the text using the configured TTS engine
        6. Optionally updates the clipboard with translated text

        Args:
            message (str): JSON-formatted message from the client
        """
        logging.info(
            f"MainWindow.handle_message: Starting to process message in thread {threading.current_thread().name}"
        )
        try:
            # Parse the JSON message
            data = json.loads(message)

            # Extract data from the received message
            args = data["args"]
            config_dict = data["config"]
            clipboard_text = data["clipboard_text"]

            # Create a ConfigParser object and update it with received config
            config = configparser.ConfigParser()
            for section, options in config_dict.items():
                config[section] = options

            # Log the Google credentials path (if available)
            if "googleTTS" in config and "creds" in config["googleTTS"]:
                logging.info(
                    f"Using Google credentials: {config['googleTTS']['creds']}"
                )

            # Get the config path from the received config
            config_path = config.get("App", "config_path", fallback=None)
            # Use utils.get_paths to get the paths
            # config_path, audio_files_path = utils.get_paths(config_path)
            # TODO: Disable config_path for now
            config_path, audio_files_path = utils.get_paths()

            if "App" not in config:
                config["App"] = {}
            config["App"]["config_path"] = config_path
            config["App"]["audio_files_path"] = audio_files_path
            # Initialize utils with the new config and args
            utils.init(config, args)

            # Initialize TTS
            tts_utils.init(utils)
            # Process the clipboard text
            if not tts_utils.ready:
                logging.info(
                    "Application is not ready. Please wait until current session is finished."
                )
                return
            self.tray_icon.setToolTip("Handling new message ...")
            self.tray_icon.setIcon(self.icon_loading)
            logging.info(f"Handling new message: {message[:50]}...")

            # Process text through the new modular pipeline
            try:
                from processing_pipeline import processing_pipeline

                text_to_process = processing_pipeline.process_text(
                    clipboard_text, config
                )
            except ImportError:
                # Fallback to old processing logic if pipeline not available
                logging.warning(
                    "Processing pipeline not available, using fallback logic"
                )
                text_to_process = clipboard_text

                # Step 1: Translation (if enabled)
                if config.getboolean("translate", "enabled", fallback=False):
                    translated_text = translate_clipboard(text_to_process, config)
                    if translated_text is not None:
                        text_to_process = translated_text

                # Step 2: Transliteration (if enabled)
                if config.getboolean("transliterate", "enabled", fallback=False):
                    transliterated_text = transliterate_clipboard(
                        text_to_process, config
                    )
                    if transliterated_text is not None:
                        text_to_process = transliterated_text

                # Perform TTS if enabled
                if config.getboolean("tts", "enabled", fallback=True):
                    tts_utils.speak(text_to_process, args["listvoices"])
                if tts_utils.voices:
                    self.pipe_thread.voices = tts_utils.voices

                # Replace clipboard if specified
                should_replace_clipboard = (
                    config.getboolean("translate", "enabled", fallback=False)
                    and config.getboolean(
                        "translate", "replace_clipboard", fallback=False
                    )
                ) or (
                    config.getboolean("transliterate", "enabled", fallback=False)
                    and config.getboolean(
                        "transliterate", "replace_clipboard", fallback=False
                    )
                )

                if should_replace_clipboard and text_to_process is not None:
                    pyperclip.copy(text_to_process)

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.tray_icon.update_last_run_info(current_time, "N/A")
            logging.info(f"Processed message at {current_time}")
            self.tray_icon.setIcon(self.icon)
            self.tray_icon.setToolTip("Waiting for new client...")
        except Exception as e:
            logging.error(f"Error handling message: {e}", exc_info=True)
        finally:
            logging.info("Message handling complete.")


def translate_clipboard(text, config):
    try:
        translator = config.get("translate", "provider").strip()
        normalized_provider = translator.lower().replace(" ", "")
        if normalized_provider in {"baidu", "baidutranslator"}:
            translator = "BaiduTranslator"

        # Get the appropriate secret key based on the translator
        key = None
        if translator == "MicrosoftTranslator":
            key = config.get(
                "translate", "microsoft_translator_secret_key", fallback=""
            )
        elif translator == "MyMemoryTranslator":
            key = config.get(
                "translate", "my_memory_translator_secret_key", fallback=""
            )
        elif translator == "DeeplTranslator":
            key = config.get("translate", "deep_l_translator_secret_key", fallback="")
        elif translator == "LibreTranslator":
            key = config.get("translate", "libre_translator_secret_key", fallback="")
        elif translator == "YandexTranslator":
            key = config.get("translate", "yandex_translator_secret_key", fallback="")
        elif translator == "QcriTranslator":
            key = config.get("translate", "qcri_translator_secret_key", fallback="")
        elif translator == "BaiduTranslator":
            key = config.get("translate", "baidu_translator_secret_key", fallback="")
        elif translator == "PapagoTranslator":
            key = config.get("translate", "papago_translator_secret_key", fallback="")
        # GoogleTranslator doesn't need a key

        email = (
            config.get("translate", "email")
            if translator == "MyMemoryTranslator"
            else None
        )
        region = (
            config.get("translate", "region")
            if translator == "MicrosoftTranslator"
            else None
        )
        pro = (
            config.getboolean("translate", "deepl_pro")
            if translator == "DeeplTranslator"
            else None
        )
        url = (
            config.get("translate", "url") if translator == "LibreTranslator" else None
        )
        client_id = (
            config.get("translate", "papago_translator_client_id")
            if translator == "PapagoTranslator"
            else None
        )
        appid = (
            config.get("translate", "baidutranslator_appid")
            if translator == "BaiduTranslator"
            else None
        )

        match translator:
            case "GoogleTranslator":
                translate_instance = GoogleTranslator(
                    source="auto", target=config.get("translate", "target_language")
                )
            case "PonsTranslator":
                translate_instance = PonsTranslator(
                    source="auto", target=config.get("translate", "target_language")
                )
            case "LingueeTranslator":
                translate_instance = LingueeTranslator(
                    source="auto", target=config.get("translate", "target_language")
                )
            case "MyMemoryTranslator":
                translate_instance = MyMemoryTranslator(
                    source=config.get("translate", "source_language"),
                    target=config.get("translate", "target_language"),
                    email=email,
                )
            case "YandexTranslator":
                translate_instance = YandexTranslator(
                    source=config.get("translate", "source_language"),
                    target=config.get("translate", "target_language"),
                    api_key=key,
                )
            case "MicrosoftTranslator":
                translate_instance = MicrosoftTranslator(
                    api_key=key,
                    source=config.get("translate", "source_language"),
                    target=config.get("translate", "target_language"),
                    region=region,
                )
            case "QcriTranslator":
                translate_instance = QcriTranslator(
                    source="auto",
                    target=config.get("translate", "target_language"),
                    api_key=key,
                )
            case "DeeplTranslator":
                translate_instance = DeeplTranslator(
                    source=config.get("translate", "source_language"),
                    target=config.get("translate", "target_language"),
                    api_key=key,
                    use_free_api=not pro,
                )
            case "LibreTranslator":
                translate_instance = LibreTranslator(
                    source=config.get("translate", "source_language"),
                    target=config.get("translate", "target_language"),
                    api_key=key,
                    custom_url=url,
                )
            case "PapagoTranslator":
                translate_instance = PapagoTranslator(
                    source="auto",
                    target=config.get("translate", "target_language"),
                    client_id=client_id,
                    secret_key=key,
                )
            case "ChatGptTranslator":
                translate_instance = ChatGptTranslator(
                    source="auto", target=config.get("translate", "target_language")
                )
            case "BaiduTranslator":
                if BaiduTranslator is None:
                    raise RuntimeError(
                        "Baidu translator is not available in the installed "
                        "deep-translator package. Install a version with "
                        "Baidu support or select another translation provider."
                    )
                translate_instance = BaiduTranslator(
                    source=config.get("translate", "source_language"),
                    target=config.get("translate", "target_language"),
                    appid=appid,
                    appkey=key,
                )
        # elif translator == "DeepLearningTranslator":
        #     translate_instance = BaiduTranslator(source=config.get('translate', 'startlang'),
        #                                          target=config.get('translate', 'endLang'),
        #                                          appid=appid,
        #                                          appkey=key)
        logging.info("Translation Provider is {}".format(translator))
        logging.info(f'Text [{config.get("translate", "source_language")}]: {text}')
        if config.get("translate", "target_language") in [
            "ckb" "ku",
            "kmr",
            "kmr-TR",
            "ckb-IQ",
        ]:
            text = normalize_text(text)
        translation = translate_instance.translate(text)
        logging.info(
            f'Translation [{config.get("translate", "target_language")}]: {translation}'
        )
        return translation
    except Exception as e:
        logging.error(f"Translation Error: {e}", exc_info=True)
        return None


def transliterate_clipboard(text, config):
    """
    Transliterate text using Azure Translator transliteration API.

    This function converts text from one script to another (e.g., Latin to Devanagari)
    while maintaining the same language, using the Azure transliteration service.

    Args:
        text (str): Text to transliterate
        config: Configuration object containing transliteration settings

    Returns:
        str or None: Transliterated text, or None if transliteration failed
    """
    try:
        # Import the transliteration module
        from azure_transliteration import transliterate_text

        # Use the transliteration function with config
        result = transliterate_text(text, config)

        if result is not None:
            logging.info(f"Transliteration successful: {text} -> {result}")
            return result
        else:
            logging.warning("Transliteration returned None, using original text")
            return None

    except ImportError as e:
        logging.error(f"Azure transliteration module not found: {e}")
        return None
    except Exception as e:
        logging.error(f"Transliteration Error: {e}", exc_info=True)
        return None


def normalize_text(text: str):
    normalizedText = unicodedata.normalize("NFC", text)
    logging.info("Normalized Text: {}".format(normalizedText))
    return normalizedText


def remove_stale_temp_files(directory_path, ignore_pattern=".db"):
    config = utils.config
    start = time.perf_counter()
    current_time = time.time()
    day = int(config.get("appCache", "threshold"))
    time_threshold = current_time - day * 24 * 60 * 60
    file_list = []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if (
                ignore_pattern
                and file.endswith(ignore_pattern)
                and file.endswith(".db-journal")
            ):
                continue
            try:
                file_modification_time = os.path.getmtime(file_path)
                if file_modification_time < time_threshold:
                    os.remove(file_path)
                    file_list.append(os.path.basename(file_path))
                    logging.info(f"Removed cache file: {file_path}")
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}", exc_info=True)

    stop = time.perf_counter() - start
    utils.clear_history(file_list)
    logging.info(f"Cache clearing took {stop:0.5f} seconds.")


def clearCache():
    temp_folder = os.getenv("TEMP")
    size_limit = 5 * 1024  # 5KB in bytes
    # Scan the directory
    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            if file.startswith("tmp"):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) < size_limit:
                    current_time = time.time()
                    day = 7
                    time_threshold = current_time - day * 24 * 60 * 60
                    file_modification_time = os.path.getmtime(file_path)
                    if file_modification_time < time_threshold:
                        os.remove(file_path)


if __name__ == "__main__":
    # Check if another instance is already running
    if not check_single_instance():
        logging.error(
            "Exiting: Another instance of AACSpeakHelper server is already running"
        )

        # Show a message box if we're not in frozen mode (development)
        if not getattr(sys, "frozen", False):
            try:
                app = QApplication(sys.argv)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("AACSpeakHelper Server")
                msg.setText(
                    "Another instance of AACSpeakHelper server is already running."
                )
                msg.setInformativeText(
                    "Please close the existing instance before starting a new one."
                )
                msg.exec()
            except Exception as e:
                logging.error(f"Error showing message box: {e}")

        sys.exit(1)

    clearCache()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
