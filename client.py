import sys
import argparse
import logging
import pyperclip
import win32file
import win32pipe
import pywintypes
import time
import os
import json
import configparser

def get_clipboard_text():
    return pyperclip.paste()


def send_to_pipe(data, retries=3, delay=1):
    pipe_name = r'\\.\pipe\AACSpeakHelper'
    attempt = 0
    while attempt < retries:
        try:
            handle = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0, None,
                win32file.OPEN_EXISTING,
                0, None)
            win32file.WriteFile(handle, json.dumps(data).encode())
            try:
                result, data = win32file.ReadFile(handle, 128 * 1024)
                if result == 0:
                    available_voices = data.decode()
                    print(available_voices)
                    logging.info(f"Available Voices : {available_voices}")
            except Exception as readError:
                if '109' not in str(readError):
                    print(readError)
            win32file.CloseHandle(handle)
            break
        except pywintypes.error as e:
            logging.error(f"Attempt {attempt + 1}: Error communicating with the pipe server: {e}")
            time.sleep(delay)
            attempt += 1
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AACSpeakHelper Client')
    parser.add_argument('-c', '--config', help='Path to a defined config file', required=False, default='')
    parser.add_argument('-l', '--listvoices', help='List Voices to see whats available', action="store_true")
    parser.add_argument('-p', '--preview', help='Preview Only', action="store_true")
    parser.add_argument('-s', '--style', help='Voice style for Azure TTS', default='')
    parser.add_argument('-sd', '--styledegree', type=float, help='Degree of style for Azure TTS', default=None)
    args = vars(parser.parse_args())

    config_path = args['config'] if args['config'] else get_config_path()
    config = load_config(config_path)

    clipboard_text = get_clipboard_text()

    data_to_send = {
        'args': args,
        'config': {section: dict(config[section]) for section in config.sections()},
        'clipboard_text': clipboard_text
    }

    send_to_pipe(data_to_send)
