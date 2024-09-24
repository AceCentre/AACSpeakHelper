import ast
import json
import logging
import os
from pathlib import Path
import configparser
from cryptography.fernet import Fernet
import sys
import base64
from os import path

os.setenv("CONFIG_ENCRYPTION_KEY", "YOUR_ENCRYPTION_KEY")

# Create a generated key like this
# from cryptography.fernet import Fernet
# print(Fernet.generate_key().decode())
# store that then in the environment variable CONFIG_ENCRYPTION_KEY
# and then run this script


def create_google_creds_file(creds_path="google_creds.json"):
    # Retrieve the base64-encoded JSON string from the environment variable
    encoded_json = os.getenv("GOOGLE_CREDS_JSON")
    filename = creds_path
    if not encoded_json:
        raise ValueError("GOOGLE_CREDS_JSON environment variable is not set")

    try:
        # Decode the base64 string back into JSON
        decoded_json = base64.b64decode(encoded_json).decode("utf-8")

        # Write the decoded JSON content to the specified file
        with open(filename, "w") as f:
            f.write(decoded_json)
        print(f"Google credentials file created at {filename}")

    except (ValueError, base64.binascii.Error) as e:
        print(f"Failed to decode GOOGLE_CREDS_JSON: {e}")


def find_config_enc(start_path: Path, max_depth: int = 5) -> Path:
    """
    Searches for 'config.enc' starting from 'start_path' and traversing up to 'max_depth' levels.

    Args:
        start_path (Path): The directory to start searching from.
        max_depth (int): The maximum number of parent directories to traverse.

    Returns:
        Path: The path to 'config.enc' if found.

    Raises:
        FileNotFoundError: If 'config.enc' is not found within the specified depth.
    """
    current_path = start_path
    for depth in range(max_depth):
        config_path = current_path / "config.enc"
        internal_config_path = current_path / "_internal" / "config.enc"
        logging.debug(f"Checking for config.enc at: {config_path}")
        if config_path.is_file():
            logging.debug(f"Found config.enc at: {config_path}")
            return config_path
        if internal_config_path.is_file():
            logging.debug(f"Found _internal/config.enc at: {internal_config_path}")
            return internal_config_path
        current_path = current_path.parent  # Move one level up
        logging.debug(f"Moving up to parent directory: {current_path}")

    raise FileNotFoundError(
        f"'config.enc' not found within {max_depth} levels up from {start_path}"
    )


def get_google_creds_path():
    """
    Determines the path for google_creds.json based on whether the application is frozen.

    Returns:
        Path: The path to google_creds.json.
    """
    if getattr(sys, "frozen", False):
        # Running as a bundled executable
        app_data = Path.home() / "AppData" / "Roaming" / "Ace Centre" / "AACSpeakHelper"
    else:
        # Running as a script (development)
        # Assume that config.enc is at the repository root, and so is google_creds.json
        app_data = Path.cwd()

    return app_data / "google_creds.json"


def find_config_enc(start_path: Path, max_depth: int = 5) -> Path:
    """
    Searches for 'config.enc' starting from 'start_path' and traversing up to 'max_depth' levels.

    Args:
        start_path (Path): The directory to start searching from.
        max_depth (int): The maximum number of parent directories to traverse.

    Returns:
        Path: The path to 'config.enc' if found.

    Raises:
        FileNotFoundError: If 'config.enc' is not found within the specified depth.
    """
    current_path = start_path
    for depth in range(max_depth):
        config_path = current_path / "config.enc"
        internal_config_path = current_path / "_internal" / "config.enc"
        logging.debug(f"Checking for config.enc at: {config_path}")
        if config_path.is_file():
            logging.debug(f"Found config.enc at: {config_path}")
            return config_path
        if internal_config_path.is_file():
            logging.debug(f"Found _internal/config.enc at: {internal_config_path}")
            return internal_config_path
        current_path = current_path.parent  # Move one level up
        logging.debug(f"Moving up to parent directory: {current_path}")

    raise FileNotFoundError(
        f"'config.enc' not found within {max_depth} levels up from {start_path}"
    )


def generate_key():
    """
    Generates a new Fernet encryption key.
    """
    key = Fernet.generate_key()
    logging.info("Generated new encryption key.")
    return key


def load_encryption_key():
    """
    Loads the encryption key from the environment variable.

    Returns:
        bytes: The encryption key.

    Raises:
        EnvironmentError: If the encryption key environment variable is not set.
    """
    encryption_key = os.getenv("CONFIG_ENCRYPTION_KEY")
    if not encryption_key:
        logging.error("CONFIG_ENCRYPTION_KEY environment variable is not set.")
        raise EnvironmentError("CONFIG_ENCRYPTION_KEY environment variable is not set.")
    try:
        # Ensure the key is in bytes
        encryption_key_bytes = encryption_key.encode()
        # Validate key length for Fernet (must be 32 url-safe base64-encoded bytes)
        Fernet(
            encryption_key_bytes
        )  # This will raise an exception if the key is invalid
        logging.info("Loaded encryption key from environment variable.")
        return encryption_key_bytes
    except Exception as e:
        logging.error(f"Invalid encryption key: {e}")
        raise ValueError(
            "Invalid CONFIG_ENCRYPTION_KEY. Ensure it is a valid Fernet key."
        )


def prepare_config_enc(output_path="config.enc"):
    """
    Prepares and encrypts the configuration from environment variables.

    Args:
        output_path (str): Path to save the encrypted config.enc file.
    """
    # Define the required configuration keys
    required_keys = [
        "MICROSOFT_TOKEN",
        "MICROSOFT_REGION",
        "MICROSOFT_TOKEN_TRANS",
        "GOOGLE_CREDS_JSON",
    ]

    config = {}
    missing_keys = []

    # Collect configuration from environment variables
    for key in required_keys:
        value = os.getenv(key)
        if value:
            config[key] = value
        else:
            missing_keys.append(key)

    if missing_keys:
        logging.error(
            f"Missing required environment variables: {', '.join(missing_keys)}"
        )
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_keys)}"
        )

    # Convert the config dictionary to JSON bytes
    config_json = json.dumps(config).encode()

    # Load the encryption key from environment variable
    encryption_key = load_encryption_key()

    # Encrypt the configuration
    fernet = Fernet(encryption_key)
    encrypted_config = fernet.encrypt(config_json)

    # Save the encrypted configuration
    with open(output_path, "wb") as config_file:
        config_file.write(encrypted_config)

    logging.info(f"Encrypted configuration saved to {output_path}.")


def load_config():
    """
    Load configuration from an encrypted file and optionally override with settings from settings.cfg.

    Returns:
        dict: A dictionary containing configuration keys and their corresponding values.

    Raises:
        EnvironmentError: If required environment variables are not set.
        FileNotFoundError: If config.enc or google_creds.json are not found.
        ValueError: If the configuration is incomplete or corrupted.
    """
    config = {}

    # Determine the starting directory based on whether the app is frozen
    if getattr(sys, "frozen", False):
        # Running as a bundled executable
        executable_dir = Path(sys.executable).parent
        start_dir = executable_dir
        logging.debug(f"Executable directory: {executable_dir}")
    else:
        # Running as a script (development)
        start_dir = (
            Path.cwd()
        )  # Assuming the current working directory is the repo root
        logging.debug(
            f"Script is running in development mode. Current working directory: {start_dir}"
        )

    # Attempt to find config.enc
    try:
        encrypted_config_path = find_config_enc(start_dir)
        logging.info(f"Found encrypted configuration file at: {encrypted_config_path}")
    except FileNotFoundError as e:
        logging.warning(e)
        encrypted_config_path = None

    if encrypted_config_path:
        # Load the encryption key from the environment variable
        encryption_key = os.getenv("CONFIG_ENCRYPTION_KEY")
        if not encryption_key:
            logging.error("CONFIG_ENCRYPTION_KEY environment variable is not set.")
            raise EnvironmentError(
                "CONFIG_ENCRYPTION_KEY environment variable is not set."
            )

        try:
            # Initialize Fernet with the encryption key
            fernet = Fernet(encryption_key.encode())

            # Read and decrypt the configuration
            with encrypted_config_path.open("rb") as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)

            # Debugging: print the decrypted content before parsing
            logging.debug(f"Decrypted configuration content: {decrypted_data.decode()}")

            # Load the decrypted JSON
            decrypted_config = json.loads(decrypted_data.decode())
            logging.info("Successfully decrypted configuration from config.enc.")

            # Write google_creds.json to the determined path
            google_creds_path = get_google_creds_path()
            if not path.exists(google_creds_path):
                os.makedirs(google_creds_path.parent, exist_ok=True)
                create_google_creds_file(google_creds_path)
                logging.info(f"Google credentials file created at {google_creds_path}")

            config["GOOGLE_CREDS_PATH"] = str(google_creds_path)

            # Populate other configuration keys
            config["MICROSOFT_TOKEN"] = decrypted_config.get(
                "MICROSOFT_TOKEN", ""
            ).strip()
            config["MICROSOFT_REGION"] = decrypted_config.get(
                "MICROSOFT_REGION", ""
            ).strip()
            config["MICROSOFT_TOKEN_TRANS"] = decrypted_config.get(
                "MICROSOFT_TOKEN_TRANS", ""
            ).strip()

        except Exception as e:
            print(e)
            logging.error(f"Failed to load configuration from encrypted file: {e}")
            logging.info("Falling back to loading configuration from settings.cfg.")
            encrypted_config_path = None  # Reset to allow loading from settings.cfg

    # Load configuration from settings.cfg if it exists
    settings_cfg_path = start_dir / "settings.cfg"
    if settings_cfg_path.is_file():
        logging.info(f"Loading configuration overrides from {settings_cfg_path}")
        config_parser = configparser.ConfigParser()
        config_parser.read(settings_cfg_path)

        if "overrides" in config_parser.sections():
            for key, value in config_parser["overrides"].items():
                config[key.upper()] = value.strip()
                logging.info(f"Overridden {key.upper()} with value from settings.cfg")
        else:
            logging.warning(f"No [overrides] section found in {settings_cfg_path}")
    else:
        logging.info("No settings.cfg file found. Skipping overrides.")

    # Final validation to ensure all required fields are present
    required_fields = [
        "MICROSOFT_TOKEN",
        "MICROSOFT_REGION",
        "MICROSOFT_TOKEN_TRANS",
        "GOOGLE_CREDS_PATH",
    ]
    missing_fields = [field for field in required_fields if not config.get(field)]
    if missing_fields:
        logging.error(
            f"Missing configuration fields after loading: {', '.join(missing_fields)}"
        )
        raise ValueError(f"Missing configuration fields: {', '.join(missing_fields)}")

    # Verify that google_creds.json exists
    google_creds_path = Path(config["GOOGLE_CREDS_PATH"])
    if not google_creds_path.is_file():
        logging.error(f"Google credentials file not found at {google_creds_path}.")
        raise FileNotFoundError(
            f"Google credentials file not found at {google_creds_path}."
        )

    logging.info("Final configuration loaded successfully.")
    return config
