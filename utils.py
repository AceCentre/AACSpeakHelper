import logging
import os
import sys
import subprocess
import time
import io
import configparser
import uuid
import posthog
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sqlite3
from tts_wrapper import SherpaOnnxTTS
import wave
import pyaudio
import warnings
warnings.filterwarnings("ignore")
args = {'config': '', 'listvoices': False, 'preview': False, 'style': '', 'styledegree': None}
config_path = None
audio_files_path = None
config = None


def ynbox(message: str, header: str, timeout: int = 10000):
    try:

        ynInstance = QMessageBox(None)
        ynInstance.setWindowTitle(header)
        ynInstance.setText(message)
        ynInstance.setStandardButtons(QMessageBox.StandardButton.Yes)
        ynInstance.addButton(QMessageBox.StandardButton.No)
        timer = QTimer(None)
        timer.singleShot(timeout, lambda: ynInstance.button(QMessageBox.StandardButton.No).animateClick())
        return ynInstance.exec() == QMessageBox.StandardButton.Yes
    except Exception as error:
        logging.error("Message Error: {}".format(error), exc_info=True)


def msgbox(message: str, header: str, timeout: int = 10000):
    try:
        msgInstance = QMessageBox(None)
        msgInstance.setWindowTitle(header)
        msgInstance.setText(message)
        msgInstance.setStandardButtons(QMessageBox.StandardButton.Ok)
        timer = QTimer(None)
        timer.singleShot(timeout, lambda: msgInstance.button(QMessageBox.StandardButton.Ok).animateClick())
        return msgInstance.exec() == QMessageBox.StandardButton.Ok
    except Exception as error:
        logging.error("Message Error: {}".format(error), exc_info=True)


def configure_app():
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        exe_name = ""
        for root, dirs, files in os.walk(application_path):
            for file in files:
                if "Configure AACSpeakHelper" in file:
                    exe_name = file
        GUI_path = os.path.join(application_path, exe_name)
        # Use subprocess.Popen to run the executable
        process = subprocess.Popen(GUI_path)
        # Wait for the process to complete
        process.wait()
    elif __file__:
        application_path = os.path.dirname(__file__)
        GUI_script_path = os.path.join(application_path, 'GUI_TranslateAndTTS', 'widget.py')
        process = subprocess.run(["python", GUI_script_path])


def get_paths(config_path=None):
    if config_path and os.path.exists(config_path):
        audio_files_path = os.path.join(os.path.dirname(config_path), 'Audio Files')
    else:
        if getattr(sys, 'frozen', False):
            home_directory = os.path.expanduser("~")
            application_path = os.path.join(home_directory, 'AppData', 'Roaming', 'Ace Centre', 'AACSpeakHelper')
        else:
            application_path = os.path.dirname(__file__)

        audio_files_path = os.path.join(application_path, 'Audio Files')
        config_path = os.path.join(application_path, 'settings.cfg')

    # Ensure the audio files directory exists
    os.makedirs(audio_files_path, exist_ok=True)

    # Check if the file already exists - commenting this for now. 
    # if not os.path.exists(config_path):
    #     message = '\n\n Do You want to open the Configuration Setup?'
    #     try:
    #         result = ynbox("settings.cfg file not found." + message, 'Error')
    #         if result:
    #             configure_app()
    #         else:
    #             message = "\n\n Please Run 'Configure AACSpeakHelper executable' first."
    #             response = msgbox("settings.cfg file not found. " + message, 'Error')
    #             sys.exit(response)
    #     except Exception as error:
    #         logging.error("Configuration Error: {}".format(error), exc_info=True)

    return config_path, audio_files_path


def play_audio(audio_bytes, file: bool = False):
    if file:
        with wave.open(audio_bytes, 'rb') as wf:
            play_wave(wf)
    else:
        with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
            play_wave(wf)


def play_wave(wf):
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return data, pyaudio.paContinue

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        pass

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()


def save_audio(text: str, engine: str, file_format: str = 'wav', tts=None):
    timestr = time.strftime("%Y%m%d-%H%M%S.")
    filename = os.path.join(audio_files_path, timestr + file_format)
    tts.speak_streamed(text, save_to_file_path=filename, audio_format=file_format)
    sql = "INSERT INTO History(text, filename, engine) VALUES('{}','{}','{}')".format(text, filename, engine)
    try:
        connection = sqlite3.connect(os.path.join(audio_files_path, 'cache_history.db'))
        connection.execute(sql)
        connection.commit()
        connection.close()
    except Exception as error:
        logging.error("Database Error: {}".format(error), exc_info=True)


def get_uuid():
    try:
        # Note: Remove uuid config every commit
        # Code will raise an exception at first run due to blank uuid
        identifier = uuid.UUID(config.get('App', 'uuid'))
    except Exception as error:
        identifier = uuid.uuid4()
        config.set('App', 'uuid', str(identifier))
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        logging.error("Failed to get uuid: {}".format(error), exc_info=True)
    logging.info("uuid: {}".format(identifier), exc_info=True)
    return str(identifier)


def notify_posthog(id: str, event_name: str, properties: dict = {}):
    try:
        posthog_client = posthog.Posthog(project_api_key='phc_q37FBcmTQD1hHtNBgqvs9wid45gKjGKEJGduRkPog0t',
                                         host='https://app.posthog.com')
        # Attempt to send the event to PostHog
        posthog_client.capture(distinct_id=id, event=event_name, properties=properties)
        print(f"[notify-posthog] Event '{event_name}' captured successfully!")
    except Exception as e:
        # Handle the case when there's an issue with sending the event
        print(f"[notify-posthog] Failed to capture event '{event_name}': {e}")
        logging.error("[notify-posthog] Failed to capture event '{}': {}".format(event_name, e), exc_info=True)
        # You can add further logic here if needed, such as logging the error or continuing the script
        pass


def check_history(text: str):
    try:
        if args['style']:
            return None
        if os.path.isfile(os.path.join(audio_files_path, 'cache_history.db')):
            sql = "SELECT filename FROM History WHERE text='{}'".format(text)
            connection = sqlite3.connect(os.path.join(audio_files_path, 'cache_history.db'))
            cursor = connection.execute(sql)
            results = cursor.fetchone()
            base_name = results[0] if results is not None else None
            if base_name is not None:
                file = os.path.join(audio_files_path, base_name)
                connection.close()
                return file
            else:
                return None
        else:
            create_Database()
            return None
    except Exception as error:
        logging.error("Failed to connect to database: ".format(error), exc_info=True)
        return None


def clear_history(files: list):
    try:
        if os.path.isfile(os.path.join(audio_files_path, 'cache_history.db')) and len(files) > 0:
            connection = sqlite3.connect(os.path.join(audio_files_path, 'cache_history.db'))
            for file in files:
                sql = "DELETE FROM History WHERE filename='{}'".format(file)
                connection.execute(sql)
            connection.commit()
            connection.close()
    except Exception as error:
        logging.error("Failed to connect to database: ".format(error), exc_info=True)
        return None


def create_Database():
    try:
        if not os.path.isfile(os.path.join(audio_files_path, 'cache_history.db')):
            sql1 = """CREATE TABLE IF NOT EXISTS "History" ("id"	INTEGER NOT NULL UNIQUE,
                                                            "text"	TEXT NOT NULL,
                                                            "filename"	TEXT NOT NULL,
                                                            "engine"	TEXT NOT NULL,
                                                            UNIQUE("id"),
                                                            PRIMARY KEY("id" AUTOINCREMENT));"""
            sql2 = """CREATE UNIQUE INDEX IF NOT EXISTS "id_text" ON "History" ("text");"""
            connection = sqlite3.connect(os.path.join(audio_files_path, 'cache_history.db'))
            connection.execute(sql1)
            connection.execute(sql2)
            connection.close()
            logging.info("Cache database is created.")
        else:
            logging.info("Cache database is found")
    except Exception as error:
        logging.error("Failed to create database: ".format(error), exc_info=True)


def update_Database(file):
    try:
        if not os.path.isfile(os.path.join(audio_files_path, 'cache_history.db')):
            pass
        else:
            logging.info("Cache database is found: ")
    except Exception as error:
        logging.error("Failed to update database: ".format(error), exc_info=True)


def init(input_config, args=args):
    global config_path
    global audio_files_path
    global config

    config_path = input_config['App']['config_path']
    audio_files_path = input_config['App']['audio_files_path']
    config = input_config  # This assigns the passed config to the global config variable

    logging.info(f"Initialized utils with config path: {config_path}")
    logging.info(f"Audio files path: {audio_files_path}")

    # Dropping. this init now takes in a config object.. checking. msg = "\n\n Please Run 'Configure AACSpeakHelper executable' first."
    #            result = msgbox("settings.cfg file not found. " + msg, 'Error')
    #            sys.exit()

    if config.getboolean('App', 'collectstats'):
        distinct_id = get_uuid()
        event_name = 'App Run'
        event_properties = {
            'uuid': distinct_id,
            'source': 'helperApp',
            'version': 2.3,
            'fromLang': config.get('translate', 'startlang'),
            'toLang': config.get('translate', 'endlang'),
            'ttsengine': config.get('TTS', 'engine'),
        }
        notify_posthog(distinct_id, event_name, event_properties)
