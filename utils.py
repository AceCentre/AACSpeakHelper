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
from PySide6.QtGui import *


import pygame

app = QApplication(sys.argv)


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

    except Exception as e:
        print(str(e))


def msgbox(message: str, header: str, timeout: int = 10000):
    try:
        msgInstance = QMessageBox(None)
        msgInstance.setWindowTitle(header)
        msgInstance.setText(message)
        msgInstance.setStandardButtons(QMessageBox.StandardButton.Ok)
        timer = QTimer(None)
        timer.singleShot(timeout, lambda: msgInstance.button(QMessageBox.StandardButton.Ok).animateClick())
        return msgInstance.exec() == QMessageBox.StandardButton.Ok

    except Exception as e:
        print(str(e))


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
        print(GUI_script_path)
        process = subprocess.run(["python", GUI_script_path])


def get_paths(args: vars):
    if (args['config'] != '' and os.path.exists(args['config'])):
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
        print(config_path, audio_files_path)

    # Check if the directory already exists
    if not os.path.exists(audio_files_path):
        # Create the "Audio Files" directory
        os.makedirs(audio_files_path)

    # Check if the file already exists
    if not os.path.exists(config_path):
        msg = '\n\n Do You want to open the Configuration Setup?'
        # result = easygui.ynbox("settings.cfg file not found." + msg, 'Error')
        try:
            result = ynbox("settings.cfg file not found." + msg, 'Error')
            pass
        except Exception as e:
            pass
        if result:
            configure_app()
        else:
            msg = "\n\n Please Run 'Configure TranslateAndTTS executable' first."
            result = msgbox("settings.cfg file not found. " + msg, 'Error')
            sys.exit()

    return config_path, audio_files_path


def play_audio(audio_bytes: bytes):
    audio_stream = io.BytesIO(audio_bytes)
    # pygame.mixer.init()
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def save_audio(audio_bytes: bytes, format: str = 'wav'):
    # save to .wav file
    timestr = time.strftime("%Y%m%d-%H%M%S.")
    filename = os.path.join(audio_files_path, timestr + format)

    # Write the WAV bytes to the output file
    with open(filename, 'wb') as out_file:
        out_file.write(audio_bytes)


def get_uuid():
    try:
        # Code that may raise an exception
        id = uuid.UUID(config.get('App', 'uuid'))
    except Exception as e:
        # Code to handle other exceptions
        id = uuid.uuid4()
        config.set('App', 'uuid', str(id))
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    return str(id)


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
        # You can add further logic here if needed, such as logging the error or continuing the script
        pass


parser = argparse.ArgumentParser(
    description='Reads pasteboard. Translates it. Speaks it out. Or any variation of that')
parser.add_argument(
    '-c', '--config', help='Path to a defined config file', required=False, default='')
parser.add_argument(
    '-l', '--listvoices', help='List Voices to see whats available', required=False, default=False)
args = vars(parser.parse_args())
logging.info(str(args))
(config_path, audio_files_path) = get_paths(args=args)
config = configparser.ConfigParser()
current_path = os.path.dirname(config_path)
if os.path.isdir(current_path):
    # print(os.path.join(current_path, 'app.log'))
    logging.basicConfig(filename=os.path.join(current_path, 'app.log'),
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
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
    sys.exit()

if Allow_Collecting_Stats:
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
