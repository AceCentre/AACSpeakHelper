import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from utils import configure_app, config, args
import logging
import pyperclip
import pyttsx3
import easygui
import pygame
from tts_utils import speak

pygame.mixer.init()


def translatepb():
    try:
        from translate import Translator
        translator = Translator(to_lang=config.get(
            'translate', 'endLang'), from_lang=config.get('translate', 'startLang'))
        translation = translator.translate(pyperclip.paste())
        logging.info('Clipboard [{}]: {}'.format(config.get('translate', 'startLang'), pyperclip.paste()))
        logging.info('Translation [{}]: {}'.format(config.get('translate', 'endLang'), translation))
        return translation
    except Exception as e:
        logging.error("Translation Error!", exc_info=True)


def mainrun(listvoices: bool):
    if listvoices:
        try:
            # Code that may raise an exception
            engine = pyttsx3.init(config.get('TTS', 'engine'))
        except Exception as e:
            # Code to handle other exceptions
            logging.error("List Voice Error!", exc_info=True)
            result = easygui.msgbox(
                str(e) + '\n\nlistvoices method not supported for specified TTS Engine.\n\n Do You want to open the '
                         'Configuration Setup?',
                'Error')
        else:
            # Code that will run if no exception is raised
            voices = engine.getProperty('voices')
            for voice in voices:
                print(voice)
        # finally:
        #     # Code that will run regardless of whether an exception occurred
    else:
        try:
            if config.getboolean('translate', 'noTranslate'):
                clipboard = pyperclip.paste()
            else:
                clipboard = translatepb()

            speak(clipboard)  # Good Morning

            if config.getboolean('translate', 'replacepb'):
                pyperclip.copy(clipboard)
        except Exception as e:
            logging.error("Configuration Error!", exc_info=True)
            result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
            if result:
                configure_app()
            else:
                return


if __name__ == '__main__':
    mainrun(args['listvoices'])
