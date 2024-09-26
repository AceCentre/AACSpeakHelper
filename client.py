# client.py

import sys
import argparse
import logging
import pyperclip
import win32file
import pywintypes
import time
import json
from pathlib import Path

from configure_enc_utils import load_config


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("client.log"), logging.StreamHandler(sys.stdout)],
)


def get_clipboard_text():
    """
    Retrieves the current text from the clipboard.

    Returns:
        str: The clipboard text.
    """
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException as e:
        logging.error(f"Failed to get clipboard text: {e}")
        return ""


def send_to_pipe(data, retries=3, delay=1):
    """
    Sends data to a named pipe.

    Args:
        data (dict): The data to send.
        retries (int): Number of retries if the pipe is unavailable.
        delay (int): Delay in seconds between retries.

    Returns:
        None
    """
    pipe_name = r"\\.\pipe\AACSpeakHelper"
    attempt = 0
    while attempt < retries:
        try:
            handle = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None,
            )
            message = json.dumps(data).encode()
            win32file.WriteFile(handle, message)
            logging.info(f"Sent data to pipe: {data}")

            try:
                result, response = win32file.ReadFile(handle, 128 * 1024)
                if result == 0:
                    available_voices = response.decode()
                    logging.info(f"Available Voices: {available_voices}")
            except Exception as read_error:
                if "109" not in str(read_error):
                    logging.error(f"Error reading from pipe: {read_error}")

            win32file.CloseHandle(handle)
            break
        except pywintypes.error as e:
            logging.error(
                f"Attempt {attempt + 1}: Error communicating with the pipe server: {e}"
            )
            time.sleep(delay)
            attempt += 1
    else:
        logging.error(
            "Failed to communicate with the pipe server after multiple attempts."
        )


def main():
    """
    Main function to execute the client logic.
    """
    parser = argparse.ArgumentParser(description="AACSpeakHelper Client")
    parser.add_argument(
        "-c",
        "--config",
        help="Path to a defined config file",
        required=False,
        default="",
    )
    parser.add_argument(
        "-l",
        "--listvoices",
        help="List Voices to see what's available",
        action="store_true",
    )
    parser.add_argument("-p", "--preview", help="Preview Only", action="store_true")
    parser.add_argument("-s", "--style", help="Voice style for Azure TTS", default="")
    parser.add_argument(
        "-sd",
        "--styledegree",
        type=float,
        help="Degree of style for Azure TTS",
        default=None,
    )
    args = vars(parser.parse_args())

    config_path = args["config"]
    try:
        # Check if a custom configuration file was provided
        if config_path:
            # If a custom config path is provided, load config with that path
            config = load_config(custom_config_path=config_path)
            logging.info(f"Primary configuration loaded from {config_path}.")
        else:
            # Load the default configuration
            config = load_config()
            logging.info("Primary configuration loaded successfully.")
    except Exception as error:
        logging.error(f"Error loading primary configuration: {error}")
        sys.exit(1)
    logging.info("All configurations are validated successfully.")

    # Retrieve clipboard text
    clipboard_text = get_clipboard_text()
    logging.debug(f"Clipboard text: {clipboard_text}")

    # Prepare data to send
    data_to_send = {
        "args": args,
        "config": config,
        "clipboard_text": clipboard_text,
    }

    # Send data to the named pipe
    send_to_pipe(data_to_send)


if __name__ == "__main__":
    main()
