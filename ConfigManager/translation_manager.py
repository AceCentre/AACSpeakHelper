# File: translation_manager.py
"""Translation manager for handling different translation engines."""
from typing import Dict, List, Optional
from dataclasses import dataclass
from deep_translator import (
    GoogleTranslator,
    DeeplTranslator,
    MyMemoryTranslator,
    LibreTranslator,
    MicrosoftTranslator
)
import logging

@dataclass
class TranslatorConfig:
    """Configuration for a translation engine"""
    name: str
    translator_class: type
    requires_api_key: bool = False
    supports_languages: bool = True  # Whether engine provides language list
    base_url: Optional[str] = None  # For self-hosted services like LibreTranslate

class TranslationManager:
    """Manages translation engines and their instances"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.translators = {
            "Google": TranslatorConfig(
                name="Google",
                translator_class=GoogleTranslator,
                requires_api_key=False
            ),
            "Microsoft": TranslatorConfig(
                name="Microsoft",
                translator_class=MicrosoftTranslator,
                requires_api_key=True
            ),
            "DeepL": TranslatorConfig(
                name="DeepL",
                translator_class=DeeplTranslator,
                requires_api_key=True
            ),
            "MyMemory": TranslatorConfig(
                name="MyMemory",
                translator_class=MyMemoryTranslator,
                requires_api_key=False
            ),
            "LibreTranslate": TranslatorConfig(
                name="LibreTranslate",
                translator_class=LibreTranslator,
                requires_api_key=True,
                base_url="https://libretranslate.com"
            )
        }
        self.instances: Dict[str, any] = {}
        
        # Initialize Google translator by default since it doesn't need credentials
        self.initialize_translator("Google")
        
    def initialize_translator(
        self, 
        translator_name: str, 
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> bool:
        """Initialize a translation engine"""
        try:
            if translator_name not in self.translators:
                raise ValueError(f"Unknown translator: {translator_name}")
                
            config = self.translators[translator_name]
            
            # Build initialization kwargs
            kwargs = {}
            if config.requires_api_key and api_key:
                kwargs['api_key'] = api_key
            if config.base_url or base_url:
                kwargs['base_url'] = base_url or config.base_url
                
            # Initialize translator
            self.instances[translator_name] = config.translator_class(**kwargs)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize {translator_name}: {e}")
            return False
            
    def get_supported_languages(self, translator_name: str) -> List[Dict[str, str]]:
        """Get list of supported languages for a translator"""
        try:
            if not translator_name in self.instances:
                raise ValueError(f"Translator {translator_name} not initialized")
                
            translator = self.instances[translator_name]
            languages = translator.get_supported_languages(as_dict=True)
            
            return [
                {"code": code, "name": name}
                for code, name in languages.items()
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get languages for {translator_name}: {e}")
            return []
            
    def translate(
        self,
        text: str,
        translator_name: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> str:
        """Translate text using specified engine"""
        try:
            if not translator_name in self.instances:
                raise ValueError(f"Translator {translator_name} not initialized")
                
            translator = self.instances[translator_name]
            return translator.translate(
                text,
                source=source_lang,
                target=target_lang
            )
            
        except Exception as e:
            self.logger.error(f"Translation failed: {e}")
            raise
