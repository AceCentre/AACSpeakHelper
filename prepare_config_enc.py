# prepare_config_enc.py

import os
import json
import logging
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create a generated key like this
# from cryptography.fernet import Fernet
# print(Fernet.generate_key().decode())
# store that then in the environment variable CONFIG_ENCRYPTION_KEY
# and then run this script


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


def main():
    """
    Main function to prepare the encrypted configuration.
    """
    # Optionally, allow specifying the output path via an environment variable
    output_path = os.getenv("CONFIG_OUTPUT_PATH", "config.enc")

    prepare_config_enc(output_path)


if __name__ == "__main__":
    main()
