import os
import sys
import time
import asyncio
from utils import configure_app, config, args, clear_history
import utils
import logging
import pyperclip
import pyttsx3
from tts_utils import speak
from GUI_TranslateAndTTS.language_dictionary import *
from PySide6.QtWidgets import *
from deep_translator import *


def translate_clipboard():
    try:
        translator = config.get('translate', 'provider')
        key = config.get('translate', f'{translator}_secret_key') if not translator == "GoogleTranslator" else None
        email = config.get('translate', 'email') if translator == 'MyMemoryTranslator' else None
        region = config.get('translate', 'region') if translator == 'MicrosoftTranslator' else None
        pro = config.getboolean('translate', 'deepl_pro') if translator == 'DeeplTranslator' else None
        url = config.get('translate', 'url') if translator == 'LibreProvider' else None
        client_id = config.get('translate', 'papagotranslator_client_id') if translator == 'PapagoTranslator' else None
        appid = config.get('translate', 'baidutranslator_appid') if translator == 'BaiduTranslator' else None
        if translator == "GoogleTranslator":
            translate_instance = GoogleTranslator(source='auto', target=config.get('translate', 'endLang'))
        elif translator == "PonsTranslator":
            translate_instance = PonsTranslator(source='auto', target=config.get('translate', 'endLang'))
        elif translator == "LingueeTranslator":
            translate_instance = LingueeTranslator(source='auto', target=config.get('translate', 'endLang'))
        elif translator == "MyMemoryTranslator":
            translate_instance = MyMemoryTranslator(source=config.get('translate', 'startLang'),
                                                    target=config.get('translate', 'endLang'),
                                                    email=email)
        elif translator == "YandexTranslator":
            translate_instance = YandexTranslator(source=config.get('translate', 'startLang'),
                                                  target=config.get('translate', 'endLang'),
                                                  api_key=key)
        elif translator == "MicrosoftTranslator":
            translate_instance = MicrosoftTranslator(api_key=key,
                                                     source=config.get('translate', 'startLang'),
                                                     target=config.get('translate', 'endLang'),
                                                     region=region)
        elif translator == "QcriTranslator":
            translate_instance = QcriTranslator(source='auto',
                                                target=config.get('translate', 'endLang'),
                                                api_key=key)
        elif translator == "DeeplTranslator":
            translate_instance = DeeplTranslator(source=config.get('translate', 'startlang'),
                                                 target=config.get('translate', 'endLang'),
                                                 api_key=key,
                                                 use_free_api=not pro)
        elif translator == "LibreTranslator":
            translate_instance = LibreTranslator(source=config.get('translate', 'startlang'),
                                                 target=config.get('translate', 'endLang'),
                                                 api_key=key,
                                                 custom_url=url)
        elif translator == "PapagoTranslator":
            translate_instance = PapagoTranslator(source='auto',
                                                  target=config.get('translate', 'endLang'),
                                                  client_id=client_id,
                                                  secret_key=key)
        elif translator == "ChatGptTranslator":
            translate_instance = ChatGptTranslator(source='auto', target=config.get('translate', 'endLang'))
        elif translator == "BaiduTranslator":
            translate_instance = BaiduTranslator(source=config.get('translate', 'startlang'),
                                                 target=config.get('translate', 'endLang'),
                                                 appid=appid,
                                                 appkey=key)
        logging.info('Translation Provider is {}'.format(translator))

        clipboard_text = pyperclip.paste()
        logging.info(f'Clipboard [{config.get("translate", "startLang")}]: {clipboard_text}')

        translation = translate_instance.translate(clipboard_text)
        logging.info(f'Translation [{config.get("translate", "endLang")}]: {translation}')
        return translation
    except Exception as e:
        logging.error(f"Translation Error: {e}", exc_info=True)


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
    else:
        try:
            start = time.perf_counter()
            if config.getboolean('translate', 'noTranslate'):
                clipboard = pyperclip.paste()
                stop = time.perf_counter() - start
                # print(f"Clipboard runtime is {stop:0.2f} seconds.")
                logging.info(f"Clipboard runtime is {stop:0.2f} seconds.")
            else:
                clipboard = translate_clipboard()
                stop = time.perf_counter() - start
                # print(f"Translation runtime is {stop:0.5f} seconds.")
                logging.info(f"Translation runtime is {stop:0.5f} seconds.")
            
            # Check the bypass TTS flag
            if not config.getboolean('TTS', 'bypass_tts', fallback=False):
                start = time.perf_counter()
                print(f"Text: [{clipboard}].")
                speak(clipboard)
                stop = time.perf_counter() - start
                # print(f"TTS runtime is {stop:0.5f} seconds.")
                logging.info(f"TTS runtime is {stop:0.5f} seconds.")
            if config.getboolean('translate', 'replacepb') and clipboard is not None:
                pyperclip.copy(clipboard)
            logging.info("------------------------------------------------------------------------")
        except Exception as e:
            logging.error("Runtime Error: {}".format(e), exc_info=True)
            if args['preview']:
                return
            else:
                result = utils.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Runtime Error')
                if result:
                    configure_app()
                else:
                    return


async def remove_stale_temp_files(directory_path, ignore_pattern=".db"):
    start = time.perf_counter()
    current_time = time.time()
    day = int(config.get('appCache', 'threshold'))
    time_threshold = current_time - day * 24 * 60 * 60
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if ignore_pattern and file.endswith(ignore_pattern):
                continue  # Ignore this file and move to the next iteration
            file_modification_time = os.path.getmtime(file_path)
            if file_modification_time < time_threshold:
                try:
                    os.remove(file_path)
                    file_list.append(os.path.basename(file_path))
                    print(f"Removed cache file: {file_path}")
                    logging.info(f"Removed cache file: {file_path}")
                except Exception as e:
                    print(f"Error removing file {file_path}: {e}")
                    logging.error(f"Removed cache file: {file_path}", exc_info=True)
    stop = time.perf_counter() - start
    clear_history(file_list)
    # print(f"Cache clearing runtime is {stop:0.5f} seconds.")
    logging.info(f"Cache clearing is {stop:0.5f} seconds.")
    logging.info("------------------------------------------------------------------------")


async def main(wav_files_path):
    await asyncio.gather(mainrun(args['listvoices']), remove_stale_temp_files(wav_files_path))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    asyncio.run(main(utils.audio_files_path))
