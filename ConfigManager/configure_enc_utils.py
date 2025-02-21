import io
import json
import logging
import os
from pathlib import Path
from cryptography.fernet import Fernet

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
        "MICROSOFT_TOKEN_TRANS"
    ]
    config = {}

    # Collect configuration from environment variables
    for key in required_keys:
        value = os.getenv(key)
        if not value:
            logging.error(f"Missing required environment variable: {key}")
            raise EnvironmentError(f"Missing required environment variable: {key}")
        config[key] = value

    # Handle Google credentials separately - it should be base64 encoded JSON
    google_creds_b64 = os.getenv("GOOGLE_CREDS_JSON")
    if not google_creds_b64:
        logging.error("Missing GOOGLE_CREDS_JSON environment variable")
        raise EnvironmentError("Missing GOOGLE_CREDS_JSON environment variable")

    try:
        # Decode base64 to get JSON string
        import base64
        google_creds_json = base64.b64decode(google_creds_b64).decode('utf-8')
        
        # Validate it's proper JSON
        json.loads(google_creds_json)  # Just to validate
        
        # Store the JSON string directly
        config['GOOGLE_CREDS_JSON'] = google_creds_json
        
    except Exception as e:
        logging.error(f"Invalid Google credentials format: {e}")
        raise ValueError(f"GOOGLE_CREDS_JSON must be base64 encoded JSON: {e}")

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