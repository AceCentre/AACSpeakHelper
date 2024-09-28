import io
import json
import logging
import os
import pickle
from pathlib import Path
import configparser
from cryptography.fernet import Fernet
import sys
import argparse

# Ensure CONFIG_ENCRYPTION_KEY is set
if "CONFIG_ENCRYPTION_KEY" not in os.environ:
    os.environ["CONFIG_ENCRYPTION_KEY"] = "YOUR_ENCRYPTION_KEY"


# use it like this
# jq -c '@json' ttsandtranslate-7dd2e2d80d42.json

def create_google_creds_file(filename):
    google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
    if not google_creds_json:
        raise ValueError("GOOGLE_CREDS_JSON environment variable is not set")
    
    with open(filename, "w") as f:
        f.write(google_creds_json)

def load_encryption_key():
    """Loads the encryption key from the environment variable."""
    encryption_key = os.getenv("CONFIG_ENCRYPTION_KEY")
    if not encryption_key:
        logging.error("CONFIG_ENCRYPTION_KEY environment variable is not set.")
        raise EnvironmentError("CONFIG_ENCRYPTION_KEY environment variable is not set.")
    return encryption_key.encode()


def prepare_config_enc(output_path="config.enc"):
    """Prepares and encrypts the configuration from environment variables into config.enc."""
    required_keys = [
        "MICROSOFT_TOKEN",
        "MICROSOFT_REGION",
        "MICROSOFT_TOKEN_TRANS",
        "GOOGLE_CREDS_JSON",
    ]
    config = {}

    # Collect configuration from environment variables
    for key in required_keys:
        value = os.getenv(key)
        if not value:
            logging.error(f"Missing required environment variable: {key}")
            raise EnvironmentError(f"Missing required environment variable: {key}")
        config[key] = value

    # Convert the config dictionary to JSON bytes
    config_json = json.dumps(config).encode()

    # Load the encryption key and encrypt the configuration
    encryption_key = load_encryption_key()
    fernet = Fernet(encryption_key)
    encrypted_config = fernet.encrypt(config_json)

    # Save the encrypted configuration to the file
    with open(output_path, "wb") as config_file:
        config_file.write(encrypted_config)
    logging.info(f"Encrypted configuration saved to {output_path}.")


def load_config(custom_config_path=""):
    """Load configuration from the encrypted config.enc file and optionally from settings.cfg."""
    if getattr(sys, "frozen", False):
        # Running as a bundled executable
        app_data = Path.home() / "AppData" / "Roaming" / "Ace Centre" / "AACSpeakHelper"
    else:
        # Running as a script (development)
        # Assume that config.enc is at the repository root,
        app_data = Path(os.path.dirname(__file__))
    encrypted_config_path = app_data / "config.enc"
    settings_cfg_path = app_data / "settings.cfg"
    encrypted_json_path = app_data / "google_creds.enc"

    # Load configuration from the encrypted file
    try:
        encryption_key = load_encryption_key()
        fernet = Fernet(encryption_key)

        # Read and decrypt the configuration
        with encrypted_config_path.open("rb") as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)

        # Load the decrypted JSON into a dictionary
        config = json.loads(decrypted_data.decode())

        # Overwrite the creds with base64 encoded creds. This is mad - it already is but somehow it gets decrypted
        # google_creds_json = config.get("GOOGLE_CREDS_JSON")
        # google_creds_bytes = google_creds_json.encode("utf-8")
        # base64_encoded_creds = base64.b64encode(google_creds_bytes)
        # base64_encoded_creds_str = base64_encoded_creds.decode("utf-8")
        config["GOOGLE_CREDS_JSON"] = str(encrypted_json_path)
        logging.info("Successfully decrypted configuration from config.enc.")

    except Exception as e:
        logging.error(f"Failed to load configuration from encrypted file: {e}")
        raise

    # Load configuration from settings.cfg if it exists or if a custom path is provided
    if custom_config_path:
        settings_cfg_path = Path(custom_config_path)

    if settings_cfg_path.is_file():

        logging.info(f"Loading configuration overrides from {settings_cfg_path}")
        config_parser = configparser.ConfigParser()
        config_parser.read(settings_cfg_path)
        config_dict = {
            section: dict(config_parser.items(section))
            for section in config_parser.sections()
        }

        config_dict["azureTTS"]["key"] = config.get("MICROSOFT_TOKEN")
        config_dict["azureTTS"]["location"] = config.get("MICROSOFT_REGION")
        config_dict["googleTTS"]["creds"] = config.get("GOOGLE_CREDS_JSON")
        config_dict["translate"]["microsofttranslator_secret_key"] = config.get(
            "MICROSOFT_TOKEN_TRANS"
        )

    else:
        config_dict = None
        logging.info("No settings.cfg file found. Skipping overrides.")

    logging.info("Final configuration loaded successfully.")

    return config_dict


def load_credentials(fp: str) -> object:
    encryption_key = load_encryption_key()
    fernet = Fernet(encryption_key)
    with open(fp, 'rb') as f:
        return pickle.loads(fernet.decrypt(f.read()))


def save_credentials(obj: object, fp: str):
    encryption_key = load_encryption_key()
    fernet = Fernet(encryption_key)
    with open(fp, 'wb') as f:
        f.write(fernet.encrypt(pickle.dumps(obj)))

# Example usage
# prepare_config_enc()  # Run this to create config.enc
# config = load_config()  # Load config when needed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AACSpeakHelper Encryption Utility")
    parser.add_argument(
        "-i",
        "--input",
        help="Path to a defined JSON file",
        required=False
    )
    parser.add_argument(
        "-use-json-in-env",
        action="store_true",
        help="Create JSON from environment variables instead of input file"
    )
    args = vars(parser.parse_args())

    # Check if -use-json-in-env is provided
    if args['use_json_in_env']:
        # Set a default filename for the JSON file to be created from the environment variable
        filename = Path("google_creds.json")
        create_google_creds_file(filename)
    else:
        # Handle the input flag normally
        if not args['input']:
            print("Either --input or --use-json-in-env must be specified.")
            sys.exit(1)
        
        filename = Path(args['input'])

    file_path = filename.resolve().parent
    with io.open(filename, "r", encoding="utf-8") as json_file:
        json_dict = json.load(json_file)
        new_file = filename.with_suffix('.enc')
        save_credentials(json_dict, os.path.join(file_path, new_file))
        print(load_credentials(new_file))
