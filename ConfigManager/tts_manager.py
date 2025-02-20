# File: tts_manager.py
from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from tts_wrapper import MicrosoftTTS, MicrosoftClient  # type: ignore
from tts_wrapper import GoogleTTS, GoogleClient  # type: ignore
from tts_wrapper import ElevenLabsTTS, ElevenLabsClient  # type: ignore
from tts_wrapper import PlayHTTTS, PlayHTClient  # type: ignore
from tts_wrapper import SherpaOnnxTTS, SherpaOnnxClient  # type: ignore

@dataclass
class CredentialField:
    """Defines a credential field requirement"""
    name: str
    field_type: str  # "text", "file", or "region"
    label: str

@dataclass
class TTSConfig:
    """Configuration for a TTS engine"""
    name: str
    tts_class: type
    client_class: type
    requires_download: bool = False
    requires_credentials: bool = True
    credential_fields: Optional[List[CredentialField]] = None

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

    def initialize_engine(self, engine_name: str, credentials: tuple) -> bool:
        """Initialize a TTS engine with credentials"""
        try:
            if engine_name not in self.engines:
                raise ValueError(f"Unknown engine: {engine_name}")

            config = self.engines[engine_name]
            
            # Create client - handle SherpaOnnx differently
            if engine_name == "SherpaOnnx":
                client = config.client_class()  # No credentials needed
            else:
                client = config.client_class(credentials=credentials)
            
            self.clients[engine_name] = client
            
            # Create TTS instance
            tts = config.tts_class(client)
            self.tts_instances[engine_name] = tts
            
            self.initialized[engine_name] = True
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize {engine_name}: {e}")
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

    def preview_voice(
        self, 
        engine_name: str, 
        voice_id: str, 
        text: str = "This is a preview."
    ) -> None:
        """Preview a voice"""
        try:
            if engine_name not in self.tts_instances:
                raise ValueError(f"Engine {engine_name} not initialized")
                
            tts = self.tts_instances[engine_name]
            tts.set_voice(voice_id)  # type: ignore
            tts.speak(text)  # type: ignore
            
        except Exception as e:
            logging.error(f"Failed to preview voice {voice_id}: {e}")
            raise

    def get_engine_names(self) -> List[str]:
        """Get list of available engine names"""
        return list(self.engines.keys())

    def requires_download(self, engine_name: str) -> bool:
        """Check if engine requires model download"""
        return self.engines[engine_name].requires_download
