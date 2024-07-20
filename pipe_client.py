import sys
import argparse
import logging
import pyperclip
import win32file
import win32pipe
import pywintypes
import time
import os


def send_to_pipe(sentence, retries=3, delay=1):
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
            win32file.WriteFile(handle, sentence.encode())
            result, data = win32file.ReadFile(handle, 64 * 1024)
            corrected_sentence = data.decode()
            win32file.CloseHandle(handle)
            return corrected_sentence
        except pywintypes.error as e:
            logging.error(f"Attempt {attempt + 1}: Error communicating with the pipe server: {e}")
            time.sleep(delay)  # Wait before retrying
            attempt += 1
    return None


if __name__ == '__main__':
    send_to_pipe(sentence='Hello World')
