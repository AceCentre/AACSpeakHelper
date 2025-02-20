# File: tts_manager.py
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
from tts_wrapper import (
    MicrosoftTTS, MicrosoftClient,
    GoogleTTS, GoogleClient,
    ElevenLabsTTS, ElevenLabsClient,
    PlayHTTTS, PlayHTClient,
    SherpaOnnxTTS, SherpaOnnxClient
)
from pathlib import Path

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
            "Microsoft": TTSConfig(
                name="Microsoft",
                tts_class=MicrosoftTTS,
                client_class=MicrosoftClient,
                credential_fields=[
                    CredentialField("subscription_key", "text", "API Key"),
                    CredentialField("subscription_region", "region", "Region")
                ]
            ),
            "Google": TTSConfig(
                name="Google",
                tts_class=GoogleTTS,
                client_class=GoogleClient,
                credential_fields=[
                    CredentialField("credentials_file", "file", "Service Account JSON")
                ]
            ),
            "PlayHT": TTSConfig(
                name="PlayHT",
                tts_class=PlayHTTTS,
                client_class=PlayHTClient,
                credential_fields=[
                    CredentialField("api_key", "text", "API Key"),
                    CredentialField("user_id", "text", "User ID")
                ]
            ),
            "ElevenLabs": TTSConfig(
                name="ElevenLabs",
                tts_class=ElevenLabsTTS,
                client_class=ElevenLabsClient,
                credential_fields=[
                    CredentialField("api_key", "text", "API Key")
                ]
            ),
            "SherpaOnnx": TTSConfig(
                name="SherpaOnnx",
                tts_class=SherpaOnnxTTS,
                client_class=SherpaOnnxClient,
                requires_download=True,
                requires_credentials=False
            )
        }
        self.clients: Dict[str, Any] = {}
        self.tts_instances: Dict[str, Any] = {}
        self.initialized: Dict[str, bool] = {name: False for name in self.engines}
        self.download_queue = []
        self.downloading = False

    def initialize_engine(self, engine_name: str, credentials: tuple) -> bool:
        """Initialize a TTS engine with credentials or default settings"""
        try:
            if engine_name not in self.engines:
                raise ValueError(f"Unknown engine: {engine_name}")

            config = self.engines[engine_name]
            
            if engine_name == "SherpaOnnx":
                # Get base directory
                try:
                    from configparser import ConfigParser
                    cfg = ConfigParser()
                    cfg.read('settings.cfg')
                    base_dir = Path(cfg.get('TTS', 'base_dir'))
                except:
                    base_dir = Path.home() / "mms_models"
                
                base_dir.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Initializing SherpaOnnx with base dir: {base_dir}")
                
                # Initialize with no_default_download=True to prevent auto-downloads
                client = config.client_class(
                    model_path=str(base_dir),
                    no_default_download=True
                )
            else:
                client = config.client_class(credentials=credentials)
            
            self.clients[engine_name] = client
            self.tts_instances[engine_name] = config.tts_class(client)
            self.initialized[engine_name] = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize {engine_name}: {e}")
            return False

    def get_voices(self, engine_name: str) -> List[dict]:
        """Get available voices for an engine"""
        try:
            if engine_name not in self.tts_instances:
                raise ValueError(f"Engine {engine_name} not initialized")
            
            tts = self.tts_instances[engine_name]
            return tts.get_voices()  # type: ignore
            
        except Exception as e:
            logging.error(f"Failed to get voices for {engine_name}: {e}")
            return []

    def preview_voice(self, engine_name: str, voice_id: str, text: str = "This is a preview.") -> None:
        """Preview a voice"""
        try:
            if engine_name == "SherpaOnnx":
                client = self.clients[engine_name]
                tts = self.tts_instances[engine_name]
                # Set voice ID before preview
                client._model_id = voice_id
                client.set_voice()
                tts.speak(text)
            else:
                if engine_name not in self.tts_instances:
                    raise ValueError(f"Engine {engine_name} not initialized")
                tts = self.tts_instances[engine_name]
                tts.speak(text)
            
        except Exception as e:
            self.logger.error(f"Failed to preview voice {voice_id}: {e}")
            raise

    def get_engine_names(self) -> List[str]:
        """Get list of available engine names"""
        return list(self.engines.keys())

    def requires_download(self, engine_name: str) -> bool:
        """Check if engine requires model download"""
        return self.engines[engine_name].requires_download

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
