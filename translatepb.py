import pyperclip
import pyttsx4
import configparser
import os
import sys
import argparse
import time
import easygui
import pygame
import io
from tts_wrapper import MicrosoftClient, MicrosoftTTS
from tts_wrapper import GoogleClient, GoogleTTS
from tts_wrapper import SAPIClient, SAPITTS

def configure_app():
    import subprocess
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

parser = argparse.ArgumentParser(
    description='Reads pasteboard. Translates it. Speaks it out. Or any variation of that')
parser.add_argument(
    '-c', '--config', help='Path to a defined config file', required=False, default='')
parser.add_argument(
    '-l', '--listvoices', help='List Voices to see whats available', required=False, default=False)
args = vars(parser.parse_args())

pygame.mixer.init()

if (args['config'] != '' and os.path.exists(args['config'])):
    config_path = args['config']
    wav_files_path = os.path.join(os.path.dirname(config_path), 'WAV Files')
    # Check if the directory already exists
    if not os.path.exists(wav_files_path):
        # Create the "WAV Files" directory
        os.makedirs(wav_files_path)
    print(wav_files_path)
else:
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        # Get the path to the user's app data folder
        home_directory = os.path.expanduser("~")
        application_path = os.path.join(home_directory, 'AppData', 'Roaming', 'TranslateAndTTS')

    elif __file__:
        application_path = os.path.dirname(__file__)

    wav_files_path = os.path.join(application_path, 'WAV Files')
    # Check if the directory already exists
    if not os.path.exists(wav_files_path):
        # Create the "WAV Files" directory
        os.makedirs(wav_files_path)

    config_path = os.path.join(application_path, 'settings.cfg')


# Check if the file already exists
if not os.path.exists(config_path):
    result = easygui.ynbox("settings.cfg file not found." + '\n\n Do You want to open the Configuration Setup?', 'Error')
    if result == True:
        configure_app()
    else:
        result = easygui.msgbox("settings.cfg file not found. \n\n Please Run 'Configure TranslateAndTTS executable' first.", 'Error')
        sys.exit()

config = configparser.ConfigParser()
config.read(config_path)

def translatepb():
    from translate import Translator
    translator = Translator(to_lang=config.get(
        'translate', 'endLang'), from_lang=config.get('translate', 'startLang'))
    translation = translator.translate(pyperclip.paste())
    return translation


def speakstr(text=''):
    ttsengine = config.get('TTS', 'engine')
    if (ttsengine == 'gspeak'):
        from gspeak import speak
        speak(text, lang=config.get('translate', 'endLang').lower())
    elif (ttsengine == 'azureTTS'):
        azureSpeak(text)
    elif (ttsengine == 'gTTS'):
        googleSpeak(text)
    elif (ttsengine == 'sapi5'):
        sapiSpeak(text)
    else: # Unsupported Engines
        engine = pyttsx4.init(ttsengine)
        engine.setProperty('voice', config.get('TTS', 'voiceid'))
        engine.setProperty('rate', config.get('TTS', 'rate'))
        engine.setProperty('volume', config.get('TTS', 'volume'))
        engine.say(text)
        engine.runAndWait()


def mainrun(listvoices):
    # listvoices = True
    if (listvoices == True):
        try:
            # Code that may raise an exception
            engine = pyttsx4.init(config.get('TTS', 'engine'))
        except Exception as e:
            # Code to handle other exceptions
            result = easygui.msgbox(str(e) + '\n\nlistvoices method not supported for specified TTS Engine.\n\n Do You want to open the Configuration Setup?', 'Error')
            print ("listvoices method not supported for specified TTS Engine.")
        else:
            # Code that will run if no exception is raised
            voices = engine.getProperty('voices')
            for voice in voices:
                print(voice)
        # finally:
        #     # Code that will run regardless of whether an exception occurred
    else:
        try:
            if (config.getboolean('translate', 'noTranslate')):
                newstr = pyperclip.paste()
            else:
                newstr = translatepb()
                speakstr(newstr)
            if (config.getboolean('translate', 'replacepb')):
                pyperclip.copy(newstr)
        except Exception as e:
            result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
            if result == True:
                configure_app()
            else:
                return

def azureSpeak(text):
    try:
        # Add your key and endpoint
        key = config.get('azureTTS', 'key')
        location = config.get('azureTTS', 'location')
        voiceid = config.get('azureTTS', 'voiceid')
        save_to_wav = bool(config.get('TTS', 'save_to_wav'))

        client = MicrosoftClient(credentials=key, region=location)
        tts = MicrosoftTTS(client=client, voice=voiceid)

        ttsWrapperSpeak(text, tts, save_to_wav)

    except Exception as e:
        result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
        if result == True:
            configure_app()
        else:
            return
        
def googleSpeak(text):
    try:
        # Add your key and endpoint
        creds_file = config.get('googleTTS', 'creds_file')
        voiceid = config.get('googleTTS', 'voiceid')
        save_to_wav = bool(config.get('TTS', 'save_to_wav'))

        client = GoogleClient(credentials=creds_file)
        tts = GoogleTTS(client=client, voice=voiceid)
        ttsWrapperSpeak(text, tts, save_to_wav)
    except Exception as e:
        result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
        if result == True:
            configure_app()
        else:
            return

def sapiSpeak(text):
    try:
        # Add your key and endpoint
        voiceid = config.get('sapi5TTS', 'voiceid')
        save_to_wav = bool(config.get('TTS', 'save_to_wav'))
        
        
        client = SAPIClient()
        client._client.setProperty('voice', voiceid)
        client._client.setProperty('rate', config.get('TTS', 'rate'))
        client._client.setProperty('volume', config.get('TTS', 'volume'))
        tts = SAPITTS(client=client)
        ttsWrapperSpeak(text, tts, save_to_wav)
    except Exception as e:
        result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
        if result == True:
            configure_app()
        else:
            return


def ttsWrapperSpeak(text, tts, save_to_wav):
    try:
        if isinstance(tts, SAPITTS):
            wav_bytes = tts.synth_to_bytes(text, 'wav')
        else:
            wav_bytes = tts.synth_to_bytes(tts.ssml.add(text), 'wav')

        play_wav(wav_bytes=wav_bytes)
        print("Speech synthesized for text [{}]".format(text))
    except Exception as e:
        result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
        if result == True:
            configure_app()
        else:
            return
    else:
        if save_to_wav:
            try:
                save_wav(wav_bytes=wav_bytes)
            except Exception as e:
                result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
                if result == True:
                    configure_app()
    # What a beautiful day today!

def play_wav(wav_bytes):
    wav_stream = io.BytesIO(wav_bytes)
    # pygame.mixer.init()
    pygame.mixer.music.load(wav_stream)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def save_wav(wav_bytes):
    # save to .wav file
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(wav_files_path, timestr+'.wav')

    # Write the WAV bytes to the output file
    with open(filename, 'wb') as out_file:
        out_file.write(wav_bytes)


if __name__ == '__main__':
    mainrun(args['listvoices'])
