import pyperclip
import pyttsx3
import easygui
import pygame

from utils import configure_app, config, args
from tts_utils import speak

pygame.mixer.init()

def translatepb():
    from translate import Translator
    translator = Translator(to_lang=config.get(
        'translate', 'endLang'), from_lang=config.get('translate', 'startLang'))
    translation = translator.translate(pyperclip.paste())
    return translation

def mainrun(listvoices : bool):
    if listvoices:
        try:
            # Code that may raise an exception
            engine = pyttsx3.init(config.get('TTS', 'engine'))
        except Exception as e:
            # Code to handle other exceptions
            result = easygui.msgbox(str(e) + '\n\nlistvoices method not supported for specified TTS Engine.\n\n Do You want to open the Configuration Setup?', 'Error')
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

            speak(newstr) # Good Morning

            if (config.getboolean('translate', 'replacepb')):
                pyperclip.copy(newstr)
        except Exception as e:
            result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
            if result == True:
                configure_app()
            else:
                return
            
if __name__ == '__main__':
    mainrun(args['listvoices'])