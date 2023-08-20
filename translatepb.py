import pyperclip
import pyttsx4
import configparser
import os
import translate
import sys
import argparse
import time
from aspeak import SpeechService, AudioFormat
import easygui





parser = argparse.ArgumentParser(
    description='Reads pasteboard. Translates it. Speaks it out. Or any variation of that')
parser.add_argument(
    '-c', '--config', help='Path to a defined config file', required=False, default='')
parser.add_argument(
    '-l', '--listvoices', help='List Voices to see whats available', required=False, default=False)
args = vars(parser.parse_args())

if (args['config'] != '' and os.path.exists(args['config'])):
    config_path = args['config']
else:
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        # Get the path to the user's app data folder
        home_directory = os.path.expanduser("~")
        application_path = os.path.join(home_directory, 'AppData', 'Roaming', '.TranslateAndTTS')

    elif __file__:
        application_path = os.path.dirname(__file__)

    wav_files_path = os.path.join(application_path, 'WAV Files')
    # Check if the directory already exists
    if not os.path.exists(wav_files_path):
        # Create the "WAV Files" directory
        os.makedirs(wav_files_path)

    config_path = os.path.join(application_path, 'settings.cfg')

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
    if (ttsengine == 'gTTS'):
        from gspeak import speak
        speak(text, lang=config.get('translate', 'endLang').lower())
    if (ttsengine == 'azureTTS'):
        azureSpeak(text, lang=config.get('translate', 'endLang').lower(),)
    else:
        engine = pyttsx4.init(ttsengine)
        engine.setProperty('voice', config.get('TTS', 'voiceid'))
        engine.setProperty('rate', config.get('TTS', 'rate'))
        engine.setProperty('volume', config.get('TTS', 'volume'))
        engine.say(text)
        engine.runAndWait()

def mainrun(listvoices):
    if (listvoices == True):
        try:
            # Code that may raise an exception
            engine = pyttsx4.init(config.get('TTS', 'engine'))
        except Exception as e:
            # Code to handle other exceptions
            print ("listvoices method not supported for specified TTS Engine.")
        else:
            # Code that will run if no exception is raised
            voices = engine.getProperty('voices')
            for voice in voices:
                print(voice)
        # finally:
        #     # Code that will run regardless of whether an exception occurred
    else:
        if (config.getboolean('translate', 'noTranslate')):
            newstr = pyperclip.paste()
        else:
            newstr = translatepb()
            speakstr(newstr)
        if (config.getboolean('translate', 'replacepb')):
            pyperclip.copy(newstr)

def azureSpeak(text, lang):
    try:
        # Add your key and endpoint
        key = config.get('azureTTS', 'key')
        location = config.get('azureTTS', 'location')
        voiceid = config.get('azureTTS', 'voiceid')
        service = SpeechService(AudioFormat.Riff24Khz16BitMonoPcm, region=location, key=key)
        service.speak_text(text, voice=voiceid)
        print("Speech synthesized for text [{}]".format(text))
    except Exception as e:
        result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
        if result == True:
            easygui.msgbox('In Milestone 2')
        else:
            return
    else:
        try:
            save_to_wav = bool(config.get('azureTTS', 'save_to_wav'))
        except Exception as e:
            pass
        else:
            if save_to_wav:
                # save to .wav file
                timestr = time.strftime("%Y%m%d-%H%M%S")
                filename = os.path.join(wav_files_path, timestr+'.wav')
                try:
                    service.synthesize_text(text, output=filename, voice=voiceid)
                except Exception as e:
                    result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
                    if result == True:
                        easygui.msgbox('In Milestone 2')

    # What a beautiful day today!

    

if __name__ == '__main__':
    mainrun(args['listvoices'])
