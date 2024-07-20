import asyncio
import json
import logging
import os
import time

import pyperclip
import pyttsx3
import pywintypes
import win32file
import win32pipe
from PySide6.QtWidgets import *
from deep_translator import *
import utils
from GUI_TranslateAndTTS.language_dictionary import *
import tts_utils
# from utils import init, configure_app, config, args, clear_history


def translate_clipboard():
    try:
        config = utils.config
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
        # elif translator == "DeepLearningTranslator":
        #     translate_instance = BaiduTranslator(source=config.get('translate', 'startlang'),
        #                                          target=config.get('translate', 'endLang'),
        #                                          appid=appid,
        #                                          appkey=key)
        logging.info('Translation Provider is {}'.format(translator))

        clipboard_text = pyperclip.paste()
        logging.info(f'Clipboard [{config.get("translate", "startLang")}]: {clipboard_text}')

        translation = translate_instance.translate(clipboard_text)
        logging.info(f'Translation [{config.get("translate", "endLang")}]: {translation}')
        return translation
    except Exception as e:
        logging.error(f"Translation Error: {e}", exc_info=True)


async def mainrun(listvoices: bool):
    config = utils.config
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
                utils.configure_app()
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
                tts_utils.speak(clipboard)
                stop = time.perf_counter() - start
                # print(f"App runtime is {stop:0.5f} seconds.")
                logging.info(f"App runtime is {stop:0.5f} seconds.")
            if config.getboolean('translate', 'replacepb') and clipboard is not None:
                pyperclip.copy(clipboard)
            logging.info("------------------------------------------------------------------------")
        except Exception as e:
            logging.error("Runtime Error: {}".format(e), exc_info=True)
            if utils.args['preview']:
                return
            else:
                result = utils.ynbox(str(e) + '\n\n Do You want to open the Configuration Setup?', 'Runtime Error')
                if result:
                    utils.configure_app()
                else:
                    return


async def remove_stale_temp_files(directory_path, ignore_pattern=".db"):
    config = utils.config
    start = time.perf_counter()
    current_time = time.time()
    day = int(config.get('appCache', 'threshold'))
    time_threshold = current_time - day * 24 * 60 * 60
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if ignore_pattern and file.endswith(ignore_pattern) and file.endswith('.db-journal'):
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
    utils.clear_history(file_list)
    # print(f"Cache clearing runtime is {stop:0.5f} seconds.")
    logging.info(f"Cache clearing is {stop:0.5f} seconds.")
    logging.info("------------------------------------------------------------------------")


async def main(wav_files_path):
    await asyncio.gather(mainrun(utils.args['listvoices']), remove_stale_temp_files(wav_files_path))


def pipe_server():
    pipe_name = r'\\.\pipe\AACSpeechHelper'
    logging.info("Pipe Server: Creating named pipe...")
    while True:
        try:
            pipe = win32pipe.CreateNamedPipe(
                pipe_name,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1, 65536, 65536,
                0,
                None)
            logging.info("Pipe Server: Waiting for client...")
            print(f'Waiting for request ...')
            win32pipe.ConnectNamedPipe(pipe, None)
            logging.info("Pipe Server: Client connected.")
        except pywintypes.error as e:
            logging.error(f"Failed to create or connect named pipe: {e}")
            print(f"Failed to create or connect named pipe: Close all python.exe to restart the Pipe")
            continue  # Attempt to create a new pipe and wait for a new connection

        try:
            while True:
                # Read the sentence from the client
                result, data = win32file.ReadFile(pipe, 64 * 1024)
                if result == 0:  # Check if the read was successful
                    arguments = json.loads(data.decode())
                    utils.init(args=arguments)
                    tts_utils.init(utils)
                    asyncio.run(main(utils.audio_files_path))
                else:
                    break  # Break out of the inner loop if reading fails
        except pywintypes.error as e:
            logging.error(f"Communication error: {e}")
        finally:
            win32file.CloseHandle(pipe)
            logging.info("Client disconnected. Waiting for new connection...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pipe_server()
