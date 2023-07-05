import pyperclip
import pyttsx4
import configparser
import os
import translate
import sys
import argparse

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
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
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
    else:
        engine = pyttsx4.init(ttsengine)
        engine.setProperty('voice', config.get('TTS', 'voiceid'))
        engine.setProperty('rate', config.get('TTS', 'rate'))
        engine.setProperty('volume', config.get('TTS', 'volume'))
        engine.say(text)
        engine.runAndWait()


def mainrun(listvoices):
    if (listvoices == True):
        engine = pyttsx4.init(config.get('TTS', 'engine'))
        voices = engine.getProperty('voices')
        for voice in voices:
            print(voice)
    else:
        if (config.getboolean('translate', 'noTranslate')):
            newstr = pyperclip.paste()
        else:
            newstr = translatepb()
            speakstr(newstr)
        if (config.getboolean('translate', 'replacepb')):
            pyperclip.copy(newstr)


if __name__ == '__main__':
    mainrun(args['listvoices'])
