# File: encryption.py
import json
import logging
import os
import base64
from cryptography.fernet import Fernet
import sys
from pathlib import Path


class EncryptionManager:
    def __init__(self):
        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)
        self.logger = logging.getLogger(__name__)

    def _get_or_create_key(self) -> bytes:
        """Get existing key or create new one"""
        key_file = os.path.join(os.path.dirname(__file__), ".key")
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def load_encrypted_credentials(self) -> dict:
        """Load and decrypt credentials from config.enc"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), "config.enc")
            if not os.path.exists(config_path):
                logging.error("config.enc not found")
                return {}

            with open(config_path, "rb") as f:
                encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data)

        except Exception as e:
            logging.error(f"Failed to load encrypted credentials: {e}")
            return {}

    def save_encrypted_credentials(self, credentials: dict) -> bool:
        """Encrypt and save credentials to config.enc"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), "config.enc")
            encrypted_data = self.fernet.encrypt(json.dumps(credentials).encode())
            
            with open(config_path, "wb") as f:
                f.write(encrypted_data)
            return True

        except Exception as e:
            logging.error(f"Failed to save encrypted credentials: {e}")
            return False

    def create_google_creds_file(self, creds_base64: str, output_path: str):
        """Create Google credentials JSON file from base64 string"""
        try:
            # Decode base64 to JSON
            creds_json = base64.b64decode(creds_base64).decode("utf-8")
            creds_dict = json.loads(creds_json)
            
            # Write to file
            with open(output_path, "w") as f:
                json.dump(creds_dict, f, indent=4)
                
        except Exception as e:
            logging.error(f"Failed to create Google credentials file: {e}")
            raise

    def load_encrypted_config(self, config_path: str) -> dict:
        """Load and decrypt config.enc"""
        try:
            with open(config_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Get key from environment
            key = os.environ.get('CONFIG_ENCRYPTION_KEY').encode()
            fernet = Fernet(key)
            
            # Decrypt and parse JSON
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        
        except Exception as e:
            self.logger.error(f"Failed to load encrypted config: {e}")
            raise
