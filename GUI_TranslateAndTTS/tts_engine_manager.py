from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Type
from PySide6.QtWidgets import (
    QListWidget, QLineEdit, QLabel, QWidget, 
    QVBoxLayout, QPushButton, QListWidgetItem
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
import logging
from configure_enc_utils import load_credentials
import os
import base64
import tempfile

# Import all TTS engine classes
from tts_wrapper import (
    SherpaOnnxTTS, SherpaOnnxClient,
    MicrosoftTTS, MicrosoftClient,
    GoogleTransTTS, GoogleTransClient,
    PlayHTClient, PlayHTTTS,
    ElevenLabsTTS, ElevenLabsClient
)

@dataclass
class TTSEngineDefinition:
    """Complete definition of a TTS engine"""
    id: str                     # Internal ID (e.g. "microsoft")
    ui_name: str                # Display name in UI (e.g. "Azure TTS")
    engine_id: str              # Class name (e.g. "MicrosoftTTS")
    client_class: Type          # The client class
    tts_class: Type            # The TTS class
    needs_download: bool = False
    credential_fields: List[str] = None
    page_name: str = None       # UI page name (e.g. "azure_page")

# Single source of truth for all engine definitions
TTS_ENGINES = {
    "microsoft": TTSEngineDefinition(
        id="microsoft",
        ui_name="Azure TTS",
        engine_id="MicrosoftTTS",
        client_class=MicrosoftClient,
        tts_class=MicrosoftTTS,
        credential_fields=["key", "region"],
        page_name="azure_page"
    ),
    "google": TTSEngineDefinition(
        id="google",
        ui_name="Google TTS",
        engine_id="GoogleTTS",
        client_class=GoogleTransClient,
        tts_class=GoogleTransTTS,
        credential_fields=["creds_path"],
        page_name="gTTS_page"
    ),
    "sherpa": TTSEngineDefinition(
        id="sherpa",
        ui_name="Sherpa-ONNX",
        engine_id="SherpaOnnxTTS",
        client_class=SherpaOnnxClient,
        tts_class=SherpaOnnxTTS,
        needs_download=True,
        page_name="onnx_page"
    ),
    "google_trans": TTSEngineDefinition(
        id="google_trans",
        ui_name="Google Trans",
        engine_id="GoogleTransTTS",
        client_class=GoogleTransClient,
        tts_class=GoogleTransTTS,
        page_name="gspeak_page"
    ),
    "elevenlabs": TTSEngineDefinition(
        id="elevenlabs",
        ui_name="ElevenLabs",
        engine_id="ElevenLabsTTS",
        client_class=ElevenLabsClient,
        tts_class=ElevenLabsTTS,
        credential_fields=["api_key"],
        page_name="elevenlabs_page"
    ),
    "playht": TTSEngineDefinition(
        id="playht",
        ui_name="PlayHT",
        engine_id="PlayHTTTS",
        client_class=PlayHTClient,
        tts_class=PlayHTTTS,
        credential_fields=["api_key", "user_id"],
        page_name="playht_page"
    )
}

class TTSEngineHandler:
    """Handles UI and logic for a specific TTS engine"""
    def __init__(self, 
                 config: TTSEngineDefinition,
                 list_widget: QListWidget,
                 search_box: QLineEdit,
                 no_creds_label: Optional[QLabel] = None,
                 icons: Optional[Dict[str, QIcon]] = None):
        self.config = config
        self.list_widget = list_widget
        self.search_box = search_box
        self.no_creds_label = no_creds_label
        self.client = None
        self.tts = None
        self.icons = icons or {}
        self.model_path = None  # Add this to store model path
        
        # Set placeholder text
        self.search_box.setPlaceholderText(f"Search {config.ui_name} voices...")
        
        # Load default credentials from encrypted config
        self.default_credentials = self.load_default_credentials()

    def load_default_credentials(self) -> Dict[str, str]:
        """Load default credentials from encrypted config"""
        try:
            if self.config.engine_id == "MicrosoftTTS":
                return {
                    "key": os.environ.get('MICROSOFT_TOKEN', ''),
                    "region": os.environ.get('MICROSOFT_REGION', '')
                }
            elif self.config.engine_id == "GoogleTTS":
                google_creds = os.environ.get('GOOGLE_CREDS_JSON')
                if google_creds:
                    return {"creds_json": base64.b64decode(google_creds)}
            return {}
        except Exception as e:
            logging.error(f"Error loading default credentials for {self.config.ui_name}: {e}")
            return {}

    def initialize(self, ui_credentials: Optional[Dict[str, str]] = None) -> bool:
        """Initialize the TTS client with credentials"""
        try:
            # Special cases for engines that don't use credentials
            if self.config.engine_id in ["SherpaOnnxTTS", "GoogleTransTTS"]:
                if self.config.engine_id == "SherpaOnnxTTS":
                    model_path = ui_credentials.get('model_path', '') if ui_credentials else ''
                    self.client = self.config.client_class(model_path=model_path)
                else:  # GoogleTransTTS
                    self.client = self.config.client_class()  # No credentials needed
                self.tts = self.config.tts_class(self.client)
                self.load_voices()
                return True

            # Use UI credentials if provided, otherwise fall back to defaults
            credentials = ui_credentials if ui_credentials else self.default_credentials
            
            if not any(credentials.values()) and self.config.credential_fields:
                logging.warning(f"No credentials available for {self.config.ui_name}")
                if self.no_creds_label:
                    self.no_creds_label.show()
                    self.list_widget.hide()
                return False

            # Special handling for Google which needs temp file
            if self.config.engine_id == "GoogleTTS" and "creds_json" in credentials:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_creds:
                    temp_creds.write(credentials["creds_json"])
                    temp_creds.close()
                    credentials = {"creds_path": temp_creds.name}

            self.client = self.config.client_class(credentials=tuple(credentials.values()))
            self.tts = self.config.tts_class(self.client)
            
            if self.no_creds_label:
                self.no_creds_label.hide()
                self.list_widget.show()
                
            self.load_voices()
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize {self.config.ui_name}: {e}")
            if self.no_creds_label:
                self.no_creds_label.show()
                self.list_widget.hide()
            return False

    def load_voices(self):
        """Load and display available voices"""
        try:
            voices = self.tts.get_voices()
            self.list_widget.clear()
            for voice in voices:
                self.add_voice_to_list(voice)
        except Exception as e:
            logging.error(f"Error loading voices for {self.config.ui_name}: {e}")

    def filter_voices(self, search_text: str):
        """Filter voices based on search text"""
        try:
            if not self.tts:
                return
            
            voices = self.tts.get_voices()
            self.list_widget.clear()
            
            search_text = search_text.lower()
            for voice in voices:
                # Search in name, language codes and gender
                searchable_text = (
                    f"{voice.get('name', '')} "
                    f"{' '.join(voice.get('language_codes', []))} "
                    f"{voice.get('gender', '')}"
                ).lower()
                
                if search_text in searchable_text:
                    self.add_voice_to_list(voice)
        except Exception as e:
            logging.error(f"Error filtering voices for {self.config.ui_name}: {e}")

    def add_voice_to_list(self, voice: Dict[str, Any]):
        """Add a voice to the list widget with standardized format"""
        try:
            item_widget = QWidget()
            layout = QVBoxLayout(item_widget)
            
            # Create name label with language codes
            name_text = f"{voice['name']} ({', '.join(voice['language_codes'])})"
            if voice.get('gender'):
                name_text += f" - {voice['gender']}"
                
            name_label = QLabel(name_text)
            name_label.setFont(QFont("", 12))
            layout.addWidget(name_label)
            
            # Create list item
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            item.setData(Qt.UserRole, voice)
            
            # Add preview/download button based on engine type
            if self.config.needs_download:
                self.add_download_button(item_widget, voice, layout)
            else:
                self.add_preview_button(item_widget, voice, layout)
            
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)
            
        except Exception as e:
            logging.error(f"Error adding voice to list: {e}")

    def add_preview_button(self, item_widget: QWidget, voice: Dict[str, Any], layout: QVBoxLayout):
        """Add preview button for standard voices"""
        preview_btn = QPushButton("Preview")
        if 'preview' in self.icons:
            preview_btn.setIcon(self.icons['preview'])
        preview_btn.clicked.connect(lambda: self.preview_voice(voice['id']))
        layout.addWidget(preview_btn)

    def add_download_button(self, item_widget: QWidget, voice: Dict[str, Any], layout: QVBoxLayout):
        """Add download button for downloadable voices"""
        is_downloaded = self.check_if_downloaded(voice['id'])
        btn = QPushButton("Preview" if is_downloaded else "Download")
        btn.setIcon(self.icons.get('preview' if is_downloaded else 'download'))
        btn.clicked.connect(
            lambda: self.preview_voice(voice['id']) if is_downloaded 
            else self.download_voice(voice['id'])
        )
        layout.addWidget(btn)

    def check_if_downloaded(self, voice_id: str) -> bool:
        """Check if a voice model is downloaded"""
        if not self.config.needs_download:
            return True
            
        try:
            if not self.model_path:
                return False
                
            model_path = os.path.join(self.model_path, f"{voice_id}", "model.onnx")
            tokens_path = os.path.join(self.model_path, f"{voice_id}", "tokens.txt")
            return os.path.exists(model_path) and os.path.exists(tokens_path)
        except Exception as e:
            logging.error(f"Error checking if voice {voice_id} is downloaded: {e}")
            return False
            
    def set_model_path(self, path: str):
        """Set the path where models are stored"""
        self.model_path = path 