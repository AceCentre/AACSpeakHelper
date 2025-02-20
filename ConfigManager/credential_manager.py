# File: credential_manager.py
import os
import sys
from configparser import ConfigParser
from typing import Optional, Dict, Any
import logging


class CredentialManager:
    def __init__(self, encryption):
        self.encryption = encryption
        self.config = ConfigParser()
        
        # Set up paths
        if getattr(sys, "frozen", False):
            self.config_dir = os.path.join(
                os.path.expanduser("~"),
                "AppData/Roaming/Ace Centre/AACSpeakHelper"
            )
        else:
            self.config_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.settings_cfg = os.path.join(self.config_dir, "settings.cfg")
        self.config_enc = os.path.join(self.config_dir, "config.enc")
        self.logger = logging.getLogger(__name__)

    def get_credentials(self, service: str) -> Optional[Dict[str, Any]]:
        """Get credentials with fallback system"""
        # Try user credentials first
        user_creds = self._load_user_credentials(service)
        if user_creds:
            return user_creds
            
        # Fall back to encrypted credentials
        return self._load_encrypted_credentials(service)

    def _load_user_credentials(self, service: str) -> Optional[Dict[str, Any]]:
        """Load credentials from settings.cfg"""
        try:
            self.config.read(self.settings_cfg)
            if self.config.has_section(service):
                return dict(self.config.items(service))
            return None
        except Exception as e:
            self.logger.error(f"Error loading user credentials for {service}: {e}")
            return None

    def _load_encrypted_credentials(self, service: str) -> Optional[Dict[str, Any] | tuple]:
        """Load credentials from config.enc"""
        try:
            encrypted_creds = self.encryption.load_encrypted_credentials()
            if not encrypted_creds:
                self.logger.debug(f"No encrypted credentials found for {service}")
                return None

            service_map = {
                "Microsoft": "azure",
                "Google": "google",
                "ElevenLabs": "elevenlabs",
                "PlayHT": "playht"
            }

            config_key = service_map.get(service)
            if not config_key or config_key not in encrypted_creds:
                return None

            creds = encrypted_creds[config_key]
            
            # Format credentials based on service
            if service == "Microsoft":
                return (
                    creds.get("MICROSOFT_TOKEN"),
                    creds.get("MICROSOFT_REGION")
                )
            elif service == "Google":
                # Google needs the credentials as a dictionary
                if isinstance(creds, dict) and "GOOGLE_APPLICATION_CREDENTIALS" in creds:
                    try:
                        import base64
                        import json
                        creds_json = base64.b64decode(
                            creds["GOOGLE_APPLICATION_CREDENTIALS"]
                        ).decode('utf-8')
                        return json.loads(creds_json)
                    except Exception as e:
                        self.logger.error(
                            f"Failed to decode Google credentials: {e}"
                        )
                        return None
                return None
            else:
                return creds

        except Exception as e:
            self.logger.error(f"Error loading encrypted credentials for {service}: {e}")
            return None

    def save_credentials(self, service: str, credentials: Dict[str, Any]) -> bool:
        """Save credentials to settings.cfg"""
        try:
            if not self.config.has_section(service):
                self.config.add_section(service)
                
            for key, value in credentials.items():
                self.config.set(service, key, str(value))
                
            with open(self.settings_cfg, 'w') as f:
                self.config.write(f)
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving credentials for {service}: {e}")
            return False
