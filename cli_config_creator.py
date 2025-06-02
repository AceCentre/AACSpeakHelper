#!/usr/bin/env python
# cli_config_creator.py
# A simple CLI configuration tool for AACSpeakHelper

import os
import sys
import configparser
import argparse
from pathlib import Path
import json

# Import language dictionaries
try:
    from GUI_TranslateAndTTS.language_dictionary import (
        Google_Translator,
        MyMemory_Translator,
        Libre_Translator,
        DeepL_Translator,
        Microsoft_Translator,
        Pons_Translator,
        Linguee_Translator,
        Papago_Translator,
        Qcri_Translator,
        Baidu_Translator,
        Yandex_Translator,
        azure_tts_list,
        google_TTS_list,
        gSpeak_TTS_list,
    )
except ImportError:
    # Fallback to direct import if not running as a module
    try:
        from language_dictionary import (
            Google_Translator,
            MyMemory_Translator,
            Libre_Translator,
            DeepL_Translator,
            Microsoft_Translator,
            Pons_Translator,
            Linguee_Translator,
            Papago_Translator,
            Qcri_Translator,
            Baidu_Translator,
            Yandex_Translator,
            azure_tts_list,
            google_TTS_list,
            gSpeak_TTS_list,
        )
    except ImportError:
        print("Warning: Language dictionaries not found. Some features may be limited.")
        # Create minimal dictionaries for testing
        Google_Translator = {"English": "en", "Spanish": "es", "French": "fr"}
        azure_tts_list = {
            "English (United States)": "en-US",
            "Spanish (Spain)": "es-ES",
        }
        google_TTS_list = {
            "English (United States)": "en-US",
            "Spanish (Spain)": "es-ES",
        }
        gSpeak_TTS_list = {"English": "en", "Spanish": "es"}
        # Define other dictionaries as empty
        MyMemory_Translator = {}
        Libre_Translator = {}
        DeepL_Translator = {}
        Microsoft_Translator = {}
        Pons_Translator = {}
        Linguee_Translator = {}
        Papago_Translator = {}
        Qcri_Translator = {}
        Baidu_Translator = {}
        Yandex_Translator = {}

# Define TTS engines
TTS_ENGINES = {
    "azure": {
        "name": "Azure TTS",
        "config_section": "azureTTS",
        "credential_fields": ["key", "location"],
        "voice_list": azure_tts_list,
    },
    "google": {
        "name": "Google TTS",
        "config_section": "googleTTS",
        "credential_fields": ["creds"],
        "voice_list": google_TTS_list,
    },
    "sherpa": {
        "name": "Sherpa-ONNX",
        "config_section": "SherpaOnnxTTS",
        "credential_fields": [],
        "voice_list": {"English": "eng", "Chinese": "cmn"},
    },
    "google_trans": {
        "name": "Google Trans",
        "config_section": "googleTransTTS",
        "credential_fields": [],
        "voice_list": gSpeak_TTS_list,
    },
    "elevenlabs": {
        "name": "ElevenLabs",
        "config_section": "ElevenLabsTTS",
        "credential_fields": ["api_key"],
        "voice_list": {},  # ElevenLabs voices are fetched from API
    },
    "playht": {
        "name": "PlayHT",
        "config_section": "PlayHTTTS",
        "credential_fields": ["api_key", "user_id"],
        "voice_list": {},  # PlayHT voices are fetched from API
    },
}

# Define translation providers
TRANSLATION_PROVIDERS = {
    "google": {
        "name": "GoogleTranslator",
        "credential_fields": [],
        "language_list": Google_Translator,
    },
    "microsoft": {
        "name": "MicrosoftTranslator",
        "credential_fields": ["microsoft_translator_secret_key", "region"],
        "language_list": Microsoft_Translator,
    },
    "deepl": {
        "name": "DeeplTranslator",
        "credential_fields": ["deep_l_translator_secret_key", "deepl_pro"],
        "language_list": DeepL_Translator,
    },
    "mymemory": {
        "name": "MyMemoryTranslator",
        "credential_fields": ["my_memory_translator_secret_key", "email"],
        "language_list": MyMemory_Translator,
    },
    "libre": {
        "name": "LibreTranslator",
        "credential_fields": ["libre_translator_secret_key", "url"],
        "language_list": Libre_Translator,
    },
    "papago": {
        "name": "PapagoTranslator",
        "credential_fields": [
            "papago_translator_client_id",
            "papago_translator_secret_key",
        ],
        "language_list": Papago_Translator,
    },
    "yandex": {
        "name": "YandexTranslator",
        "credential_fields": ["yandex_translator_secret_key"],
        "language_list": Yandex_Translator,
    },
    "qcri": {
        "name": "QcriTranslator",
        "credential_fields": ["qcri_translator_secret_key"],
        "language_list": Qcri_Translator,
    },
    "baidu": {
        "name": "BaiduTranslator",
        "credential_fields": ["baidu_translator_appid", "baidu_translator_secret_key"],
        "language_list": Baidu_Translator,
    },
    "pons": {
        "name": "PonsTranslator",
        "credential_fields": [],
        "language_list": Pons_Translator,
    },
    "linguee": {
        "name": "LingueeTranslator",
        "credential_fields": [],
        "language_list": Linguee_Translator,
    },
}


def get_config_dir():
    """Get the configuration directory path"""
    if getattr(sys, "frozen", False):
        config_dir = os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Roaming",
            "Ace Centre",
            "AACSpeakHelper",
        )
    else:
        config_dir = os.path.dirname(os.path.abspath(__file__))

    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def load_config(custom_config_path=None):
    """Load configuration from file"""
    config = configparser.ConfigParser()

    if custom_config_path and os.path.exists(custom_config_path):
        config_path = custom_config_path
    else:
        config_path = os.path.join(get_config_dir(), "settings.cfg")

    if os.path.exists(config_path):
        config.read(config_path)
        print(f"Configuration loaded from {config_path}")
    else:
        print("No existing configuration found. Creating default configuration.")
        create_default_config(config)

    return config, config_path


def create_default_config(config):
    """Create a default configuration"""
    # Add default sections and values
    config["App"] = {"collectstats": "True", "uuid": ""}

    config["translate"] = {
        "no_translate": "False",
        "notranslate": "False",
        "start_lang": "en",
        "startlang": "en",
        "end_lang": "en",
        "endlang": "en",
        "replace_pb": "True",
        "provider": "GoogleTranslator",
        "microsoft_translator_secret_key": "",
        "papago_translator_client_id": "",
        "papago_translator_secret_key": "",
        "my_memory_translator_secret_key": "",
        "email": "",
        "libre_translator_secret_key": "",
        "url": "",
        "deep_l_translator_secret_key": "",
        "deepl_pro": "false",
        "region": "",
        "yandex_translator_secret_key": "",
        "qcri_translator_secret_key": "",
        "baidu_translator_appid": "",
        "baidu_translator_secret_key": "",
    }

    config["TTS"] = {
        "engine": "SherpaOnnxTTS",
        "bypass_tts": "False",
        "save_audio_file": "True",
        "rate": "0",
        "volume": "100",
        "voice_id": "eng",
    }

    config["azureTTS"] = {"key": "", "location": "", "voice_id": "en-US-JennyNeural"}

    config["googleTTS"] = {"creds": "", "voice_id": "en-US-Wavenet-C"}

    config["googleTransTTS"] = {"voice_id": ""}

    config["sapi5TTS"] = {
        "voice_id": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
    }

    config["SherpaOnnxTTS"] = {"voice_id": "eng"}

    config["appCache"] = {"threshold": "7"}

    return config


def save_config(config, config_path):
    """Save configuration to file"""
    with open(config_path, "w") as configfile:
        config.write(configfile)
    print(f"Configuration saved to {config_path}")


def print_menu(config):
    """Print the main menu with current configuration summary"""
    print("\n===== AACSpeakHelper Configuration Tool =====")

    # Display current TTS configuration
    tts_engine = config.get("TTS", "engine", fallback="Not configured")
    tts_voice = "Not configured"

    # Get the voice ID from the appropriate section based on the engine
    # The engine name in config is now the section name, so use it directly
    if tts_engine in ["azureTTS", "Azure TTS"]:
        tts_voice = config.get("azureTTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["googleTTS", "Google TTS"]:
        tts_voice = config.get("googleTTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["SherpaOnnxTTS", "Sherpa-ONNX"]:
        tts_voice = config.get("SherpaOnnxTTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["googleTransTTS", "Google Trans"]:
        tts_voice = config.get("googleTransTTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["ElevenLabsTTS", "ElevenLabs"]:
        tts_voice = config.get("ElevenLabsTTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["PlayHTTTS", "PlayHT"]:
        tts_voice = config.get("PlayHTTTS", "voice_id", fallback="Not configured")

    # Display current translation configuration
    trans_provider = config.get("translate", "provider", fallback="Not configured")
    trans_source = config.get("translate", "start_lang", fallback="Not configured")
    trans_target = config.get("translate", "end_lang", fallback="Not configured")

    # Display the configuration summary
    print("\nCurrent Configuration:")
    print(f"TTS Engine: {tts_engine}")
    print(f"TTS Voice: {tts_voice}")
    print(f"Translation Provider: {trans_provider}")
    print(f"Translation: {trans_source} → {trans_target}")

    print("\nOptions:")
    print("1. Configure TTS")
    print("2. Configure Translation")
    print("3. View Full Configuration")
    print("4. Save and Exit")
    print("5. Exit without Saving")
    print("===========================================")


def configure_tts(config):
    """Configure TTS settings"""
    print("\n===== TTS Configuration =====")
    print("Available TTS Engines:")

    # Display available engines
    engines = list(TTS_ENGINES.keys())
    for i, engine_key in enumerate(engines):
        print(f"{i+1}. {TTS_ENGINES[engine_key]['name']}")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect TTS engine (number): ")) - 1
            if 0 <= choice < len(engines):
                selected_engine = engines[choice]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

    # Update the main TTS engine setting
    # Use the config section name instead of display name for the engine
    engine_section = TTS_ENGINES[selected_engine]["config_section"]
    engine_name = TTS_ENGINES[selected_engine]["name"]
    config.set("TTS", "engine", engine_section)
    print(f"Selected TTS engine: {engine_name} (config: {engine_section})")

    # Configure engine-specific settings
    engine_config = TTS_ENGINES[selected_engine]
    section_name = engine_config["config_section"]

    # Ensure the section exists
    if not config.has_section(section_name):
        config.add_section(section_name)

    # Configure credentials if needed
    for field in engine_config["credential_fields"]:
        current_value = config.get(section_name, field, fallback="")
        new_value = input(f"Enter {field} [{current_value}]: ") or current_value
        config.set(section_name, field, new_value)

    # Configure voice
    configure_voice(config, selected_engine)

    return config


def configure_voice(config, engine_key):
    """Configure voice for the selected TTS engine"""
    engine_config = TTS_ENGINES[engine_key]
    section_name = engine_config["config_section"]
    voice_list = engine_config["voice_list"]

    if not voice_list:
        print("Voice list not available for this engine.")
        voice_id = input("Enter voice ID manually: ")
        config.set(section_name, "voice_id", voice_id)
        return

    # Allow searching by language
    search_term = input(
        "Search for a voice by language name (or press Enter to see all): "
    ).lower()

    matching_voices = []
    for voice_name, voice_id in voice_list.items():
        if search_term in voice_name.lower():
            matching_voices.append((voice_name, voice_id))

    if not matching_voices:
        print("No matching voices found.")
        return

    print("\nMatching voices:")
    for i, (voice_name, voice_id) in enumerate(matching_voices):
        print(f"{i+1}. {voice_name} ({voice_id})")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect voice (number): ")) - 1
            if 0 <= choice < len(matching_voices):
                selected_voice = matching_voices[choice]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

    # Update the voice ID
    voice_name, voice_id = selected_voice
    config.set(section_name, "voice_id", voice_id)
    print(f"Selected voice: {voice_name} ({voice_id})")

    return config


def configure_translation(config):
    """Configure translation settings"""
    print("\n===== Translation Configuration =====")
    print("Available Translation Providers:")

    # Display available providers
    providers = list(TRANSLATION_PROVIDERS.keys())
    for i, provider_key in enumerate(providers):
        print(f"{i+1}. {TRANSLATION_PROVIDERS[provider_key]['name']}")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect translation provider (number): ")) - 1
            if 0 <= choice < len(providers):
                selected_provider = providers[choice]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

    # Update the provider setting
    provider_name = TRANSLATION_PROVIDERS[selected_provider]["name"]
    config.set("translate", "provider", provider_name)
    print(f"Selected translation provider: {provider_name}")

    # Configure provider-specific settings
    provider_config = TRANSLATION_PROVIDERS[selected_provider]

    # Configure credentials if needed
    for field in provider_config["credential_fields"]:
        current_value = config.get("translate", field, fallback="")
        new_value = input(f"Enter {field} [{current_value}]: ") or current_value
        config.set("translate", field, new_value)

    # Configure languages
    configure_languages(config, selected_provider)

    return config


def configure_languages(config, provider_key):
    """Configure source and target languages for translation"""
    provider_config = TRANSLATION_PROVIDERS[provider_key]
    language_list = provider_config["language_list"]

    if not language_list:
        print("Language list not available for this provider.")
        start_lang = input("Enter source language code manually: ")
        end_lang = input("Enter target language code manually: ")
        config.set("translate", "start_lang", start_lang)
        config.set("translate", "end_lang", end_lang)
        return

    # Configure source language
    print("\nAvailable source languages:")
    languages = list(language_list.items())
    for i, (lang_name, lang_code) in enumerate(languages):
        print(f"{i+1}. {lang_name} ({lang_code})")

    # Get user selection for source language
    while True:
        try:
            choice = int(input("\nSelect source language (number): ")) - 1
            if 0 <= choice < len(languages):
                selected_lang = languages[choice]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

    # Update the source language
    lang_name, lang_code = selected_lang
    config.set("translate", "start_lang", lang_code)
    print(f"Selected source language: {lang_name} ({lang_code})")

    # Configure target language
    print("\nAvailable target languages:")
    for i, (lang_name, lang_code) in enumerate(languages):
        print(f"{i+1}. {lang_name} ({lang_code})")

    # Get user selection for target language
    while True:
        try:
            choice = int(input("\nSelect target language (number): ")) - 1
            if 0 <= choice < len(languages):
                selected_lang = languages[choice]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

    # Update the target language
    lang_name, lang_code = selected_lang
    config.set("translate", "end_lang", lang_code)
    print(f"Selected target language: {lang_name} ({lang_code})")

    return config


def view_config(config):
    """Display the current configuration"""
    print("\n===== Current Configuration =====")
    for section in config.sections():
        print(f"\n[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")

    input("\nPress Enter to continue...")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="AACSpeakHelper CLI Configuration Tool"
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Path to a defined config file",
        required=False,
        default="",
    )
    args = parser.parse_args()

    # Load configuration
    config, config_path = load_config(args.config if args.config else None)

    # Main menu loop
    while True:
        print_menu(config)
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            config = configure_tts(config)
        elif choice == "2":
            config = configure_translation(config)
        elif choice == "3":
            view_config(config)
        elif choice == "4":
            save_config(config, config_path)
            print("Configuration saved. Exiting...")
            break
        elif choice == "5":
            print("Exiting without saving...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
