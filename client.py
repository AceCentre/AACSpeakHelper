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

parser = argparse.ArgumentParser(
    description='Reads pasteboard. Translates it. Speaks it out. Or any variation of that')
parser.add_argument(
    '-c', '--config', help='Path to a defined config file', required=False, default='')
parser.add_argument(
    '-l', '--listvoices', help='List Voices to see whats available', required=False, default=False, action="store_true")
parser.add_argument(
    '-p', '--preview', help='Preview Only', required=False, default=False, action="store_true")
parser.add_argument(
    '-s', '--style', help='Voice style for Azure TTS', required=False, default='')
parser.add_argument(
    '-sd', '--styledegree', type=float, help='Degree of style for Azure TTS', required=False, default=None)
args = vars(parser.parse_args())
data_string = json.dumps(args)


def send_to_pipe(arguments, retries=3, delay=1):
    pipe_name = r'\\.\pipe\AACSpeechHelper'
    attempt = 0
    while attempt < retries:
        try:
            handle = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0, None,
                win32file.OPEN_EXISTING,
                0, None)
            win32file.WriteFile(handle, arguments.encode())
            win32file.CloseHandle(handle)
            break
        except pywintypes.error as e:
            logging.error(f"Attempt {attempt + 1}: Error communicating with the pipe server: {e}")
            time.sleep(delay)  # Wait before retrying
            attempt += 1
    return None


if __name__ == '__main__':
    send_to_pipe(data_string)
