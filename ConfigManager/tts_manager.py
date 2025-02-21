# File: tts_manager.py
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
from tts_wrapper import (
    MicrosoftTTS, MicrosoftClient,
    GoogleTTS, GoogleClient,
    ElevenLabsTTS, ElevenLabsClient,
    PlayHTTTS, PlayHTClient,
    SherpaOnnxTTS, SherpaOnnxClient,
    GoogleTransClient
)
from pathlib import Path
from credential_manager import CredentialManager
from encryption import EncryptionManager

@dataclass
class CredentialField:
    """Defines a credential field requirement for a TTS engine"""
    name: str  # Field identifier
    field_type: str  # "text", "file", or "region"
    label: str  # Display label for UI

@dataclass
class TTSConfig:
    """Configuration for a TTS engine"""
    name: str  # Engine name
    tts_class: type  # TTS class
    client_class: type  # Client class
    requires_download: bool = False  # Whether engine needs model downloads
    requires_credentials: bool = True  # Whether engine needs credentials
    credential_fields: Optional[List[CredentialField]] = None  # Required credential fields

    def __post_init__(self):
        if self.credential_fields is None:
            self.credential_fields = []

class TTSManager:
    """Manages TTS engines and their instances"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engines = {
            "Azure TTS": {
                'class': MicrosoftClient,
                'requires_credentials': True,
                'credential_format': {'subscription_key': str, 'region': str},
                'credential_fields': [
                    CredentialField("subscription_key", "text", "API Key"),
                    CredentialField("region", "text", "Region")
                ],
                'requires_download': False
            },
            "Google TTS": {
                'class': GoogleClient,
                'requires_credentials': True,
                'credential_format': {'credentials_file': str},
                'credential_fields': [
                    CredentialField("credentials_file", "file", "Credentials File")
                ],
                'requires_download': False
            },
            "ElevenLabs": {
                'class': ElevenLabsClient,
                'requires_credentials': True,
                'credential_format': {'api_key': str},
                'credential_fields': [
                    CredentialField("api_key", "text", "API Key")
                ],
                'requires_download': False
            },
            "SherpaOnnx": {
                'class': SherpaOnnxClient,
                'requires_credentials': False,
                'credential_format': {},
                'credential_fields': []
            },
            "PlayHT": {
                'class': PlayHTClient,
                'requires_credentials': True,
                'credential_format': {'user_id': str, 'api_key': str},
                'credential_fields': [
                    CredentialField("user_id", "text", "User ID"),
                    CredentialField("api_key", "text", "API Key")
                ]
            },
            "GoogleTrans": {
                'class': GoogleTransClient,
                'requires_credentials': False,
                'credential_format': {},
                'credential_fields': []
            }
        }
        self.clients = {}
        self.tts_instances = {}  # Add this
        self.cred_mgr = CredentialManager(EncryptionManager())
        
        # Try to initialize Azure and Google with encrypted credentials
        try:
            azure_creds = self.cred_mgr.get_credentials("Azure TTS")
            if azure_creds:
                self.logger.info("Initializing Azure TTS with credentials")
                key, region = azure_creds
                self.logger.debug(f"Azure creds type: {type(azure_creds)}")
                self.logger.debug(f"Key type: {type(key)}, Region type: {type(region)}")
                self.logger.debug(f"Key value: {'*' * len(key)}, Region value: {region}")
                
                # Pass both key and region as a tuple to credentials
                client = MicrosoftClient(credentials=(key, region))
                
                # Test before storing
                voices = client.get_voices()
                if voices:
                    self.logger.info(f"Successfully got {len(voices)} voices")
                    self.clients["Azure TTS"] = client
                else:
                    raise ValueError("No voices returned after initialization")
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure TTS: {e}", exc_info=True)

        try:
            google_creds = self.cred_mgr.get_credentials("Google TTS")
            if google_creds:
                self.logger.info("Initializing Google TTS with credentials")
                creds_path = google_creds[0]
                client = GoogleClient(credentials=creds_path)  # Pass directly to constructor
                self.clients["Google TTS"] = client
                # Test if it worked
                voices = client.get_voices()
                self.logger.info(f"Initialized Google TTS with {len(voices)} voices")
        except Exception as e:
            self.logger.error(f"Failed to initialize Google TTS: {e}")

        # Initialize engines that don't need credentials
        for engine_name, engine_info in self.engines.items():
            if not engine_info['requires_credentials'] and engine_name not in self.clients:
                try:
                    self.clients[engine_name] = engine_info['class']()
                    self.logger.info(f"Initialized {engine_name} without credentials")
                except Exception as e:
                    self.logger.error(f"Failed to initialize {engine_name}: {e}")

    def initialize_engine(self, engine_name: str, credentials: Optional[dict] = None) -> None:
        """Initialize a TTS engine with credentials"""
        try:
            if engine_name not in self.engines:
                raise ValueError(f"Unknown engine: {engine_name}")
                
            engine_info = self.engines[engine_name]
            engine_class = engine_info['class']
            
            if credentials:
                # Log credentials for debugging (mask sensitive data)
                debug_creds = {k: '***' if 'key' in k.lower() else v 
                             for k, v in credentials.items()}
                self.logger.debug(f"Initializing {engine_name} with credentials: {debug_creds}")
                
                if engine_name == "Azure TTS":
                    # Pass credentials as a tuple
                    client = engine_class(credentials=(
                        credentials['subscription_key'],
                        credentials['region']
                    ))
                    self.clients[engine_name] = client
                elif engine_name == "Google TTS":
                    client = engine_class(credentials=credentials['credentials_file'])
                    self.clients[engine_name] = client
                else:
                    self.clients[engine_name] = engine_class(**credentials)
                    
                # Test if initialization worked
                voices = self.clients[engine_name].get_voices()
                self.logger.info(f"Initialized {engine_name} successfully with {len(voices)} voices")
                
            elif not engine_info['requires_credentials']:
                self.logger.debug(f"Initializing {engine_name} without credentials")
                self.clients[engine_name] = engine_class()
                
        except Exception as e:
            self.logger.error(f"Failed to initialize {engine_name}: {e}")
            raise

    def get_engine_names(self) -> List[str]:
        """Get list of available engine names"""
        return list(self.engines.keys())

    def get_voices(self, engine_name: str) -> List[Dict]:
        """Get available voices for an engine"""
        try:
            if engine_name not in self.clients:
                self.logger.error(f"Engine {engine_name} not initialized")
                return []
                
            client = self.clients[engine_name]
            return client.get_voices()
            
        except Exception as e:
            self.logger.error(f"Failed to get voices for {engine_name}: {e}")
            return []

    def _init_tts_instance(self, engine_name: str) -> None:
        """Initialize TTS instance for an engine"""
        if engine_name == "Azure TTS":
            self.tts_instances[engine_name] = MicrosoftTTS(self.clients[engine_name])
        elif engine_name == "Google TTS":
            self.tts_instances[engine_name] = GoogleTTS(self.clients[engine_name])
        elif engine_name == "ElevenLabs":
            self.tts_instances[engine_name] = ElevenLabsTTS(self.clients[engine_name])
        elif engine_name == "PlayHT":
            self.tts_instances[engine_name] = PlayHTTTS(self.clients[engine_name])
        elif engine_name == "SherpaOnnx":
            self.tts_instances[engine_name] = SherpaOnnxTTS(self.clients[engine_name])

    def preview_voice(self, engine_name: str, voice_id: str, text: str = "This is a preview.") -> None:
        """Preview a voice"""
        try:
            if engine_name not in self.tts_instances:
                self._init_tts_instance(engine_name)
                
            tts = self.tts_instances[engine_name]
            if engine_name == "SherpaOnnx":
                client = self.clients[engine_name]
                client._model_id = voice_id
                client.set_voice()
            else:
                tts.set_voice(voice_id)  # Set voice before preview
            tts.speak(text)
            
        except Exception as e:
            self.logger.error(f"Failed to preview voice {voice_id}: {e}")
            raise

    def requires_download(self, engine_name: str) -> bool:
        """Check if engine requires model download"""
        return self.engines[engine_name].get('requires_download', False)

    def queue_download(self, engine_name: str, voice_id: str) -> None:
        """Add a voice to the download queue"""
        self.download_queue.append((engine_name, voice_id))
        if not self.downloading:
            self.process_download_queue()

    def process_download_queue(self) -> None:
        """Process the next download in the queue"""
        if not self.download_queue:
            self.downloading = False
            return

        self.downloading = True
        engine_name, voice_id = self.download_queue[0]
        
        try:
            if engine_name == "SherpaOnnx":
                client = self.clients[engine_name]
                # Let client handle download and paths
                client.check_and_download_model(voice_id)
                
        except Exception as e:
            self.logger.error(f"Failed to download voice {voice_id}: {e}")
            raise
        finally:
            self.download_queue.pop(0)
            self.process_download_queue()

    def check_credentials(self):
        """Check and log credential status for all engines"""
        for engine_name in self.engines:
            try:
                creds = self.cred_mgr.get_credentials(engine_name)
                if creds:
                    self.logger.info(f"Found credentials for {engine_name}")
                    self.logger.debug(f"Credentials: {creds}")
                else:
                    self.logger.warning(f"No credentials found for {engine_name}")
            except Exception as e:
                self.logger.error(f"Error checking credentials for {engine_name}: {e}")

    def requires_credentials(self, engine_name: str) -> bool:
        """Check if engine requires credentials"""
        return self.engines[engine_name]['requires_credentials']
