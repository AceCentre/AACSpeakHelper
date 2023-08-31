import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from utils import configure_app, config, args
import logging
import pyperclip
import pyttsx3
import easygui
import pygame
from tts_utils import speak
from translate import Translator
import translate

pygame.mixer.init()


def translatepb():
    try:

        print(translate.providers.__all__)
        provider = config.get('translate', 'provider')
        if provider == 'MyMemoryProvider':
            key = config.get('translate', 'mymemoryprovider_secret_key')
            email = config.get('translate', 'email')
            translator = Translator(to_lang=config.get('translate', 'endLang'),
                                    from_lang=config.get('translate', 'startLang'),
                                    provider='mymemory',
                                    secret_access_key=None if key == "" else key,
                                    email=None if email == "" else email)
            logging.info('Translation Provider is {}'.format(provider))
        elif provider == 'MicrosoftProvider':
            key = config.get('translate', 'microsoftprovider_secret_key')
            region = config.get('translate', 'region')
            translator = Translator(to_lang=config.get('translate', 'endLang'),
                                    from_lang=config.get('translate', 'startLang'),
                                    provider='microsoft',
                                    secret_access_key=None if key == "" else key,
                                    region=None if region == "" else region)
            logging.info('Translation Provider is {}'.format(provider))
        elif provider == 'DeeplProvider':
            key = config.get('translate', 'deeplprovider_secret_key')
            pro = config.getboolean('translate', 'deepl_pro')
            translator = Translator(to_lang=config.get('translate', 'endLang'),
                                    from_lang=config.get('translate', 'startLang'),
                                    provider='deepl',
                                    secret_access_key=None if key == "" else key,
                                    pro=False if pro == "" else pro)
            logging.info('Translation Provider is {}'.format(provider))
        elif provider == 'LibreProvider':
            key = config.get('translate', 'libreprovider_secret_key')
            url = config.get('translate', 'url')
            translator = Translator(to_lang=config.get('translate', 'endLang'),
                                    from_lang=config.get('translate', 'startLang'),
                                    provider='libre',
                                    secret_access_key=None if key == "" else key,
                                    base_url=None if url == "" else url)
            logging.info('Translation Provider is {}'.format(provider))
        # # else:
        # #     translator = Translator(to_lang=config.get('translate', 'endLang'),
        #                             from_lang=config.get('translate', 'startLang'))

        translation = translator.translate(pyperclip.paste())
        logging.info('Clipboard [{}]: {}'.format(config.get('translate', 'startLang'), pyperclip.paste()))
        logging.info('Translation [{}]: {}'.format(config.get('translate', 'endLang'), translation))
        return translation
    except Exception as e:
        logging.error("Translation Error: {}".format(e), exc_info=True)


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
            logging.error("Configuration ErrorL {}".format(e), exc_info=True)
            result = easygui.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Error')
            if result:
                configure_app()
            else:
                return


if __name__ == '__main__':
    mainrun(args['listvoices'])
