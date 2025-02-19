# This Python file uses the following encoding: utf-8
import os
import sys
import json
import logging
import configparser
import pyperclip
from pathlib import Path
from threading import Thread
from PySide6.QtCore import Qt, QSize, QObject, Signal, QRunnable, QThreadPool, QFile, QIODevice, QTextStream, QEvent, QMetaObject, Slot, Q_ARG

# Add project root to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from PySide6.QtWidgets import (
    QWidget, QListWidgetItem, QMessageBox, QApplication,
    QPushButton, QLabel, QHBoxLayout, QListWidget,
    QDialogButtonBox, QFileDialog, QVBoxLayout
)
from PySide6.QtGui import QIcon, QMovie, QColor, QFont
from ui_form import Ui_Widget  # Import from current directory
from item import Ui_item
from tts_wrapper import (
    SherpaOnnxTTS, SherpaOnnxClient,
    MicrosoftTTS, MicrosoftClient,
    GoogleTransTTS, GoogleTransClient
)
from language_dictionary import *

# Language codes mapping
LANGUAGE_CODES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'pl': 'Polish',
    'vi': 'Vietnamese',
    'th': 'Thai',
    'cs': 'Czech',
    'da': 'Danish',
    'fi': 'Finnish'
}

# TTS providers configuration
PROVIDERS = {
    'onnx': {
        'name': 'ONNX',
        'enabled': True,
        'client_class': SherpaOnnxClient,
        'tts_class': SherpaOnnxTTS,
    },
    'azure': {
        'name': 'Azure',
        'enabled': True,
        'client_class': MicrosoftClient,
        'tts_class': MicrosoftTTS,
    },
    'google': {
        'name': 'Google Translate',
        'enabled': True,
        'client_class': GoogleTransClient,
        'tts_class': GoogleTransTTS,
    }
}

# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

class SherpaOnnxManager:
    MODELS_INFO_URL = "https://k2-fsa.github.io/sherpa/onnx/pretrained_models/index.html"
    DEFAULT_CACHE_DIR = Path.home() / ".cache" / "sherpa-onnx"

    def __init__(self, cache_dir=None):
        self.cache_dir = Path(cache_dir) if cache_dir else self.DEFAULT_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.models = self._get_available_models()

    def _get_available_models(self):
        """Fetch available models from Sherpa-ONNX repository."""
        try:
            response = requests.get(self.MODELS_INFO_URL)
            response.raise_for_status()
            # Parse the HTML to extract model information
            # This is a simplified version - in practice you'd want to properly parse the HTML
            models = []
            # Add model information (this would be parsed from the HTML)
            models.append({
                "name": "English TTS (vits)",
                "url": "https://huggingface.co/csukuangfj/sherpa-onnx-vits-vctk",
                "description": "English TTS model based on VITS",
                "size": "150MB"
            })
            return models
        except Exception as e:
            logging.error(f"Failed to fetch Sherpa-ONNX models: {e}")
            return []

    def download_model(self, model_name, progress_callback=None):
        """Download a specific model."""
        model = next((m for m in self.models if m["name"] == model_name), None)
        if not model:
            raise ValueError(f"Model {model_name} not found")

        target_dir = self.cache_dir / model_name.lower().replace(" ", "_")
        target_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Download model files
            response = requests.get(model["url"], stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192
            downloaded = 0

            target_file = target_dir / "model.onnx"
            with open(target_file, "wb") as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    if progress_callback:
                        progress = (downloaded / total_size) * 100
                        progress_callback(progress)

            return str(target_file)
        except Exception as e:
            logging.error(f"Failed to download model {model_name}: {e}")
            raise

    def get_installed_models(self):
        """Get list of installed models."""
        installed = []
        for model_dir in self.cache_dir.iterdir():
            if model_dir.is_dir() and (model_dir / "model.onnx").exists():
                installed.append(model_dir.name)
        return installed


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize UI
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        
        # Set up logging with more detail
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.debug("Widget initialized")
        
        # Initialize icons
        self.iconDownload = QIcon(":/images/images/download.ico")
        self.iconPlayed = QIcon(":/images/images/play-round-icon.png")
        self.iconTick = QIcon(":/images/images/downloaded.ico")  # Use downloaded.ico as tick
        
        # Create loading spinner movie
        self.spinner = QMovie(":/images/images/loading.gif")  # Use existing loading.gif
        self.spinner.setScaledSize(QSize(16, 16))
        self.active_downloads = {}  # Track active downloads
        
        # Initialize providers dictionary
        self.providers = {
            "azure": True,
            "google": True,
            "google_trans": True,
            "onnx": True
        }
        
        # Set tab titles
        self.ui.tabWidget.setTabText(0, "Speech Engine")
        self.ui.tabWidget.setTabText(1, "Translation")
        self.ui.tabWidget.setTabText(2, "Options")
        
        # Get screen size
        screen = QApplication.primaryScreen()
        self.screenSize = screen.size() if screen else None
        
        # Initialize paths based on frozen state
        home_directory = os.path.expanduser("~")
        if getattr(sys, "frozen", False):
            # Get the path to the user's app data folder
            self.app_data_path = os.path.join(
                home_directory,
                "AppData",
                "Local",
                "Programs",
                "Ace Centre",
                "AACSpeakHelper",
            )
            self.config_path = os.path.join(
                home_directory,
                "AppData",
                "Roaming",
                "Ace Centre",
                "AACSpeakHelper",
                "settings.cfg",
            )
            self.audio_path = os.path.join(
                home_directory,
                "AppData",
                "Roaming",
                "Ace Centre",
                "AACSpeakHelper",
                "Audio Files",
            )
            self.onnx_cache_path = os.path.join(
                home_directory,
                "AppData",
                "Roaming",
                "Ace Centre",
                "AACSpeakHelper",
                "models",
            )
            self.ui.appPath.setText(self.app_data_path)
        elif __file__:
            self.app_data_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir)
            )
            self.config_path = os.path.join(self.app_data_path, "settings.cfg")
            self.audio_path = os.path.join(self.app_data_path, "Audio Files")
            self.onnx_cache_path = os.path.join(self.app_data_path, "models")
            self.ui.appPath.setText(
                os.path.join(self.app_data_path, "AACSpeakHelperServer.py")
            )
        
        # Create necessary directories
        for path in [self.audio_path, self.onnx_cache_path]:
            if not os.path.exists(path):
                os.makedirs(path)
        
        # Initialize state
        self.temp_config_file = None
        self.threadList = []
        self.lock = True
        self.comboBox = "Sherpa-ONNX"  # Default value
        self.ttsEngine = "SherpaOnnxTTS"
        
        # Initialize Sherpa client
        self.sherpa_client = None
        try:
            from .sherpa_integration import SherpaOnnxTTS
            self.sherpa_client = SherpaOnnxTTS()
        except Exception as e:
            logging.error(f"Sherpa initialization failed: {e}")
        
        # Set up UI elements
        self.ui.onnx_cache.setText(self.onnx_cache_path)
        self.ui.clear_cache.clicked.connect(self.cache_clear)
        self.ui.cache_pushButton.clicked.connect(self.open_onnx_cache)
        
        # Connect signals
        self.ui.ttsEngineBox.currentTextChanged.connect(self.on_tts_engine_toggled)
        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(
            lambda: self.on_save_pressed(True)
        )
        self.ui.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(
            self.on_discard_pressed
        )
        self.ui.browseButton.clicked.connect(self.on_browse_button_pressed)
        self.ui.credsFilePathEdit.textChanged.connect(self.on_creds_file_path_changed)
        
        # Load configuration
        self.config = configparser.ConfigParser()
        self.setWindowTitle("Configure TranslateAndTTS: {}".format(self.config_path))
        
        # Initialize default values
        self.notranslate = False
        self.saveAudio_azure = True
        self.overwritePb = True
        self.bypassTTS = False
        
        if os.path.exists(self.config_path):
            self.load_existing_config()
        else:
            self.initialize_default_config()
            
        # Generate voice models
        self.generate_onnx_voice_models()
        self.generate_azure_voice_models()
        self.generate_google_voice_models()
        self.generate_google_trans_voice_models()
        
        # Set initial engine
        self.on_tts_engine_toggled(self.comboBox)
        self.lock = False
        
        # Set list widget styling
        list_style = """
            QListWidget {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QListWidget::item {
                border-bottom: 1px solid #eeeeee;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #e6f3ff;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """
        self.ui.onnx_listWidget.setStyleSheet(list_style)
        self.ui.listWidget_voiceazure.setStyleSheet(list_style)
        self.ui.listWidget_voicegoogle.setStyleSheet(list_style)
        self.ui.listWidget_voicegoogleTrans.setStyleSheet(list_style)
        
        # Set scrollbar styling
        self.ui.onnx_listWidget.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical { width: 30px; }"
        )

        # Set larger font for search boxes
        search_font = QFont()
        search_font.setPointSize(14)
        
        # Debug print search box objects
        logging.debug(f"Azure search box: {self.ui.search_language_azure}")
        logging.debug(f"Google search box: {self.ui.search_language_google}")
        logging.debug(f"ONNX search box: {self.ui.search_language}")
        logging.debug(f"Google Trans search box: {self.ui.search_language_googleTrans}")
        
        self.ui.search_language_azure.setFont(search_font)
        self.ui.search_language_google.setFont(search_font)
        self.ui.search_language.setFont(search_font)  
        self.ui.search_language_googleTrans.setFont(search_font)
        
        # Connect search boxes to filter functions with debug
        logging.debug("Connecting search box signals...")
        
        def debug_text_changed(text, provider):
            print(f"Text changed in {provider} search box: '{text}'")  # Print for immediate feedback
            logging.debug(f"Text changed in {provider} search box: '{text}'")
            self.on_search_changed(text, provider)
            
        def debug_return_pressed(provider):
            print(f"Return pressed in {provider} search box")  # Print for immediate feedback
            logging.debug(f"Return pressed in {provider} search box")
            self.on_search_return(provider)
        
        # Connect with debug wrappers
        self.ui.search_language_azure.textChanged.connect(
            lambda text: debug_text_changed(text, "azure"))
        self.ui.search_language_google.textChanged.connect(
            lambda text: debug_text_changed(text, "google"))
        self.ui.search_language.textChanged.connect(
            lambda text: debug_text_changed(text, "onnx"))
        self.ui.search_language_googleTrans.textChanged.connect(
            lambda text: debug_text_changed(text, "google_trans"))
        
        self.ui.search_language_azure.returnPressed.connect(
            lambda: debug_return_pressed("azure"))
        self.ui.search_language_google.returnPressed.connect(
            lambda: debug_return_pressed("google"))
        self.ui.search_language.returnPressed.connect(
            lambda: debug_return_pressed("onnx"))
        self.ui.search_language_googleTrans.returnPressed.connect(
            lambda: debug_return_pressed("google_trans"))
        
        logging.debug("Search box signals connected")
        
        # Set placeholder text for search boxes
        self.ui.search_language_azure.setPlaceholderText("Search Azure voices...")
        self.ui.search_language_google.setPlaceholderText("Search Google voices...")
        self.ui.search_language.setPlaceholderText("Search ONNX voices...")
        self.ui.search_language_googleTrans.setPlaceholderText("Search Google Trans voices...")
        
    def load_existing_config(self):
        """Load configuration from existing config file."""
        try:
            config = configparser.ConfigParser()
            config_path = os.path.join(os.path.dirname(__file__), "config.ini")
            if os.path.exists(config_path):
                config.read(config_path)
                
                if "Providers" in config:
                    for provider in self.providers:
                        if provider in config["Providers"]:
                            self.providers[provider] = config["Providers"].getboolean(provider)
                
                if "Settings" in config:
                    settings = config["Settings"]
                    if "language" in settings:
                        self.current_language = settings["language"]
                    if "voice" in settings:
                        self.current_voice = settings["voice"]
                    if "provider" in settings:
                        self.current_provider = settings["provider"]
                
                self.generate_azure_voice_models()
                self.generate_google_voice_models()
                self.generate_onnx_voice_models()
                self.generate_google_trans_voice_models()
                self.pool_starter()
                self.get_microsoft_language()
                
                # Load configuration values
                self.notranslate = self.ttsEngine = self.config.getboolean(
                    "translate", "no_translate"
                )
                self.startLang = self.config.get("translate", "start_lang")
                self.endLang = self.config.get("translate", "end_lang")
                self.overwritePb = self.config.getboolean("translate", "replace_pb")
                self.bypassTTS = self.config.getboolean("TTS", "bypass_tts")
                self.provider = self.config.get("translate", "provider")
                
                # Update UI with loaded values
                self.ui.comboBox_provider.setCurrentIndex(
                    self.ui.comboBox_provider.findText(self.provider)
                )
                self.ui.checkBox_translate.setChecked(not self.notranslate)
                self.ui.checkBox_overwritepb.setChecked(self.overwritePb)
                self.ui.checkBox_bypass.setChecked(self.bypassTTS)
                self.ui.spinBox_threshold.setValue(
                    int(self.config.get("appCache", "threshold"))
                )
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            self.initialize_default_config()

    def initialize_default_config(self):
        """Initialize default configuration."""
        try:
            self.generate_onnx_voice_models()
            self.generate_azure_voice_models()
            self.generate_google_voice_models()
            
            # Load language codes
            self.ui.comboBox_writeLang.addItems(LANGUAGE_CODES.values())
            self.ui.comboBox_targetLang.addItems(LANGUAGE_CODES.values())
            
            # Set default values
            self.ui.comboBox_writeLang.setCurrentText("English")
            self.ui.comboBox_targetLang.setCurrentText("Chinese (Simplified)")
            self.ui.comboBox_provider.addItems(["google", "azure", "google_trans", "onnx"])
            self.ui.comboBox_provider.setCurrentText("google")
            
            # Set default paths
            self.ui.appPath.setText(os.path.dirname(__file__))
            
        except Exception as e:
            logging.error(f"Error initializing default config: {e}")

    def event_filter(self, obj, event):
        """Filter events for the widget."""
        if event.type() == QEvent.Type.Timer:
            self.ui.validate_google.setVisible(self.ui.credsFilePathEdit.text() != "")
            self.ui.validate_azure.setVisible(
                self.ui.lineEdit_key.text() != "" and self.ui.lineEdit_region.text() != ""
            )
        return super().event_filter(obj, event)

    def on_tts_engine_toggled(self, text):
        """Handle TTS engine selection changes."""
        if text == "Azure TTS":
            self.ui.stackedWidget.setCurrentIndex(0)
            if self.screenSize and self.screenSize.height() > 800:
                self.ui.listWidget_voiceazure.setFixedHeight(400)
        elif text == "Google TTS":
            self.ui.stackedWidget.setCurrentIndex(1)
            if self.screenSize and self.screenSize.height() > 800:
                self.ui.listWidget_voicegoogle.setFixedHeight(400)
        elif text == "GoogleTranslator TTS":
            self.ui.stackedWidget.setCurrentIndex(2)
        elif text == "Sherpa-ONNX":
            self.ui.stackedWidget.setCurrentIndex(6)
            if self.screenSize and self.screenSize.height() > 800:
                self.ui.onnx_listWidget.setFixedHeight(400)
        else:
            self.ui.stackedWidget.setCurrentIndex(5)

    def on_save_pressed(self, permanent=True):
        self.ui.statusBar.clear()
        if (
            self.ui.listWidget_voiceazure.currentItem() is None
            or self.ui.listWidget_voiceazure.currentItem().toolTip() == ""
            and self.ui.stackedWidget.currentIndex() == 0
        ):
            self.ui.statusBar.setText(
                "Failed to save settings. Please select voice model."
            )
            return
        if (
            self.ui.listWidget_voicegoogle.currentItem() is None
            or self.ui.listWidget_voicegoogle.currentItem().toolTip() == ""
            and self.ui.stackedWidget.currentIndex() == 1
        ):
            self.ui.statusBar.setText(
                "Failed to save settings. Please select voice model."
            )
            return
        if (
            self.ui.onnx_listWidget.currentItem() is None
            or self.ui.onnx_listWidget.currentItem().toolTip() == ""
            and self.ui.stackedWidget.currentIndex() == 6
        ):
            self.ui.statusBar.setText(
                "Failed to save settings. Please select voice model."
            )
            return
        if (
            self.ui.listWidget_voicegoogleTrans.currentItem() is None
            or self.ui.listWidget_voicegoogleTrans.currentItem().toolTip() == ""
            and self.ui.stackedWidget.currentIndex() == 2
        ):
            self.ui.statusBar.setText(
                "Failed to save settings. Please select voice model."
            )
            return
        # TODO: Block saving if API-key is blank
        # Add sections and key-value pairs
        self.startLang = self.translate_languages[
            self.ui.comboBox_writeLang.currentText()
        ]
        self.endLang = self.translate_languages[
            self.ui.comboBox_targetLang.currentText()
        ]
        self.notranslate = not self.ui.checkBox_translate.isChecked()

        identifier = self.get_uuid()
        # TODO: check this function later
        # self.config.clear()

        (
            self.config.add_section("App")
            if not self.config.has_section("App")
            else print("")
        )
        self.config.set("App", "uuid", str(identifier))
        self.config.set("App", "collectstats", str(self.ui.checkBox_stats.isChecked()))

        (
            self.config.add_section("translate")
            if not self.config.has_section("translate")
            else print("")
        )
        self.config.set("translate", "no_translate", str(self.notranslate))
        self.config.set("translate", "start_lang", self.startLang)
        self.config.set("translate", "end_lang", self.endLang)
        self.config.set(
            "translate", "replace_pb", str(self.ui.checkBox_overwritepb.isChecked())
        )
        self.config.set(
            "translate", "provider", str(self.ui.comboBox_provider.currentText())
        )

        self.config.set(
            "translate",
            "my_memory_translator_secret_key",
            self.ui.mymemory_secret_key.text(),
        )
        self.config.set("translate", "email", self.ui.email_mymemory.text())
        self.config.set(
            "translate", "libre_translator_secret_key", self.ui.LibreTranslate_secret_key.text()
        )
        self.config.set("translate", "url", self.ui.LibreTranslate_url.text())
        self.config.set(
            "translate",
            "deep_l_translator_secret_key",
            self.ui.deepl_secret_key.text(),
        )
        self.config.set(
            "translate",
            "deepl_pro",
            str(self.ui.checkBox_pro.isChecked()).lower()
        )
        # Add default microsofttranslator_secret_key if not permanent.
        self.config.set(
            "translate",
            "microsoft_translator_secret_key",
            self.ui.microsoft_secret_key.text(),
        )
        self.config.set("translate", "region", self.ui.microsoft_region.text())
        self.config.set(
            "translate", "yandex_translator_secret_key", self.ui.yandex_secret_key.text()
        )
        self.config.set(
            "translate", "papago_translator_client_id", self.ui.papago_client_id.text()
        )
        self.config.set(
            "translate", "papago_translator_secret_key", self.ui.papago_secret_key.text()
        )
        self.config.set(
            "translate", "baidu_translator_appid", self.ui.baidu_appid.text()
        )
        self.config.set(
            "translate", "baidu_translator_secret_key", self.ui.baidu_secret_key.text()
        )
        self.config.set(
            "translate", "qcri_translator_secret_key", self.ui.qcri_secret_key.text()
        )

        (
            self.config.add_section("TTS")
            if not self.config.has_section("TTS")
            else print("")
        )
        self.config.set("TTS", "engine", self.ttsEngine)
        if self.ttsEngine == "azureTTS":
            if permanent:
                self.config.set(
                    "TTS",
                    "save_audio_file",
                    str(self.ui.checkBox_saveAudio.isChecked()),
                )
            else:
                self.config.set("TTS", "save_audio_file", str(False))
        elif self.ttsEngine == "googleTTS":
            if permanent:
                self.config.set(
                    "TTS",
                    "save_audio_file",
                    str(self.ui.checkBox_saveAudio_gTTS.isChecked()),
                )
            else:
                self.config.set("TTS", "save_audio_file", str(False))
        elif self.ttsEngine == "SherpaOnnxTTS":
            if permanent:
                self.config.set(
                    "TTS", "save_audio_file", str(self.ui.onnx_checkBox.isChecked())
                )
            else:
                self.config.set("TTS", "save_audio_file", str(False))
        elif self.ttsEngine == "googleTransTTS":
            if permanent:
                self.config.set(
                    "TTS",
                    "save_audio_file",
                    str(self.ui.checkBox_saveAudio_googleTrans.isChecked()),
                )
            else:
                self.config.set("TTS", "save_audio_file", str(False))
        else:
            self.config.set("TTS", "save_audio_file", str(False))

        self.config.set("TTS", "voice_id", self.ui.lineEdit_voiceID.text())
        self.config.set("TTS", "rate", str(self.ui.horizontalSlider_rate.value()))
        self.config.set(
            "TTS", "volume", str(self.ui.horizontalSlider_volume.value())
        )
        self.config.set(
            "TTS", "bypass_tts", str(self.ui.bypass_tts_checkBox.isChecked())
        )

        (
            self.config.add_section("azureTTS")
            if not self.config.has_section("azureTTS")
            else print("")
        )
        if self.ui.lineEdit_key.text() == "" and not permanent:
            self.config.set("azureTTS", "key", ms_token)
        else:
            self.config.set("azureTTS", "key", self.ui.lineEdit_key.text())
        if self.ui.lineEdit_region.text() == "" and not permanent:
            self.config.set("azureTTS", "location", ms_region)
        else:
            self.config.set("azureTTS", "location", self.ui.lineEdit_region.text())
        if self.ui.listWidget_voiceazure.currentItem() is None:
            self.config.set("azureTTS", "voice_id", "en-US-JennyNeural")
        else:
            self.config.set(
                "azureTTS",
                "voice_id",
                self.ui.listWidget_voiceazure.currentItem().toolTip(),
            )

        (
            self.config.add_section("googleTTS")
            if not self.config.has_section("googleTTS")
            else print("")
        )
        if self.credsFilePath == "" and not permanent:
            self.config.set("googleTTS", "creds", google_creds_path)
        else:
            self.config.set("googleTTS", "creds", self.credsFilePath)
        if self.ui.listWidget_voicegoogle.currentItem() is None:
            self.config.set("googleTTS", "voice_id", "en-US-Wavenet-C")
        else:
            self.config.set(
                "googleTTS",
                "voice_id",
                self.ui.listWidget_voicegoogle.currentItem().toolTip(),
            )
        if self.ui.listWidget_voicegoogleTrans.currentItem() is None:
            self.config.set("googleTransTTS", "voice_id", "en-co.uk")
        else:
            self.config.set(
                "googleTransTTS",
                "voice_id",
                self.ui.listWidget_voicegoogleTrans.currentItem().toolTip(),
            )


        (
            self.config.add_section("SherpaOnnxTTS")
            if not self.config.has_section("SherpaOnnxTTS")
            else print("")
        )
        (
            self.config.add_section("googleTransTTS")
            if not self.config.has_section("googleTransTTS")
            else print("")
        )
        if self.ui.onnx_listWidget.currentItem() is None:
            self.config.set("SherpaOnnxTTS", "voice_id", "eng")
        else:
            self.config.set(
                "SherpaOnnxTTS",
                "voice_id",
                self.ui.onnx_listWidget.currentItem().toolTip(),
            )

        (
            self.config.add_section("appCache")
            if not self.config.has_section("appCache")
            else print("")
        )
        self.config.set("appCache", "threshold", str(self.ui.spinBox_threshold.value()))

        # Write the configuration to a file
        if permanent:
            with open(self.config_path, "w") as configfile:
                self.config.write(configfile)
                logging.info(
                    "Configuration file is saved on {}".format(self.config_path)
                )
                self.ui.statusBar.setText("Saving settings is successful.")
            # self.close()
        else:
            self.temp_config_file = tempfile.NamedTemporaryFile(delete=False)
            with open(self.temp_config_file.name, "w") as configfile:
                self.config.write(configfile)
                logging.info(
                    "Configuration file is saved on {}".format(
                        self.temp_config_file.name
                    )
                )

    def on_discard_pressed(self):
        self.close()

    def on_browse_button_pressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.credsFilePath, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File containing OAuth 2.0 Credentials",
            "",
            "JSON Files (*.json)",
            options=options,
        )
        self.ui.credsFilePathEdit.setText(self.credsFilePath)

    def on_creds_file_path_changed(self):
        self.credsFilePath = self.ui.credsFilePathEdit.text()

    def get_uuid(self):
        try:
            # Code that may raise an exception
            if os.path.isfile(self.config_path) and self.config.has_section("App"):
                id = self.config.get("App", "uuid")
                identifier = uuid.UUID(id)
            else:
                identifier = uuid.uuid4()
        except Exception as e:
            # Code to handle other exceptions
            identifier = uuid.uuid4()
            logging.error(
                "UUID Error: {}. Generating UUID is successful.".format(e),
                exc_info=False,
            )
        return identifier

    def set_parameter(self, string):
        self.ui.comboBox_writeLang.clear()
        self.ui.comboBox_targetLang.clear()
        match string:
            case "GoogleTranslator":
                try:
                    self.translate_languages = Google_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.google)
                )
            case "MyMemoryTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.mymemory_secret_key.setText(
                            self.config.get(
                                "translate", "my_memory_translator_secret_key"
                            )
                        )
                        self.ui.email_mymemory.setText(
                            self.config.get("translate", "email")
                        )
                    self.translate_languages = MyMemory_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.mymemory)
                )
            case "LibreTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.LibreTranslate_secret_key.setText(
                            self.config.get("translate", "libre_translator_secret_key")
                        )
                        self.ui.LibreTranslate_url.setText(
                            self.config.get("translate", "url")
                        )
                    self.translate_languages = Libre_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.libretranslate)
                )
            case "DeeplTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.deepl_secret_key.setText(
                            self.config.get("translate", "deep_l_translator_secret_key")
                        )
                        self.ui.checkBox_pro.setChecked(
                            self.config.getboolean("translate", "deepl_pro")
                        )
                    self.translate_languages = DeepL_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.deepl)
                )
            case "MicrosoftTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.microsoft_secret_key.setText(
                            self.config.get(
                                "translate", "microsoft_translator_secret_key"
                            )
                        )
                        self.ui.microsoft_region.setText(
                            self.config.get("translate", "region")
                        )
                    self.translate_languages = Microsoft_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.microsoft)
                )
            case "PonsTranslator":
                try:
                    self.translate_languages = Pons_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.pons)
                )
            case "LingueeTranslator":
                try:
                    self.translate_languages = Linguee_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.linguee)
                )
            case "PapagoTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.papago_secret_key.setText(
                            self.config.get("translate", "papago_translator_secret_key")
                        )
                        self.ui.papago_client_id.setText(
                            self.config.get("translate", "papago_translator_client_id")
                        )
                    self.translate_languages = Papago_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.papago)
                )
            case "QcriTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.qcri_secret_key.setText(
                            self.config.get("translate", "qcri_translator_secret_key")
                        )
                    self.translate_languages = Qcri_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.qcri)
                )
            case "BaiduTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.baidu_secret_key.setText(
                            self.config.get("translate", "baidu_translator_secret_key")
                        )
                        self.ui.baidu_appid.setText(
                            self.config.get("translate", "baidu_translator_appid")
                        )
                    self.translate_languages = Baidu_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.baidu)
                )
            case "YandexTranslator":
                try:
                    if os.path.exists(self.config_path):
                        self.ui.yandex_secret_key.setText(
                            self.config.get("translate", "yandex_translator_secret_key")
                        )
                    self.translate_languages = Yandex_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.yandex)
                )
        self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
        self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
        self.set_translate_dropdown(self.translate_languages)

    def update_language(self, language_input):
        self.ui.statusBar.setText("")
        if self.lock:
            return
        match self.ui.ttsEngineBox.currentText():
            case "Azure TTS":
                for text in list(azure_tts_list.keys()):
                    if self.ui.comboBox_targetLang.currentText() in text:
                        self.ui.statusBar.setText(
                            "Azure TTS might be compatible to the Translation Engine"
                        )
                        return
            case "Google TTS":
                for text in list(google_TTS_list.keys()):
                    if self.ui.comboBox_targetLang.currentText() in text:
                        self.ui.statusBar.setText(
                            "Google TTS might be compatible to the Translation Engine"
                        )
                        return
            case "GSpeak":
                for text in list(gSpeak_TTS_list.keys()):
                    if self.ui.comboBox_targetLang.currentText() in text:
                        self.ui.statusBar.setText(
                            "GSpeak might be compatible to the Translation Engine"
                        )
                        return
            case _:
                pass
        # # TODO: Iterate targetlang and text to check compatibility

    def set_azure_voice(self, text):
        if text == "":
            text = "en-US-JennyNeural"
        for index in range(self.ui.listWidget_voiceazure.count()):
            item = self.ui.listWidget_voiceazure.item(index)
            if text == item.toolTip():
                self.azure_row = self.ui.listWidget_voiceazure.row(item)
                self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                break

    def preview_pressed(self):
        self.currentButton = self.sender()
        text = self.sender().parent().findChild(QLabel, "name").text()
        
        if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
            parentWidget = self.ui.listWidget_voiceazure
            for index in range(self.ui.listWidget_voiceazure.count()):
                item = self.ui.listWidget_voiceazure.item(index)
                if text == item.text():
                    self.azure_row = self.ui.listWidget_voiceazure.row(item)
                    self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                    break
        elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
            parentWidget = self.ui.listWidget_voicegoogle
            for index in range(self.ui.listWidget_voicegoogle.count()):
                item = self.ui.listWidget_voicegoogle.item(index)
                if text == item.text():
                    self.google_row = self.ui.listWidget_voicegoogle.row(item)
                    self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                    break
        elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
            parentWidget = self.ui.onnx_listWidget
            for index in range(self.ui.onnx_listWidget.count()):
                item = self.ui.onnx_listWidget.item(index)
                if text == item.text():
                    self.onnx_row = self.ui.onnx_listWidget.row(item)
                    self.ui.onnx_listWidget.setCurrentRow(self.onnx_row)
                    break
        elif self.ui.stackedWidget.currentWidget() == self.ui.gspeak_page:
            parentWidget = self.ui.listWidget_voicegoogleTrans
            for index in range(self.ui.listWidget_voicegoogleTrans.count()):
                item = self.ui.listWidget_voicegoogleTrans.item(index)
                if text == item.text():
                    self.googleTrans_row = self.ui.listWidget_voicegoogleTrans.row(item)
                    self.ui.listWidget_voicegoogleTrans.setCurrentRow(self.googleTrans_row)
                    break
        self.on_save_pressed(False)
        if self.temp_config_file is None:
            return
        pyperclip.copy("Hello World")
        pool = QThreadPool.globalInstance()
        runnable = Player(self.temp_config_file)
        runnable.signals.completed.connect(self.enable_play_buttons)
        buttons = parentWidget.findChildren(QPushButton)
        self.movie = QMovie(":/images/images/loading.gif")
        self.movie.updated.connect(self.update_buttons)
        self.movie.start()
        self.ui.ttsEngineBox.setEnabled(False)
        for button in buttons:
            button.setEnabled(False)
        pool.start(runnable)

    def update_buttons(self):
        loading_icon = QIcon(self.movie.currentPixmap())
        self.currentButton.setIcon(loading_icon)

    def enable_play_buttons(self):
        if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
            buttons = self.ui.listWidget_voiceazure.findChildren(QPushButton)
        elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
            buttons = self.ui.listWidget_voicegoogle.findChildren(QPushButton)
        elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
            buttons = self.ui.onnx_listWidget.findChildren(QPushButton)
        elif self.ui.stackedWidget.currentWidget() == self.ui.gspeak_page:
            buttons = self.ui.listWidget_voicegoogleTrans.findChildren(QPushButton)
        self.ui.ttsEngineBox.setEnabled(True)
        for button in buttons:
            button.setEnabled(True)
        self.movie.stop()
        icon = QIcon()
        icon.addFile(":/images/images/play-round-icon.png")
        self.currentButton.setIcon(icon)
        self.temp_config_file.close()
        os.unlink(self.temp_config_file.name)
        self.ui.statusBar.setText(f"")
        self.temp_config_file = None

    def print_data(self, item):
        try:
            if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
                self.ui.listWidget_voiceazure.setCurrentItem(item)
            elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
                self.ui.listWidget_voicegoogle.setCurrentItem(item)
            elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
                self.ui.onnx_listWidget.setCurrentItem(item)
            elif self.ui.stackedWidget.currentWidget() == self.ui.gspeak_page:
                self.ui.listWidget_voicegoogleTrans.setCurrentItem(item)
        except Exception as error:
            pass

    def update_row(self, row):
        try:
            # Set the row when index become zero (no selected item)
            if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
                if self.ui.listWidget_voiceazure.currentItem() is None:
                    self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                    self.ui.listWidget_voiceazure.setCurrentItem(
                        self.ui.listWidget_voiceazure.item(self.azure_row)
                    )
                self.ui.azure_voice_models.setTitle(
                    f"Current Voice Model: {self.ui.listWidget_voiceazure.currentItem().text()}"
                )
            elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
                if self.ui.listWidget_voicegoogle.currentItem() is None:
                    self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                    self.ui.listWidget_voicegoogle.setCurrentItem(
                        self.ui.listWidget_voicegoogle.item(self.google_row)
                    )
                self.ui.google_voice_models.setTitle(
                    f"Current Voice Model: {self.ui.listWidget_voicegoogle.currentItem().text()}"
                )
            elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
                if self.ui.onnx_listWidget.currentItem() is None:
                    self.ui.onnx_listWidget.setCurrentRow(self.onnx_row)
                    self.ui.onnx_listWidget.setCurrentItem(
                        self.ui.onnx_listWidget.item(self.onnx_row)
                    )
                self.ui.onnx_voice_models.setTitle(
                    f"Current Voice Model: {self.ui.onnx_listWidget.currentItem().text()} - {self.ui.onnx_listWidget.currentItem().toolTip()}"
                )
            elif self.ui.stackedWidget.currentWidget() == self.ui.gspeak_page:
                if self.ui.listWidget_voicegoogleTrans.currentItem() is None:
                    self.ui.listWidget_voicegoogleTrans.setCurrentRow(
                        self.googleTrans_row
                    )
                    self.ui.listWidget_voicegoogleTrans.setCurrentItem(
                        self.ui.listWidget_voicegoogleTrans.item(self.googleTrans_row)
                    )
                self.ui.gspeak_voice_models.setTitle(
                    f"Current Voice Model: {self.ui.listWidget_voicegoogleTrans.currentItem().text()}"
                )
        except Exception as error:
            logging.error(f"Voice Model Error: {error}")

    def filter_voices(self, provider: str, search_text: str):
        """Filter voices in the list widget based on search text."""
        logging.debug(f"Search changed handler called - Provider: {provider}, Text: '{search_text}'")
        
        # Get the appropriate list widget based on provider
        list_widget = None
        if provider == "azure":
            list_widget = self.ui.listWidget_voiceazure
        elif provider == "google":
            list_widget = self.ui.listWidget_voicegoogle
        elif provider == "onnx":
            list_widget = self.ui.onnx_listWidget
        elif provider == "google_trans":
            list_widget = self.ui.listWidget_voicegoogleTrans
        
        if not list_widget:
            return
            
        logging.debug(f"Filtering voices with: '{search_text}'")
        
        # Get total items in list widget
        total_items = list_widget.count()
        logging.debug(f"List widget has {total_items} items")
        
        if total_items == 0:
            logging.debug("No voices found in list widget")
            return
            
        # Iterate through all items
        for i in range(total_items):
            item = list_widget.item(i)
            if not item:
                continue
                
            # Get voice data
            voice_data = item.data(Qt.UserRole)
            if not voice_data:
                continue
                
            # Get searchable text - combine name and ID
            name = voice_data.get('name', '').lower()
            voice_id = voice_data.get('id', '').lower()
            language = voice_data.get('language', '').lower()
            searchable_text = f"{name} {voice_id} {language}"
            
            # Show/hide based on search
            should_show = not search_text or search_text.lower() in searchable_text
            item.setHidden(not should_show)
            
        logging.debug(f"Finished filtering voices for {provider}")

    def filter_azure_voices(self):
        self.filter_voices("azure", self.ui.search_language_azure.text())

    def filter_google_voices(self):
        self.filter_voices("google", self.ui.search_language_google.text())

    def filter_onnx_voices(self):
        self.filter_voices("onnx", self.ui.search_language.text())

    def filter_google_trans_voices(self):
        self.filter_voices("google_trans", self.ui.search_language_googleTrans.text())

    def generate_azure_voice_models(self):
        """Generate Azure voice models."""
        try:
            if not self.lock:
                return
            logging.info("Generating Azure voice models...")
            
            # Run in main thread since we're accessing Qt widgets
            self.ui.listWidget_voiceazure.clear()
            if hasattr(self.ui, 'azure_progressBar'):
                self.ui.azure_progressBar.setVisible(True)
            
            # Create voice models
            voices = self.get_azure_voices()
            if voices:
                for i, voice in enumerate(voices):
                    try:
                        # Create list widget item
                        item = QListWidgetItem()
                        item.setSizeHint(QSize(0, 80))
                        
                        # Create custom widget
                        widget = QWidget()
                        layout = QHBoxLayout(widget)
                        
                        # Add voice name label
                        name = voice.get('name', 'Unknown')
                        name_label = QLabel(name)
                        name_label.setStyleSheet("font-weight: bold;")
                        layout.addWidget(name_label)
                        
                        # Add spacer
                        layout.addStretch()
                        
                        # Add preview button
                        preview_btn = QPushButton("Preview")
                        preview_btn.setIcon(self.iconPlayed)
                        preview_btn.clicked.connect(lambda: self.preview_voice(voice.get('id')))
                        layout.addWidget(preview_btn)
                        
                        # Set item widget and tooltip
                        self.ui.listWidget_voiceazure.addItem(item)
                        self.ui.listWidget_voiceazure.setItemWidget(item, widget)
                        item.setToolTip(voice.get('id', ''))
                        
                        # Store voice data
                        item.setData(Qt.UserRole, voice)
                        
                        # Update progress
                        if hasattr(self.ui, 'azure_progressBar'):
                            progress = int((i + 1) / len(voices) * 100)
                            self.ui.azure_progressBar.setValue(progress)
                    except Exception as e:
                        logging.error(f"Error loading Azure voice item: {e}")
                        continue
            
            if hasattr(self.ui, 'azure_progressBar'):
                self.ui.azure_progressBar.setVisible(False)
            
        except Exception as e:
            logging.error(f"Error loading Azure voice models: {e}")
            if hasattr(self.ui, 'azure_progressBar'):
                self.ui.azure_progressBar.setVisible(False)

    def get_azure_voices(self):
        """Get list of available Azure voices."""
        try:
            key = os.environ.get('MICROSOFT_TOKEN', '')
            region = os.environ.get('MICROSOFT_REGION', '')
            if not key or not region:
                logging.warning("Azure TTS credentials not found in environment variables")
                return []
                
            client = MicrosoftClient(credentials=(key, region))
            tts = MicrosoftTTS(client)
            voices = tts.get_voices()  
            return [{'id': voice.id, 'name': voice.name} for voice in voices]
        except Exception as e:
            logging.error(f"Error getting Azure voices: {e}")
            return []

    def get_google_voices(self):
        file = PySide6.QtCore.QFile(":/binary/google_voices.json")
        if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
            text = PySide6.QtCore.QTextStream(file).readAll()
            self.voice_google_list = json.loads(text.encode())
            logging.info("Google voice list fetched from Resource file.")
            file.close()
        return self.voice_google_list

    def pool_starter(self):
        try:
            pool = QThreadPool.globalInstance()
            for thread in self.threadList:
                pool.start(thread)
        except Exception as threadError:
            print(f"ThreadPool Error: {threadError}")
            logging.error(f"ThreadPool Error: {threadError}")

    def handle_error(self, string, tts):
        if tts == "Azure TTS":
            self.ui.lineEdit_key.clear()
            self.ui.lineEdit_region.clear()
            self.ui.lineEdit_key.setPlaceholderText("Invalid Token")
            self.ui.lineEdit_region.setPlaceholderText("Invalid Region")
        elif tts == "Google TTS":
            self.ui.credsFilePathEdit.clear()
            self.ui.credsFilePathEdit.setPlaceholderText("Invalid JSON Credentials")

    def get_google_credentials(self, filename, default=False):
        try:
            if filename is not None and os.path.isfile(filename) and not default:
                logging.info("Using User Defined Google Credentials")
                return filename
            else:
                if default:
                    logging.info("Using Default Google Credentials")
                    return load_credentials(google_creds_path)
                else:
                    logging.info(f"Invalid Google Credentials {filename}")
            return google_creds_path
        except Exception as e:
            print(f'Error: {e}')
            return google_creds_path

    def generate_google_voice_models(self):
        """Generate Google voice models."""
        try:
            if not self.lock:
                return
            logging.info("Generating Google voice models...")
            
            # Clear list and show progress
            self.ui.listWidget_voicegoogle.clear()
            
            # Create custom widget for each voice
            voices = self.get_google_trans_voices()
            if voices:
                for i, voice in enumerate(voices):
                    # Create list widget item
                    item = QListWidgetItem()
                    item.setSizeHint(QSize(0, 80))  
                    
                    # Create custom widget
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    
                    # Add voice name label
                    name = voice.get('name', 'Unknown')
                    name_label = QLabel(name)
                    name_label.setStyleSheet("font-weight: bold;")
                    layout.addWidget(name_label)
                    
                    # Add spacer
                    layout.addStretch()
                    
                    # Add preview button
                    preview_btn = QPushButton("Preview")
                    preview_btn.setIcon(self.iconPlayed)
                    preview_btn.clicked.connect(lambda: self.preview_voice(voice.get('id')))
                    layout.addWidget(preview_btn)
                    
                    # Set item widget
                    self.ui.listWidget_voicegoogle.addItem(item)
                    self.ui.listWidget_voicegoogle.setItemWidget(item, widget)
                    
                    # Store voice data
                    item.setData(Qt.UserRole, voice)
                    
                    # Update progress
                    if hasattr(self.ui, 'google_progressBar'):
                        progress = int((i + 1) / len(voices) * 100)
                        self.ui.google_progressBar.setValue(progress)
            
            if hasattr(self.ui, 'google_progressBar'):
                self.ui.google_progressBar.setVisible(False)
            
        except Exception as e:
            logging.error(f"Error loading Google voice models: {e}")
            if hasattr(self.ui, 'google_progressBar'):
                self.ui.google_progressBar.setVisible(False)

    def generate_onnx_voice_models(self):
        """Generate ONNX voice models."""
        try:
            if not self.lock:
                return
            logging.info("Generating ONNX voice models...")
            
            # Clear list and show progress
            self.ui.onnx_listWidget.clear()
            if hasattr(self.ui, 'onnx_progressBar'):
                self.ui.onnx_progressBar.setVisible(True)
                self.ui.onnx_progressBar.setValue(0)
            
            # Try to get voices from ONNX client
            try:
                client = SherpaOnnxClient(model_path=self.onnx_cache_path, tokens_path=None)
                tts = SherpaOnnxTTS(client)
                onnx_voices = tts.get_voices()  
                if onnx_voices:
                    voices = onnx_voices
                else:
                    voices = []
                    logging.warning("No voices returned from ONNX client")
            except Exception as e:
                voices = []
                logging.error(f"Error getting voices from ONNX client: {e}")
            
            # Add voices to list widget
            for i, voice in enumerate(voices):
                try:
                    # Create list widget item
                    item = QListWidgetItem()
                    item.setSizeHint(QSize(0, 100))  # Increased height for more details
                    
                    # Create custom widget
                    widget = QWidget()
                    layout = QVBoxLayout(widget)  # Changed to vertical layout
                    
                    # Top row with name and buttons
                    top_row = QHBoxLayout()
                    
                    # Add voice details
                    details_widget = QWidget()
                    details_layout = QVBoxLayout(details_widget)
                    
                    # Create horizontal layout for name and status icon
                    name_layout = QHBoxLayout()
                    
                    # Name and language
                    name = voice.get('name', 'Unknown')
                    language = voice.get('language', '')
                    name_label = QLabel(f"<b>{name}</b>")
                    name_layout.addWidget(name_label)
                    
                    # Add status icon (tick if downloaded)
                    status_label = QLabel()
                    model_path = os.path.join(self.onnx_cache_path, f"{voice.get('id', '')}.onnx")
                    if os.path.exists(model_path):
                        status_label.setPixmap(self.iconTick.pixmap(16, 16))
                    name_layout.addWidget(status_label)
                    name_layout.addStretch()
                    
                    details_layout.addLayout(name_layout)
                    
                    # Additional details
                    details = []
                    if voice.get('gender'):
                        details.append(f"Gender: {voice.get('gender')}")
                    if voice.get('script'):
                        details.append(f"Script: {voice.get('script')}")
                    if voice.get('locale'):
                        details.append(f"Locale: {voice.get('locale')}")
                    if voice.get('style'):
                        details.append(f"Style: {voice.get('style')}")
                    
                    if details:
                        details_label = QLabel(" | ".join(details))
                        details_label.setStyleSheet("color: #666;")
                        details_layout.addWidget(details_label)
                    
                    top_row.addWidget(details_widget)
                    top_row.addStretch()
                    
                    # Add buttons
                    buttons_widget = QWidget()
                    buttons_layout = QHBoxLayout(buttons_widget)
                    buttons_layout.setContentsMargins(0, 0, 0, 0)
                    
                    # Preview button
                    preview_btn = QPushButton("Preview")
                    preview_btn.setIcon(self.iconPlayed)
                    preview_btn.clicked.connect(lambda checked, v=voice: self.preview_voice(v.get('id')))
                    buttons_layout.addWidget(preview_btn)
                    
                    # Download button or spinner - only show if model not downloaded
                    if not os.path.exists(model_path):
                        download_container = QWidget()
                        download_layout = QHBoxLayout(download_container)
                        download_layout.setContentsMargins(0, 0, 0, 0)
                        
                        download_btn = QPushButton("Download")
                        download_btn.setIcon(self.iconDownload)
                        download_btn.clicked.connect(lambda checked, v=voice, b=download_btn, c=download_container: 
                                                  self.start_download(v.get('id'), b, c))
                        download_layout.addWidget(download_btn)
                        
                        # Create spinner label (hidden by default)
                        spinner_label = QLabel()
                        spinner_label.setMovie(self.spinner)
                        spinner_label.hide()
                        download_layout.addWidget(spinner_label)
                        
                        buttons_layout.addWidget(download_container)
                        
                        # Store references for later
                        voice['_download_btn'] = download_btn
                        voice['_spinner_label'] = spinner_label
                        voice['_status_label'] = status_label
                    
                    top_row.addWidget(buttons_widget)
                    layout.addLayout(top_row)
                    
                    # Set item widget and tooltip
                    self.ui.onnx_listWidget.addItem(item)
                    self.ui.onnx_listWidget.setItemWidget(item, widget)
                    
                    # Set tooltip with all voice details
                    tooltip_details = [
                        f"ID: {voice.get('id', 'Unknown')}",
                        f"Language: {voice.get('language', 'Unknown')}",
                    ]
                    if voice.get('gender'):
                        tooltip_details.append(f"Gender: {voice.get('gender')}")
                    if voice.get('script'):
                        tooltip_details.append(f"Script: {voice.get('script')}")
                    if voice.get('locale'):
                        tooltip_details.append(f"Locale: {voice.get('locale')}")
                    if voice.get('style'):
                        tooltip_details.append(f"Style: {voice.get('style')}")
                    
                    item.setToolTip("\n".join(tooltip_details))
                    
                    # Store voice data
                    item.setData(Qt.UserRole, voice)
                    
                    # Update progress
                    if hasattr(self.ui, 'onnx_progressBar'):
                        progress = int((i + 1) / len(voices) * 100)
                        self.ui.onnx_progressBar.setValue(progress)
                        
                    logging.debug(f"Added voice to list: {name}")
                    
                except Exception as e:
                    logging.error(f"Error loading ONNX voice item: {e}")
                    continue
            
            if hasattr(self.ui, 'onnx_progressBar'):
                self.ui.onnx_progressBar.setVisible(False)
            
            logging.info(f"Added {self.ui.onnx_listWidget.count()} voices to ONNX list widget")
            
        except Exception as e:
            logging.error(f"Error loading ONNX voice models: {e}")
            if hasattr(self.ui, 'onnx_progressBar'):
                self.ui.onnx_progressBar.setVisible(False)

    def download_voice(self, voice_id):
        """Download a voice model using SherpaOnnxClient's check_and_download_model."""
        try:
            if not voice_id:
                return
                
            # Initialize client
            client = SherpaOnnxClient(model_path=self.onnx_cache_path, tokens_path=None)
            
            try:
                # Use check_and_download_model which will handle downloading if needed
                result = client.check_and_download_model(voice_id)
                
                # Handle different return values (some versions return 2 values, others 4)
                if isinstance(result, tuple) and len(result) == 4:
                    model_path, tokens_path, lexicon_path, dict_dir = result
                else:
                    model_path, tokens_path = result
                    lexicon_path = ""
                    dict_dir = ""
                
                message = f"Voice model {voice_id} is ready to use.\nModel path: {model_path}"
                if tokens_path:
                    message += f"\nTokens path: {tokens_path}"
                if lexicon_path:
                    message += f"\nLexicon path: {lexicon_path}"
                if dict_dir:
                    message += f"\nDictionary directory: {dict_dir}"
                
                QMessageBox.information(
                    self,
                    "Download Complete",
                    message
                )
                
                # Refresh the voice list to update UI
                self.generate_onnx_voice_models()
                
            except Exception as download_error:
                logging.error(f"Error during model download: {download_error}")
                QMessageBox.warning(
                    self,
                    "Download Failed",
                    f"Failed to download/prepare voice model {voice_id}.\nError: {str(download_error)}"
                )
                
        except Exception as e:
            logging.error(f"Error initializing client for voice {voice_id}: {e}")
            QMessageBox.critical(
                self,
                "Download Error",
                f"Error setting up download for voice model {voice_id}: {str(e)}"
            )

    def generate_google_trans_voice_models(self):
        """Generate Google Translate voice models."""
        try:
            if not self.lock:
                return
            logging.info("Generating Google Translate voice models...")
            
            # Clear list and show progress
            self.ui.listWidget_voicegoogleTrans.clear()
            
            # Create custom widget for each voice
            voices = self.get_google_trans_voices()
            if voices:
                for i, voice in enumerate(voices):
                    # Create list widget item
                    item = QListWidgetItem()
                    item.setSizeHint(QSize(0, 80))  
                    
                    # Create custom widget
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    
                    # Add voice name label
                    name = voice.get('name', 'Unknown')
                    name_label = QLabel(name)
                    name_label.setStyleSheet("font-weight: bold;")
                    layout.addWidget(name_label)
                    
                    # Add spacer
                    layout.addStretch()
                    
                    # Add preview button
                    preview_btn = QPushButton("Preview")
                    preview_btn.setIcon(self.iconPlayed)
                    preview_btn.clicked.connect(lambda: self.preview_voice(voice.get('id')))
                    layout.addWidget(preview_btn)
                    
                    # Set item widget
                    self.ui.listWidget_voicegoogleTrans.addItem(item)
                    self.ui.listWidget_voicegoogleTrans.setItemWidget(item, widget)
                    
                    # Store voice data
                    item.setData(Qt.UserRole, voice)
                    
                    # Update progress
                    if hasattr(self.ui, 'googleTransTTS_progressBar'):
                        progress = int((i + 1) / len(voices) * 100)
                        self.ui.googleTransTTS_progressBar.setValue(progress)
            
            if hasattr(self.ui, 'googleTransTTS_progressBar'):
                self.ui.googleTransTTS_progressBar.setVisible(False)
            
        except Exception as e:
            logging.error(f"Error loading Google Translate voice models: {e}")
            if hasattr(self.ui, 'googleTransTTS_progressBar'):
                self.ui.googleTransTTS_progressBar.setVisible(False)

    def load_progress_onnx(self, value):
        """Show/hide progress bar during voice loading."""
        if value == 100:
            self.ui.onnx_progressBar.hide()
        else:
            self.ui.onnx_progressBar.show()
            self.ui.onnx_progressBar.setValue(value)

    def load_onnx_items(self, index, voice, count):
        """Load Sherpa-ONNX voice items into the list widget."""
        try:
            item = QListWidgetItem(voice)
            item.setToolTip(voice)
            self.ui.onnx_listWidget.addItem(item)
            self.load_progress_onnx(int((index + 1) / count * 100))
        except Exception as e:
            logging.error(f"Error loading ONNX items: {str(e)}")

    def load_google_trans_items(self, index, data, count):
        """Load GoogleTranslator voice items into the list widget."""
        try:
            item = QListWidgetItem(data)
            item.setToolTip(data)
            self.ui.listWidget_voicegoogleTrans.addItem(item)
            self.load_progress_onnx(int((index + 1) / count * 100))
        except Exception as e:
            logging.error(f"Error loading Google Translate items: {str(e)}")

    def get_onnx_voices(self):
        """Get list of available ONNX voices."""
        try:
            client = SherpaOnnxClient()
            tts = SherpaOnnxTTS(client)
            voices = tts.get_voices()  
            voice_list = []
            for voice in voices:
                voice_list.append({
                    'id': voice['id'],
                    'name': voice['name'],
                    'language': voice.get('language', ''),
                    'gender': voice.get('gender', ''),
                    'downloaded': voice.get('is_downloaded', False)
                })
            return voice_list
        except Exception as e:
            logging.error(f"Error getting ONNX voices: {e}")
            return []

    def get_azure_voices(self):
        """Get list of available Azure voices."""
        try:
            key = os.environ.get('MICROSOFT_TOKEN', '')
            region = os.environ.get('MICROSOFT_REGION', '')
            if not key or not region:
                logging.warning("Azure TTS credentials not found in environment variables")
                return []
                
            client = MicrosoftClient(credentials=(key, region))
            tts = MicrosoftTTS(client)
            voices = tts.get_voices()  
            voice_list = []
            for voice in voices:
                voice_list.append({
                    'id': voice['id'],
                    'name': voice['name'],
                    'language': voice.get('language', ''),
                    'gender': voice.get('gender', '')
                })
            return voice_list
        except Exception as e:
            logging.error(f"Error getting Azure voices: {e}")
            return []

    def get_google_trans_voices(self):
        """Get list of available Google Translate voices."""
        try:
            client = GoogleTransClient()
            tts = GoogleTransTTS(client)
            voices = tts.get_voices()  
            voice_list = []
            for voice in voices:
                voice_list.append({
                    'id': voice['id'],
                    'name': voice['name'],
                    'language': voice.get('language', ''),
                    'gender': voice.get('gender', '')
                })
            return voice_list
        except Exception as e:
            logging.error(f"Error getting Google Translate voices: {e}")
            return []

    def preview_voice(self, voice_id):
        """Preview a voice by speaking a sample text."""
        try:
            sample_text = "This is a preview of the selected voice."
            if voice_id.startswith('onnx_'):
                client = SherpaOnnxClient()
                tts = SherpaOnnxTTS(client)
                tts.speak(sample_text, voice_id)
            elif voice_id.startswith('azure_'):
                key = os.environ.get('MICROSOFT_TOKEN', '')
                region = os.environ.get('MICROSOFT_REGION', '')
                if not key or not region:
                    raise ValueError("Azure TTS credentials not found")
                client = MicrosoftClient(credentials=(key, region))
                tts = MicrosoftTTS(client)
                tts.speak(sample_text, voice_id)
            elif voice_id.startswith('google_'):
                client = GoogleTransClient()
                tts = GoogleTransTTS(client)
                tts.speak(sample_text, voice_id)
        except Exception as e:
            logging.error(f"Error previewing voice {voice_id}: {e}")
            QMessageBox.warning(self, "Preview Error", f"Failed to preview voice: {str(e)}")

    def copy_app_path(self):
        """Copy the application path to clipboard."""
        pyperclip.copy(self.ui.appPath.text())

    def set_google_voice(self, text):
        """Set the selected Google voice."""
        if text == "":
            text = "en-US-Wavenet-C"
        for index in range(self.ui.listWidget_voicegoogle.count()):
            item = self.ui.listWidget_voicegoogle.item(index)
            if text == item.toolTip():
                self.google_row = self.ui.listWidget_voicegoogle.row(item)
                self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                break

    def cache_open(self):
        """Open the audio cache directory."""
        if os.path.isdir(self.audio_path):
            self.ui.statusBar.setText(f"Opened {self.audio_path}")
            os.startfile(self.audio_path)
        else:
            self.ui.statusBar.setText(
                f"No cached detected. Try using main application first."
            )

    def open_onnx_cache(self):
        """Open the ONNX cache directory."""
        if os.path.isdir(self.onnx_cache_path):
            self.ui.statusBar.setText(f"Opened {self.onnx_cache_path}")
            os.startfile(self.onnx_cache_path)
        else:
            os.makedirs(self.onnx_cache_path)
            os.startfile(self.onnx_cache_path)
            self.ui.statusBar.setText(
                f"No cached detected. Creating model directory..."
            )

    def cache_clear(self):
        """Clear the audio cache."""
        pool = QThreadPool.globalInstance()
        runnable = Cleaner(self.audio_path)
        runnable.signals.completed.connect(self.enable_clear_cache)
        self.ui.clear_cache.setEnabled(False)
        pool.start(runnable)

    def enable_clear_cache(self):
        """Enable the clear cache button."""
        self.ui.clear_cache.setEnabled(True)

    def get_microsoft_language(self):
        """Get the list of Microsoft languages."""
        try:
            file = PySide6.QtCore.QFile(":/binary/azure_translation.json")
            if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
                text = PySide6.QtCore.QTextStream(file).readAll()
                language_azure_list = json.loads(text.encode())
                file.close()
        except Exception as error:
            print(error)
            language_azure_list = {}
        self.language_azure_list = {}
        for value in language_azure_list:
            self.language_azure_list[language_azure_list[value]["name"]] = value
        return self.language_azure_list

    def set_translate_dropdown(self, source):
        """Set the translation dropdown values."""
        try:
            lang = [key for key, value in source.items() if value == self.startLang]
            if len(lang) > 0:
                lang = lang[0]
                self.ui.comboBox_writeLang.setCurrentText(lang)

            lang = [key for key, value in source.items() if value == self.endLang]
            if len(lang) > 0:
                lang = lang[0]
                self.ui.comboBox_targetLang.setCurrentText(lang)
        except Exception as error:
            logging.error(f"Error setting current text; {error}", exc_info=False)

    def azure_validation(self):
        """Validate Azure credentials and generate voice models."""
        self.threadList.clear()
        self.generate_azure_voice_models()
        self.pool_starter()

    def google_validation(self):
        """Validate Google credentials and generate voice models."""
        self.threadList.clear()
        self.generate_google_voice_models()
        self.pool_starter()

    def load_voices(self):
        """Load voice models."""
        try:
            # Load Azure voices
            key = os.environ.get('MICROSOFT_TOKEN', '')
            region = os.environ.get('MICROSOFT_REGION', '')
            if key and region:
                client = MicrosoftClient(credentials=(key, region))
                tts = MicrosoftTTS(client)
                voices = tts.get_voices()  
                for voice in voices:
                    self.load_azure_items(voices.index(voice), voice, len(voices))

            # Load Google voices
            google_creds_json = os.environ.get('GOOGLE_CREDS_JSON')
            if google_creds_json:
                temp_creds = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
                temp_creds.write(base64.b64decode(google_creds_json))
                temp_creds.close()
                client = GoogleTransClient()
                tts = GoogleTransTTS(client)
                voices = tts.get_voices()  
                for voice in voices:
                    self.load_google_items(voices.index(voice), voice, len(voices))

            # Load Sherpa-ONNX voices
            sherpa_manager = SherpaOnnxManager()
            available_models = sherpa_manager.models
            installed_models = sherpa_manager.get_installed_models()
            for i, model in enumerate(available_models):
                voice = {
                    "name": model["name"],
                    "description": model["description"],
                    "size": model["size"],
                    "installed": model["name"].lower().replace(" ", "_") in installed_models,
                    "toolTip": model["name"].lower().replace(" ", "_"),
                    "text": model["name"],
                    "gender": "neutral",  
                    "id": model["name"].lower().replace(" ", "_"),
                    "locale": "en-US"
                }
                self.load_onnx_items(i, voice, len(available_models))

            # Load Google Translate voices
            # Since GoogleTransClient doesn't have list_voices, we'll use a predefined list
            voices = [
                {"name": "en", "text": "English", "gender": "neutral", "id": "en", "locale": "en-US"},
                {"name": "es", "text": "Spanish", "gender": "neutral", "id": "es", "locale": "es-ES"},
                {"name": "fr", "text": "French", "gender": "neutral", "id": "fr", "locale": "fr-FR"},
                {"name": "de", "text": "German", "gender": "neutral", "id": "de", "locale": "de-DE"},
                {"name": "it", "text": "Italian", "gender": "neutral", "id": "it", "locale": "it-IT"},
                {"name": "pt", "text": "Portuguese", "gender": "neutral", "id": "pt", "locale": "pt-PT"},
                {"name": "ru", "text": "Russian", "gender": "neutral", "id": "ru", "locale": "ru-RU"},
                {"name": "ja", "text": "Japanese", "gender": "neutral", "id": "ja", "locale": "ja-JP"},
                {"name": "ko", "text": "Korean", "gender": "neutral", "id": "ko", "locale": "ko-KR"},
                {"name": "zh", "text": "Chinese", "gender": "neutral", "id": "zh", "locale": "zh-CN"}
            ]
            for i, voice in enumerate(voices):
                self.load_google_trans_items(i, voice, len(voices))

        except Exception as e:
            logging.error(f"Error loading voices: {e}")


    def load_azure_items(self, index, data, count):
        try:
            self.ui.azure_progressBar.setValue((index + 1) * 100 / count)
            item_widget = QWidget()
            item_UI = Ui_item()
            item_UI.setupUi(item_widget)
            item_UI.name.setText(data["name"])
            font = QFont()
            font.setPointSize(14)  
            item_UI.name.setFont(font)
            item_UI.play.clicked.connect(self.preview_pressed)  
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            item.setToolTip(data["id"])
            self.ui.listWidget_voiceazure.addItem(item)
            self.ui.listWidget_voiceazure.setItemWidget(item, item_widget)
        except Exception as e:
            logging.error(f"Error loading Azure item: {e}")

    def load_google_items(self, index, data, count):
        try:
            self.ui.gTTS_progressBar.setValue((index + 1) * 100 / count)
            item_widget = QWidget()
            item_UI = Ui_item()
            item_UI.setupUi(item_widget)
            item_UI.name.setText(data["name"])
            font = QFont()
            font.setPointSize(14)  
            item_UI.name.setFont(font)
            item_UI.play.clicked.connect(self.preview_pressed)  
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            item.setToolTip(data["id"])
            self.ui.listWidget_voicegoogle.addItem(item)
            self.ui.listWidget_voicegoogle.setItemWidget(item, item_widget)
        except Exception as e:
            logging.error(f"Error loading Google item: {e}")

    def load_onnx_items(self, index, data, count):
        try:
            self.ui.onnx_progressBar.setValue((index + 1) * 100 / count)
            item_widget = QWidget()
            item_UI = Ui_item()
            item_UI.setupUi(item_widget)
            item_UI.name.setText(data["name"])
            font = QFont()
            font.setPointSize(14)  
            item_UI.name.setFont(font)
            if data.get("downloaded", False):
                item_UI.play.setIcon(self.iconPlayed)  
                item_UI.play.clicked.connect(self.preview_pressed)
            else:
                item_UI.play.setIcon(self.iconDownload)  
                item_UI.play.clicked.connect(self.preview_pressed)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            item.setToolTip(data["id"])
            self.ui.onnx_listWidget.addItem(item)
            self.ui.onnx_listWidget.setItemWidget(item, item_widget)
        except Exception as e:
            logging.error(f"Error loading ONNX item: {e}")

    def load_google_trans_items(self, index, data, count):
        try:
            self.ui.googleTransTTS_progressBar.setValue((index + 1) * 100 / count)
            item_widget = QWidget()
            item_UI = Ui_item()
            item_UI.setupUi(item_widget)
            item_UI.name.setText(data["name"])
            font = QFont()
            font.setPointSize(14)  
            item_UI.name.setFont(font)
            item_UI.play.clicked.connect(self.preview_pressed)  
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            item.setToolTip(data["id"])
            self.ui.listWidget_voicegoogleTrans.addItem(item)
            self.ui.listWidget_voicegoogleTrans.setItemWidget(item, item_widget)
        except Exception as e:
            logging.error(f"Error loading Google Translate item: {e}")

    def on_search_changed(self, text, provider):
        """Handler for search box text changes"""
        print(f"Search changed handler called - Provider: {provider}, Text: '{text}'")  # Immediate feedback
        logging.debug(f"Search changed handler called - Provider: {provider}, Text: '{text}'")
        if provider == "azure":
            self.filter_azure_voices()
        elif provider == "google":
            self.filter_google_voices()
        elif provider == "onnx":
            self.filter_onnx_voices()
        elif provider == "google_trans":
            self.filter_google_trans_voices()

    def on_search_return(self, provider):
        """Handler for search box return pressed"""
        print(f"Search return pressed for {provider}")  # Immediate feedback
        logging.debug(f"Search return pressed for {provider}")
        if provider == "azure":
            self.filter_azure_voices()
        elif provider == "google":
            self.filter_google_voices()
        elif provider == "onnx":
            self.filter_onnx_voices()
        elif provider == "google_trans":
            self.filter_google_trans_voices()

    def start_download(self, voice_id, button, container_widget):
        """Start voice download process with visual feedback"""
        if voice_id in self.active_downloads:
            return  # Download already in progress
            
        # Hide download button and show spinner
        button.setVisible(False)
        spinner_label = QLabel()
        spinner_label.setMovie(self.spinner)
        container_widget.layout().addWidget(spinner_label)
        self.spinner.start()
        
        # Track this download
        self.active_downloads[voice_id] = {
            'button': button,
            'spinner': spinner_label,
            'container': container_widget
        }
        
        # Start download in background thread
        download_thread = Thread(target=self.download_voice_thread, args=(voice_id,))
        download_thread.daemon = True
        download_thread.start()
        
    def download_voice_thread(self, voice_id):
        """Handle voice download in background thread"""
        try:
            # Verify client is initialized
            if not self.sherpa_client:
                raise Exception("Sherpa TTS client not initialized")
            
            # Use client's method
            success = self.sherpa_client.check_and_download_model(voice_id)
            
            # Update UI in main thread
            QMetaObject.invokeMethod(self, "download_complete", 
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, voice_id),
                Q_ARG(bool, success))
                
        except Exception as e:
            logging.error(f"Error downloading voice {voice_id}: {e}")
            # Update UI in main thread to show error
            QMetaObject.invokeMethod(self, "download_complete", 
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, voice_id),
                Q_ARG(bool, False))

    @Slot(str, bool)
    def download_complete(self, voice_id, success):
        """Handle download completion in main thread"""
        if voice_id not in self.active_downloads:
            return
            
        download_info = self.active_downloads[voice_id]
        button = download_info['button']
        spinner = download_info['spinner']
        container = download_info['container']
        
        # Remove spinner
        self.spinner.stop()
        spinner.setParent(None)
        spinner.deleteLater()
        
        if success:
            # Add tick icon
            tick_label = QLabel()
            tick_label.setPixmap(self.iconTick.pixmap(16, 16))
            container.layout().addWidget(tick_label)
        else:
            # Show download button again on failure
            button.setVisible(True)
            
        # Clean up tracking
        del self.active_downloads[voice_id]


class Signals(QObject):
    started = Signal()
    completed = Signal()
    thread_completed = Signal(object)
    itemGenerated = Signal(int, dict, int)
    voicesFetched = Signal(list)
    errorDetected = Signal(str, str)
    download_progress = Signal(str, float)  


class Player(QRunnable):

    def __init__(self, file):
        super().__init__()
        self.temp_config_file = file
        self.signals = Signals()

    def run(self):
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
            exe_name = ""
            for root, dirs, files in os.walk(application_path):
                for file in files:
                    if "client.exe" in file:
                        exe_name = file
            GUI_path = os.path.join(application_path, exe_name)
            # Use subprocess.Popen to run the executable
            cache_location = os.path.join(
                os.path.dirname(self.temp_config_file.name), "Audio Files"
            )
            process = subprocess.Popen(
                [GUI_path, "--config", self.temp_config_file.name, "--preview"]
            )
            process.wait()
        elif __file__:
            application_path = os.path.dirname(os.path.dirname(__file__))
            # TODO: GUI_script_path get the upper directory where translatepb.py is located
            GUI_script_path = os.path.join(application_path, "client.py")
            print(GUI_script_path)
            cache_location = os.path.join(
                os.path.dirname(self.temp_config_file.name), "Audio Files"
            )
            process = subprocess.Popen(
                [
                    f"{application_path}/venv/Scripts/python.exe",
                    GUI_script_path,
                    "--config",
                    self.temp_config_file.name,
                    "--preview",
                ]
            )
            process.wait()
        self.signals.completed.emit()


class Cleaner(QRunnable):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.signals = Signals()

    def run(self):
        try:
            files = os.listdir(self.path)
            for file in files:
                file_path = os.path.join(self.path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"{file_path} is deleted.")
            print("All files deleted successfully.")
        except OSError:
            logging.error("Error occurred while deleting files.", exc_info=True)
        self.signals.completed.emit()


class VoiceLoader(QRunnable):
    """A class to load voice models asynchronously."""
    def __init__(self, widget, tts=None):
        super().__init__()
        self.widget = widget
        self.tts = tts

    def run(self):
        """Run the voice loading process."""
        try:
            self.widget.load_voices()
        except Exception as e:
            logging.error(f"Voice loading error: {e}")


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
    log_file = os.path.join(log_dir, "configure.log")

    # Create formatters and handlers
    file_formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
    )
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add our handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Log startup information
    logging.info("Starting AACSpeakHelper")
    logging.info(f"Log file location: {log_file}")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Operating system: {platform.platform()}")
    
    return log_file


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        widget = Widget()
        widget.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Application error: {e}")
        raise

class SherpaOnnxTTS(TTS):
    def __init__(self, model_dir=None, data_dir=None, **kwargs):
        super().__init__(**kwargs)
        
        self.model_dir = Path(model_dir or "./sherpa_models")
        self.data_dir = Path(data_dir or "~/AACSpeakHelper/sherpa_tts").expanduser()
        
        self._verify_model_files()
        self.client = self._create_client()

    def _verify_model_files(self):
        required_files = {'model.onnx', 'tokens.txt', 'lexicon.txt'}
        existing_files = {f.name for f in self.model_dir.glob('*')}
        
        if missing := required_files - existing_files:
            logging.warning(f"Missing model files: {missing}. Attempting download...")
            self._download_base_model()
            
    def _download_base_model(self):
        try:
            from sherpa_onnx import download_model
            download_model(
                model='sherpa_onnx_tts_model',
                repo_id='AACSpeakHelper/sherpa-models',
                dest_dir=str(self.model_dir)
            )
            logging.info("Base model downloaded successfully")
        except Exception as e:
            logging.error(f"Model download failed: {e}")
            raise TTSInitializationError("Failed to download required model files")
            
    def _create_client(self):
        from sherpa_onnx import SherpaOnnxOfflineTts
        return SherpaOnnxOfflineTts(
            model=str(self.model_dir),
            data_dir=str(self.data_dir),
            debug=self.debug
        )

    def get_available_voices(self):
        return self.client.list_voices()

    def download_voice(self, voice_id, progress_callback=None):
        if not self.client:
            raise TTSNotInitializedError()
            
        return self.client.download_model(
            voice_id=voice_id,
            progress_handler=progress_callback,
            tts_model_dir=self.data_dir
        )