#!/usr/bin/env python
"""
azure_transliteration.py - Azure Translator Transliteration API Module

This module provides transliteration functionality using the Azure Translator service.
Transliteration converts text from one script to another (e.g., Latin to Devanagari)
while maintaining the same language, unlike translation which converts meaning between languages.

The module integrates with the existing AACSpeakHelper configuration system and follows
the same patterns used for translation functionality.

Usage:
    from azure_transliteration import AzureTransliterator
    
    transliterator = AzureTransliterator(
        subscription_key="your_key",
        region="your_region"
    )
    
    result = transliterator.transliterate(
        text="namaste",
        language="mr",
        from_script="Latn",
        to_script="Deva"
    )

Author: Ace Centre
"""

import requests
import uuid
import logging
from typing import Dict, Optional


class AzureTransliterator:
    """
    Azure Translator Transliteration API client.
    
    This class handles transliteration requests to the Azure Translator service,
    converting text from one script to another within the same language.
    """
    
    def __init__(self, subscription_key: str, region: str):
        """
        Initialize the Azure Transliterator.
        
        Args:
            subscription_key (str): Azure Translator subscription key
            region (str): Azure resource region (e.g., "uksouth", "eastus")
        """
        self.subscription_key = subscription_key
        self.region = region
        self.endpoint = "https://api.cognitive.microsofttranslator.com"
        self.api_version = "3.0"
        
        # Validate credentials
        if not subscription_key or not region:
            raise ValueError("Both subscription_key and region are required")
    
    def transliterate(self, text: str, language: str, from_script: str, to_script: str) -> Optional[str]:
        """
        Transliterate text from one script to another.
        
        Args:
            text (str): Text to transliterate
            language (str): Language code (e.g., "mr" for Marathi, "hi" for Hindi)
            from_script (str): Source script code (e.g., "Latn" for Latin)
            to_script (str): Target script code (e.g., "Deva" for Devanagari)
            
        Returns:
            Optional[str]: Transliterated text, or None if transliteration failed
        """
        try:
            # Construct the API endpoint
            path = "/transliterate"
            params = {
                "api-version": self.api_version,
                "language": language,
                "fromScript": from_script,
                "toScript": to_script
            }
            url = self.endpoint + path
            
            # Prepare headers
            headers = {
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Ocp-Apim-Subscription-Region": self.region,
                "Content-type": "application/json",
                "X-ClientTraceId": str(uuid.uuid4())
            }
            
            # Prepare request body
            body = [{"text": text}]
            
            logging.info(f"Azure Transliteration: {language} {from_script}->{to_script}: {text}")
            
            # Make the API request
            response = requests.post(url, params=params, headers=headers, json=body, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0 and "text" in result[0]:
                    transliterated_text = result[0]["text"]
                    logging.info(f"Azure Transliteration result: {transliterated_text}")
                    return transliterated_text
                else:
                    logging.error(f"Azure Transliteration: Unexpected response format: {result}")
                    return None
            else:
                logging.error(f"Azure Transliteration API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Azure Transliteration network error: {e}")
            return None
        except Exception as e:
            logging.error(f"Azure Transliteration error: {e}", exc_info=True)
            return None
    
    def get_supported_languages(self) -> Optional[Dict]:
        """
        Get supported languages and scripts for transliteration.
        
        Returns:
            Optional[Dict]: Dictionary of supported languages and their scripts,
                          or None if the request failed
        """
        try:
            # Use the languages endpoint to get transliteration support
            url = f"{self.endpoint}/languages"
            params = {"api-version": self.api_version, "scope": "transliteration"}
            
            headers = {
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Ocp-Apim-Subscription-Region": self.region,
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("transliteration", {})
            else:
                logging.error(f"Azure Languages API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting supported languages: {e}", exc_info=True)
            return None


def transliterate_text(text: str, config, language: str = None, from_script: str = None, to_script: str = None) -> Optional[str]:
    """
    Convenience function to transliterate text using configuration settings.
    
    This function integrates with the AACSpeakHelper configuration system,
    following the same patterns as the translation functionality.
    
    Args:
        text (str): Text to transliterate
        config: Configuration object (ConfigParser)
        language (str, optional): Language code, defaults to config setting
        from_script (str, optional): Source script, defaults to config setting
        to_script (str, optional): Target script, defaults to config setting
        
    Returns:
        Optional[str]: Transliterated text, or None if transliteration failed
    """
    try:
        # Get credentials from transliterate section first, fallback to translate section
        subscription_key = config.get("transliterate", "microsoft_transliterator_secret_key", fallback="")
        region = config.get("transliterate", "region", fallback="")

        # Fallback to translate section for backward compatibility
        if not subscription_key:
            subscription_key = config.get("translate", "microsoft_translator_secret_key", fallback="")
        if not region:
            region = config.get("translate", "region", fallback="")

        if not subscription_key or not region:
            logging.error("Azure transliteration credentials not found in [transliterate] or [translate] configuration sections")
            return None
        
        # Get transliteration settings from config
        if not language:
            language = config.get("transliterate", "language", fallback="")
        if not from_script:
            from_script = config.get("transliterate", "from_script", fallback="")
        if not to_script:
            to_script = config.get("transliterate", "to_script", fallback="")
        
        if not all([language, from_script, to_script]):
            logging.error("Transliteration settings incomplete: language, from_script, and to_script are required")
            return None
        
        # Create transliterator and perform transliteration
        transliterator = AzureTransliterator(subscription_key, region)
        return transliterator.transliterate(text, language, from_script, to_script)
        
    except Exception as e:
        logging.error(f"Transliteration error: {e}", exc_info=True)
        return None


# Common language and script mappings for transliteration
TRANSLITERATION_LANGUAGES = {
    "Arabic": "ar",
    "Bengali": "bn", 
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Oriya": "or",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur"
}

TRANSLITERATION_SCRIPTS = {
    "Latin": "Latn",
    "Arabic": "Arab", 
    "Devanagari": "Deva",
    "Bengali": "Beng",
    "Gujarati": "Gujr",
    "Gurmukhi": "Guru",
    "Kannada": "Knda",
    "Malayalam": "Mlym",
    "Oriya": "Orya",
    "Tamil": "Taml",
    "Telugu": "Telu"
}

# Script combinations commonly used for transliteration
COMMON_SCRIPT_PAIRS = [
    ("Latn", "Deva"),  # Latin to Devanagari (Hindi, Marathi, etc.)
    ("Latn", "Arab"),  # Latin to Arabic
    ("Latn", "Beng"),  # Latin to Bengali
    ("Latn", "Gujr"),  # Latin to Gujarati
    ("Latn", "Guru"),  # Latin to Gurmukhi (Punjabi)
    ("Latn", "Knda"),  # Latin to Kannada
    ("Latn", "Mlym"),  # Latin to Malayalam
    ("Latn", "Orya"),  # Latin to Oriya
    ("Latn", "Taml"),  # Latin to Tamil
    ("Latn", "Telu"),  # Latin to Telugu
    ("Deva", "Latn"),  # Devanagari to Latin
    ("Arab", "Latn"),  # Arabic to Latin
]
