# client.py

import sys
import os
import argparse
import logging
import pyperclip
import win32file
import pywintypes
import time
import json

from configure_enc_utils import load_config


# Configure logging
def setup_logging():
    if getattr(sys, "frozen", False):
        # If the application is run as a bundle, use the AppData directory
        log_dir = os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Roaming",
            "Ace Centre",
            "AACSpeakHelper",
        )
    else:
        # If run from a Python environment, use the current directory
        log_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "client.log")

    logging.basicConfig(
        filename=log_file,
        filemode="a",
        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
        level=logging.DEBUG,
    )

    return log_file


logfile = setup_logging()


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
        bool: True if the data was sent successfully, False otherwise.
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
                    # If we're listing voices, print them to the console
                    if data.get("args", {}).get("listvoices", False) and data.get(
                        "args", {}
                    ).get("verbose", False):
                        print("Available voices:")
                        print(available_voices)
            except Exception as read_error:
                if "109" not in str(read_error):
                    logging.error(f"Error reading from pipe: {read_error}")

            win32file.CloseHandle(handle)
            return True  # Successfully sent data
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
        return False  # Failed to send data


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
    parser.add_argument(
        "-t",
        "--text",
        help="Text to process instead of clipboard content",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose output",
        action="store_true",
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

    # Get text to process (from command line or clipboard)
    if args["text"]:
        text_to_process = args["text"]
        if args["verbose"]:
            print(f"Using provided text: {text_to_process}")
        logging.debug(f"Using provided text: {text_to_process}")
    else:
        text_to_process = get_clipboard_text()
        if args["verbose"]:
            print(f"Using clipboard text: {text_to_process}")
        logging.debug(f"Clipboard text: {text_to_process}")

    # Convert ConfigParser to dictionary for JSON serialization
    config_dict = {}
    if hasattr(config, "sections"):
        for section in config.sections():
            config_dict[section] = {}
            for key, value in config.items(section):
                config_dict[section][key] = value

    # Prepare data to send
    data_to_send = {
        "args": args,
        "config": config_dict,
        "clipboard_text": text_to_process,
    }

    if args["verbose"]:
        print("Sending data to AACSpeakHelper server...")
        print(f"TTS Engine: {config.get('TTS', 'engine', fallback='Not configured')}")
        print(f"Voice: {config.get('TTS', 'voice_id', fallback='Default')}")
        if not config.getboolean("translate", "noTranslate", fallback=True):
            print(
                f"Translation: {config.get('translate', 'provider', fallback='None')}"
            )
            print(
                f"From: {config.get('translate', 'startLang', fallback='auto')} "
                f"To: {config.get('translate', 'endLang', fallback='en')}"
            )

    # Send data to the named pipe
    result = send_to_pipe(data_to_send)

    if args["verbose"]:
        if result:
            print("Request processed successfully.")
        else:
            print("Failed to process request. Check the logs for details.")
            print(f"Log file: {logfile}")


if __name__ == "__main__":
    main()
