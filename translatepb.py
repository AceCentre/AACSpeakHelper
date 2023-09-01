import os
import time
import asyncio
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from utils import configure_app, config, args
import utils
import logging
import pyperclip
import pyttsx3
import pygame
from tts_utils import speak
from translate import Translator

pygame.mixer.init()


def translatepb():
    try:

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


async def mainrun(listvoices: bool):
    if listvoices:
        try:
            # Code that may raise an exception
            engine = pyttsx3.init(config.get('TTS', 'engine'))
        except Exception as e:
            # Code to handle other exceptions
            logging.error("List Voice Error!", exc_info=True)
            result = utils.ynbox(
                str(e) + '\n\nlistvoices method not supported for specified TTS Engine.\n\n Do You want to open the '
                         'Configuration Setup?',
                'List Voice Error')
            if result:
                configure_app()
            else:
                return
        else:
            # Code that will run if no exception is raised
            voices = engine.getProperty('voices')
            for voice in voices:
                print(voice)
        # finally:
        #     # Code that will run regardless of whether an exception occurred
    else:
        try:
            start = time.perf_counter()
            if config.getboolean('translate', 'noTranslate'):
                clipboard = pyperclip.paste()
                stop = time.perf_counter() - start
                print(f"Clipboard runtime is {stop:0.2f} seconds.")
                logging.info(f"Clipboard runtime is {stop:0.2f} seconds.")
            else:
                clipboard = translatepb()
                stop = time.perf_counter() - start
                print(f"Clipboard[Translate] runtime is {stop:0.5f} seconds.")
                logging.info(f"Clipboard[Translate] runtime is {stop:0.5f} seconds.")
            start = time.perf_counter()
            speak(clipboard)  # Good Morning
            stop = time.perf_counter() - start
            print(f"TTS runtime is {stop:0.5f} seconds.")
            logging.info(f"TTS runtime is {stop:0.5f} seconds.")
            if config.getboolean('translate', 'replacepb'):
                pyperclip.copy(clipboard)
            logging.info("------------------------------------------------------------------------")
        except Exception as e:
            logging.error("Configuration ErrorL {}".format(e), exc_info=True)
            result = utils.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Runtime Error')
            if result:
                configure_app()
            else:
                return


async def remove_stale_temp_files(directory_path, ignore_pattern=".history"):
    start = time.perf_counter()
    current_time = time.time()
    time_threshold = current_time - 7 * 24 * 60 * 60
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if ignore_pattern and file.endswith(ignore_pattern):
                continue  # Ignore this file and move to the next iteration
            file_modification_time = os.path.getmtime(file_path)
            if file_modification_time < time_threshold:
                try:
                    os.remove(file_path)
                    print(f"Removed cache file: {file_path}")
                    logging.info(f"Removed cache file: {file_path}")
                except Exception as e:
                    print(f"Error removing file {file_path}: {e}")
                    logging.error(f"Removed cache file: {file_path}", exc_info=True)
    stop = time.perf_counter() - start
    print(f"Cache clearing runtime is {stop:0.5f} seconds.")
    logging.info(f"Cache clearing is {stop:0.5f} seconds.")


async def main(wav_files_path):
    await asyncio.gather(remove_stale_temp_files(wav_files_path, ".history"), mainrun(args['listvoices']))


if __name__ == '__main__':
    asyncio.run(main(utils.audio_files_path))


# if __name__ == '__main__':
#     mainrun(args['listvoices'])
