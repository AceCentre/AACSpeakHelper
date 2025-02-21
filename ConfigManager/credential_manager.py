# File: credential_manager.py
import os
import sys
from configparser import ConfigParser
from typing import Optional, Dict, Any
import logging


class CredentialManager:
    def __init__(self, encryption_manager):
        self.encryption = encryption_manager
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

    def get_credentials(self, engine_name: str) -> Optional[tuple]:
        """Get credentials for an engine, trying settings.cfg first then config.enc"""
        try:
            # Try settings.cfg first
            self.config.read(self.settings_cfg)
            self.logger.debug(f"Attempting to get credentials for {engine_name}")
            
            if engine_name == "Azure TTS":
                # Try user credentials first
                if self.config.has_section('azureTTS'):
                    key = self.config.get('azureTTS', 'key', fallback=None)
                    region = self.config.get('azureTTS', 'location', fallback=None)
                    if key and region:
                        self.logger.info(f"Using user credentials for Azure TTS from settings.cfg")
                        return (key, region)
                    else:
                        self.logger.debug("Incomplete Azure credentials in settings.cfg")
                
                # Fall back to encrypted credentials
                self.logger.debug("Attempting to load Azure credentials from config.enc")
                enc_config = self.encryption.load_encrypted_config(self.config_enc)
                
                if not enc_config.get('MICROSOFT_TOKEN') or not enc_config.get('MICROSOFT_REGION'):
                    self.logger.error("Missing required Azure credentials in config.enc")
                    self.logger.debug(f"Found keys: {list(enc_config.keys())}")
                    raise ValueError("Missing required Azure credentials")
                    
                self.logger.info("Using Azure credentials from config.enc")
                token = enc_config['MICROSOFT_TOKEN']
                region = enc_config['MICROSOFT_REGION']
                self.logger.debug(f"Found token (length: {len(token)}) and region: {region}")
                return (token, region)
                
            elif engine_name == "Google TTS":
                # Try user credentials first
                if self.config.has_section('googleTTS'):
                    creds_path = self.config.get('googleTTS', 'creds', fallback=None)
                    if creds_path and os.path.exists(creds_path):
                        self.logger.info(f"Using Google credentials file from settings.cfg: {creds_path}")
                        return (creds_path,)
                    else:
                        self.logger.debug(f"Invalid Google credentials path in settings.cfg: {creds_path}")
                
                # Fall back to encrypted credentials
                self.logger.debug("Attempting to load Google credentials from config.enc")
                enc_config = self.encryption.load_encrypted_config(self.config_enc)
                
                if not enc_config.get('GOOGLE_CREDS_JSON'):
                    raise ValueError("Missing Google credentials in config.enc")
                
                # Create temporary credentials file
                try:
                    import tempfile
                    import json
                    
                    # The Google creds should already be a JSON string
                    google_creds = enc_config['GOOGLE_CREDS_JSON']
                    if isinstance(google_creds, str):
                        try:
                            # Try parsing to validate JSON
                            creds_dict = json.loads(google_creds)
                        except json.JSONDecodeError:
                            # If it's base64 encoded, decode first
                            import base64
                            try:
                                decoded = base64.b64decode(google_creds).decode('utf-8')
                                creds_dict = json.loads(decoded)
                            except:
                                raise ValueError("Google credentials are neither valid JSON nor base64 encoded JSON")
                    else:
                        creds_dict = google_creds
                    
                    temp_creds = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
                    json.dump(creds_dict, temp_creds, indent=2)
                    temp_creds.close()
                    
                    self.logger.info(f"Created temporary Google credentials file: {temp_creds.name}")
                    return (temp_creds.name,)
                    
                except Exception as e:
                    self.logger.error(f"Failed to process Google credentials: {e}")
                    raise ValueError(f"Invalid Google credentials format: {e}")
                
            # Debug what we're getting from encrypted storage
            encrypted_creds = self._load_encrypted_credentials()
            if encrypted_creds and engine_name in encrypted_creds:
                creds = encrypted_creds[engine_name]
                self.logger.debug(f"Found {engine_name} creds: {type(creds)}, length: {len(creds)}")
                return creds
                
        except FileNotFoundError as e:
            self.logger.error(f"Configuration file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in encrypted config: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to get credentials for {engine_name}: {e}")
            raise

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
