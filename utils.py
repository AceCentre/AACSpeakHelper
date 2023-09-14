import logging
import os
import sys
import subprocess
import time
import io
import argparse
import configparser
import uuid
import posthog
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sqlite3

# Hide Pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.mixer.init()


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
                if "Configure TranslateAndTTS" in file:
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


def get_paths(args: vars):
    if args['config'] != '' and os.path.exists(args['config']):
        config_path = args['config']
        audio_files_path = os.path.join(os.path.dirname(config_path), 'WAV Files')
    else:
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            # Get the path to the user's app data folder
            home_directory = os.path.expanduser("~")
            application_path = os.path.join(home_directory, 'AppData', 'Roaming', 'TranslateAndTTS')

        elif __file__:
            application_path = os.path.dirname(__file__)
        audio_files_path = os.path.join(application_path, 'Audio Files')
        config_path = os.path.join(application_path, 'settings.cfg')
    # Check if the directory already exists
    if not os.path.exists(audio_files_path):
        # Create the "Audio Files" directory
        os.makedirs(audio_files_path)

    # Check if the file already exists
    if not os.path.exists(config_path):
        message = '\n\n Do You want to open the Configuration Setup?'
        try:
            result = ynbox("settings.cfg file not found." + message, 'Error')
            if result:
                configure_app()
            else:
                message = "\n\n Please Run 'Configure TranslateAndTTS executable' first."
                response = msgbox("settings.cfg file not found. " + message, 'Error')
                sys.exit(response)
        except Exception as error:
            logging.error("Configuration Error: {}".format(error), exc_info=True)

    return config_path, audio_files_path


def play_audio(audio_bytes, file: bool = False):
    if file:
        audio_stream = audio_bytes
    else:
        audio_stream = io.BytesIO(audio_bytes)
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def save_audio(audio_bytes: bytes, text: str, engine: str, format: str = 'wav'):
    timestr = time.strftime("%Y%m%d-%H%M%S.")
    filename = os.path.join(audio_files_path, timestr + format)
    sql = "INSERT INTO History(text, filename, engine) VALUES('{}','{}','{}')".format(text, timestr + format, engine)
    with open(filename, 'wb') as out_file:
        out_file.write(audio_bytes)
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
        posthog_client = posthog.Posthog(project_api_key='phc_L5wgGTFZYVC1q8Hk7Qu0dp3YKuU1OUPSPGAx7kADWcs',
                                         host='https://app.posthog.com')
        # Attempt to send the event to PostHog
        posthog_client.capture(distinct_id=id, event=event_name, properties=properties)
        print(f"Event '{event_name}' captured successfully!")
    except Exception as e:
        # Handle the case when there's an issue with sending the event
        print(f"Failed to capture event '{event_name}': {e}")
        logging.error("Failed to capture event '{}': {}".format(event_name, e), exc_info=True)
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


parser = argparse.ArgumentParser(
    description='Reads pasteboard. Translates it. Speaks it out. Or any variation of that')
parser.add_argument(
    '-c', '--config', help='Path to a defined config file', required=False, default='')
parser.add_argument(
    '-l', '--listvoices', help='List Voices to see whats available', required=False, default=False, action="store_true")
parser.add_argument(
    '-p', '--preview', help='Preview Only', required=False, default=False, action="store_true")
parser.add_argument(
    '-s', '--style', help='Voice style for Azure TTS', required=False, default='')
parser.add_argument(
    '-sd', '--styledegree', type=float, help='Degree of style for Azure TTS', required=False, default=None)
args = vars(parser.parse_args())
logging.info(str(args))
(config_path, audio_files_path) = get_paths(args=args)
config = configparser.ConfigParser()
current_path = os.path.dirname(config_path)

# Need to set initial path if no config file was found.
if os.path.isdir(current_path):
    logging.basicConfig(filename=os.path.join(current_path, 'app.log'),
                        filemode='a',
                        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
                        level=logging.DEBUG,
                        force=True)
try:
    # print(config_path)

    if os.path.isfile(config_path):
        config.read(config_path)
        Allow_Collecting_Stats = config.getboolean('App', 'collectstats')
    else:
        msg = "\n\n Please Run 'Configure TranslateAndTTS executable' first."
        result = msgbox("settings.cfg file not found. " + msg, 'Error')
        sys.exit()
except Exception as e:
    logging.error("Configuration Error {}".format(e), exc_info=True)
    sys.exit()

if Allow_Collecting_Stats:
    start = time.perf_counter()
    distinct_id = get_uuid()
    event_name = 'App Run'
    event_properties = {
        'uuid': distinct_id,
        'source': 'app',
        'fromLang': config.get('translate', 'startlang'),
        'toLang': config.get('translate', 'endlang'),
        'ttsengine': config.get('TTS', 'engine'),
    }

    notify_posthog(distinct_id, event_name, event_properties)
    stop = time.perf_counter() - start
    print(f"Posthog runtime is {stop:0.5f} seconds.")
    logging.info(f"Posthog runtime is {stop:0.5f} seconds.")
