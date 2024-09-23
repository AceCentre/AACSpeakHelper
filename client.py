# client.py

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
from pathlib import Path
from cryptography.fernet import Fernet

# Import the load_config function from config_loader.py
from config_loader import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("client.log"), logging.StreamHandler(sys.stdout)],
)


def get_config_path():
    """
    Determines the path to settings.cfg based on whether the application is frozen.

    Returns:
        str: The path to settings.cfg.
    """
    if getattr(sys, "frozen", False):
        # Running as a bundled executable
        home_directory = Path.home()
        return str(
            home_directory
            / "AppData"
            / "Roaming"
            / "Ace Centre"
            / "AACSpeakHelper"
            / "settings.cfg"
        )
    else:
        # Running as a script (development)
        return str(Path(__file__).resolve().parent / "settings.cfg")


def load_standard_config(configuration_path):
    """
    Loads additional settings from settings.cfg to override configurations from config.enc.

    Args:
        configuration_path (str): The path to settings.cfg.

    Returns:
        dict: A dictionary containing overridden configuration keys and values.
    """
    configuration = configparser.ConfigParser()
    configuration.read(configuration_path)
    overrides = {}

    if "overrides" in configuration.sections():
        for key, value in configuration["overrides"].items():
            overrides[key.upper()] = value
            logging.info(f"Overridden {key.upper()} with value from settings.cfg")
    else:
        logging.warning(f"No [overrides] section found in {configuration_path}")

    return overrides


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
    default_config_path = get_config_path()

    parser = argparse.ArgumentParser(description="AACSpeakHelper Client")
    parser.add_argument(
        "-c",
        "--config",
        help="Path to a defined config file",
        required=False,
        default=default_config_path,
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
        # Load primary configuration from config.enc
        config = load_config()
        logging.info("Primary configuration loaded successfully.")
    except Exception as error:
        logging.error(f"Error loading primary configuration: {error}")
        sys.exit(1)

    # Load overrides from settings.cfg if specified
    if config_path and Path(config_path).is_file():
        try:
            overrides = load_standard_config(config_path)
            config.update(overrides)
            logging.info("Configuration overrides applied successfully.")
        except Exception as error:
            logging.error(f"Error applying configuration overrides: {error}")
            sys.exit(1)
    else:
        if config_path != default_config_path:
            logging.warning(
                f"Specified config file {config_path} does not exist. Skipping overrides."
            )

    # Verify that all required configuration fields are present
    required_fields = [
        "MICROSOFT_TOKEN",
        "MICROSOFT_REGION",
        "MICROSOFT_TOKEN_TRANS",
        "GOOGLE_CREDS_PATH",
    ]
    missing_fields = [field for field in required_fields if not config.get(field)]
    if missing_fields:
        logging.error(f"Missing configuration fields: {', '.join(missing_fields)}")
        sys.exit(1)

    # Verify that google_creds.json exists
    google_creds_path = Path(config["GOOGLE_CREDS_PATH"])
    if not google_creds_path.is_file():
        logging.error(f"Google credentials file not found at {google_creds_path}.")
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
