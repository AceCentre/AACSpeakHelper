#!/usr/bin/env python
# cli_config_creator.py
# A simple CLI configuration tool for AACSpeakHelper

import os
import sys
import configparser
import argparse

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
    "polly": {
        "name": "AWS Polly",
        "config_section": "PollyTTS",
        "credential_fields": ["region", "aws_key_id", "aws_access_key"],
        "voice_list": {},  # Polly voices are fetched from API
    },
    "watson": {
        "name": "IBM Watson",
        "config_section": "WatsonTTS",
        "credential_fields": ["api_key", "region", "instance_id"],
        "voice_list": {},  # Watson voices are fetched from API
    },
    "openai": {
        "name": "OpenAI TTS",
        "config_section": "OpenAITTS",
        "credential_fields": ["api_key"],
        "voice_list": {},  # OpenAI voices are fetched from API
    },
    "witai": {
        "name": "Wit.AI",
        "config_section": "WitAiTTS",
        "credential_fields": ["token"],
        "voice_list": {},  # WitAI voices are fetched from API
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
    import uuid
    # Add default sections and values
    config["App"] = {"collectstats": "True", "uuid": str(uuid.uuid4())}

    config["translate"] = {
        "no_translate": "False",
        "start_lang": "en",
        "end_lang": "en",
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

    config["ElevenLabsTTS"] = {"api_key": "", "voice_id": ""}

    config["PlayHTTTS"] = {"api_key": "", "user_id": "", "voice_id": ""}

    config["PollyTTS"] = {"region": "us-east-1", "aws_key_id": "", "aws_access_key": "", "voice_id": ""}

    config["WatsonTTS"] = {"api_key": "", "region": "eu-gb", "instance_id": "", "voice_id": ""}

    config["OpenAITTS"] = {"api_key": "", "voice_id": ""}

    config["WitAiTTS"] = {"token": "", "voice_id": ""}

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
    elif tts_engine in ["PollyTTS", "AWS Polly"]:
        tts_voice = config.get("PollyTTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["WatsonTTS", "IBM Watson"]:
        tts_voice = config.get("WatsonTTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["OpenAITTS", "OpenAI TTS"]:
        tts_voice = config.get("OpenAITTS", "voice_id", fallback="Not configured")
    elif tts_engine in ["WitAiTTS", "Wit.AI"]:
        tts_voice = config.get("WitAiTTS", "voice_id", fallback="Not configured")

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
    while True:
        print("\n===== TTS Configuration =====")

        # Show current TTS settings
        current_engine = config.get("TTS", "engine", fallback="Not configured")
        current_bypass = config.get("TTS", "bypass_tts", fallback="False")
        current_save_audio = config.get("TTS", "save_audio_file", fallback="True")
        current_rate = config.get("TTS", "rate", fallback="0")
        current_volume = config.get("TTS", "volume", fallback="100")

        print(f"Current TTS Engine: {current_engine}")
        print(f"Bypass TTS: {current_bypass}")
        print(f"Save Audio Files: {current_save_audio}")
        print(f"Speech Rate: {current_rate}")
        print(f"Volume: {current_volume}")

        print("\nTTS Configuration Options:")
        print("1. Select TTS Engine")
        print("2. Configure TTS Settings (bypass, save audio, rate, volume)")
        print("3. Back to Main Menu")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            config = select_tts_engine(config)
        elif choice == "2":
            config = configure_tts_settings(config)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

    return config


def select_tts_engine(config):
    """Select and configure TTS engine"""
    print("\n===== Select TTS Engine =====")
    print("Available TTS Engines:")

    # Display available engines
    engines = list(TTS_ENGINES.keys())
    for i, engine_key in enumerate(engines):
        print(f"{i+1}. {TTS_ENGINES[engine_key]['name']}")

    print(f"{len(engines)+1}. Cancel")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect TTS engine (number): ")) - 1
            if choice == len(engines):  # Cancel option
                return config
            elif 0 <= choice < len(engines):
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


def configure_tts_settings(config):
    """Configure general TTS settings like bypass, save audio, rate, volume"""
    print("\n===== TTS Settings =====")

    # Configure bypass TTS
    current_bypass = config.get("TTS", "bypass_tts", fallback="False")
    print("\nBypass TTS (skip text-to-speech entirely)")
    print(f"Current value: {current_bypass}")
    bypass_choice = input("Bypass TTS? (y/n) [current]: ").lower()
    if bypass_choice == 'y':
        config.set("TTS", "bypass_tts", "True")
    elif bypass_choice == 'n':
        config.set("TTS", "bypass_tts", "False")

    # Configure save audio file
    current_save = config.get("TTS", "save_audio_file", fallback="True")
    print("\nSave Audio Files (cache audio for faster playback)")
    print(f"Current value: {current_save}")
    save_choice = input("Save audio files? (y/n) [current]: ").lower()
    if save_choice == 'y':
        config.set("TTS", "save_audio_file", "True")
    elif save_choice == 'n':
        config.set("TTS", "save_audio_file", "False")

    # Configure speech rate
    current_rate = config.get("TTS", "rate", fallback="0")
    print("\nSpeech Rate (0=normal, negative=slower, positive=faster)")
    print(f"Current value: {current_rate}")
    rate_input = input("Enter speech rate [-50 to 50] [current]: ")
    if rate_input:
        try:
            rate_value = int(rate_input)
            if -50 <= rate_value <= 50:
                config.set("TTS", "rate", str(rate_value))
            else:
                print("Rate must be between -50 and 50. Keeping current value.")
        except ValueError:
            print("Invalid rate value. Keeping current value.")

    # Configure volume
    current_volume = config.get("TTS", "volume", fallback="100")
    print("\nVolume (100=normal, 50=quieter, 150=louder)")
    print(f"Current value: {current_volume}")
    volume_input = input("Enter volume [0 to 200] [current]: ")
    if volume_input:
        try:
            volume_value = int(volume_input)
            if 0 <= volume_value <= 200:
                config.set("TTS", "volume", str(volume_value))
            else:
                print("Volume must be between 0 and 200. Keeping current value.")
        except ValueError:
            print("Invalid volume value. Keeping current value.")

    print("TTS settings updated.")
    return config


def get_voices_from_engine(engine_key, config):
    """Get voices from the actual TTS engine using py3-tts-wrapper"""
    try:
        from tts_wrapper import (
            MicrosoftClient, MicrosoftTTS,
            SherpaOnnxClient, SherpaOnnxTTS,
            GoogleTransClient, GoogleTransTTS,
            ElevenLabsClient, ElevenLabsTTS,
            PlayHTClient, PlayHTTTS,
            PollyClient, PollyTTS,
            WatsonClient, WatsonTTS,
            OpenAIClient,
            WitAiClient, WitAiTTS
        )

        engine_config = TTS_ENGINES[engine_key]
        section_name = engine_config["config_section"]

        if engine_key == "azure":
            # Get Azure TTS credentials
            key = config.get(section_name, "key", fallback="")
            location = config.get(section_name, "location", fallback="")
            if not key or not location:
                print("Azure TTS credentials not configured. Please configure them first.")
                return None

            client = MicrosoftClient(credentials=(key, location))
            tts = MicrosoftTTS(client)
            voices = tts.get_voices()

            # Convert to our format
            voice_list = []
            for voice in voices:
                # Handle both dict and object formats
                if isinstance(voice, dict):
                    voice_list.append({
                        'id': voice.get('id', voice.get('voice_id', '')),
                        'name': voice.get('name', voice.get('display_name', '')),
                        'language': voice.get('language', voice.get('locale', '')),
                        'gender': voice.get('gender', '')
                    })
                else:
                    voice_list.append({
                        'id': getattr(voice, 'id', getattr(voice, 'voice_id', '')),
                        'name': getattr(voice, 'name', getattr(voice, 'display_name', '')),
                        'language': getattr(voice, 'language', getattr(voice, 'locale', '')),
                        'gender': getattr(voice, 'gender', '')
                    })
            return voice_list

        elif engine_key == "sherpa":
            # Get Sherpa ONNX voices
            client = SherpaOnnxClient()
            tts = SherpaOnnxTTS(client)
            voices = tts.get_voices()
            return voices

        elif engine_key == "google_trans":
            # Google Trans TTS doesn't need credentials
            client = GoogleTransClient()
            tts = GoogleTransTTS(client)
            voices = tts.get_voices()
            return voices

        elif engine_key == "elevenlabs":
            # Get ElevenLabs credentials
            import os
            api_key = config.get(section_name, "api_key", fallback="")
            if not api_key:
                api_key = os.getenv("ELEVENLABS_API_KEY", "")
            if not api_key:
                print("ElevenLabs API key not configured. Please configure it first.")
                return None

            client = ElevenLabsClient(credentials=(api_key,))
            tts = ElevenLabsTTS(client)
            voices = tts.get_voices()
            return voices

        elif engine_key == "playht":
            # Get PlayHT credentials
            import os
            api_key = config.get(section_name, "api_key", fallback="")
            user_id = config.get(section_name, "user_id", fallback="")
            if not api_key:
                api_key = os.getenv("PLAYHT_API_KEY", "")
            if not user_id:
                user_id = os.getenv("PLAYHT_USER_ID", "")
            if not api_key or not user_id:
                print("PlayHT credentials not configured. Please configure them first.")
                return None

            client = PlayHTClient(credentials=(api_key, user_id))
            tts = PlayHTTTS(client)
            voices = tts.get_voices()
            return voices

        elif engine_key == "polly":
            # Get Polly credentials
            import os
            region = config.get(section_name, "region", fallback="")
            aws_key_id = config.get(section_name, "aws_key_id", fallback="")
            aws_access_key = config.get(section_name, "aws_access_key", fallback="")
            if not region:
                region = os.getenv("POLLY_REGION", "us-east-1")
            if not aws_key_id:
                aws_key_id = os.getenv("POLLY_AWS_KEY_ID", "")
            if not aws_access_key:
                aws_access_key = os.getenv("POLLY_AWS_ACCESS_KEY", "")
            if not aws_key_id or not aws_access_key:
                print("Polly credentials not configured. Please configure them first.")
                return None

            client = PollyClient(credentials=(region, aws_key_id, aws_access_key))
            tts = PollyTTS(client)
            voices = tts.get_voices()
            return voices

        elif engine_key == "watson":
            # Get Watson credentials
            import os
            api_key = config.get(section_name, "api_key", fallback="")
            region = config.get(section_name, "region", fallback="")
            instance_id = config.get(section_name, "instance_id", fallback="")
            if not api_key:
                api_key = os.getenv("WATSON_API_KEY", "")
            if not region:
                region = os.getenv("WATSON_REGION", "eu-gb")
            if not instance_id:
                instance_id = os.getenv("WATSON_INSTANCE_ID", "")
            if not api_key:
                print("Watson credentials not configured. Please configure them first.")
                return None

            client = WatsonClient(credentials=(api_key, region, instance_id))
            tts = WatsonTTS(client)
            voices = tts.get_voices()
            return voices

        elif engine_key == "openai":
            # Get OpenAI credentials
            import os
            api_key = config.get(section_name, "api_key", fallback="")
            if not api_key:
                api_key = os.getenv("OPENAI_API_KEY", "")
            if not api_key:
                print("OpenAI API key not configured. Please configure it first.")
                return None

            client = OpenAIClient(credentials=(api_key,))
            tts = OpenAITTS(client)
            voices = tts.get_voices()
            return voices

        elif engine_key == "witai":
            # Get WitAI credentials
            import os
            token = config.get(section_name, "token", fallback="")
            if not token:
                token = os.getenv("WITAI_TOKEN", "")
            if not token:
                print("WitAI token not configured. Please configure it first.")
                return None

            client = WitAiClient(credentials=(token,))
            tts = WitAiTTS(client)
            voices = tts.get_voices()
            return voices

        # Add other engines as needed
        return None

    except Exception as e:
        print(f"Error getting voices from {engine_key}: {e}")
        return None


def configure_voice(config, engine_key):
    """Configure voice for the selected TTS engine"""
    engine_config = TTS_ENGINES[engine_key]
    section_name = engine_config["config_section"]

    # Try to get voices from the actual TTS engine first
    print("Getting available voices from TTS engine...")
    voices = get_voices_from_engine(engine_key, config)

    if voices:
        # Allow searching by language
        search_term = input(
            "Search for a voice by language name (or press Enter to see all): "
        ).lower()

        matching_voices = []
        for voice in voices:
            voice_name = voice.get('name', voice.get('id', ''))
            voice_id = voice.get('id', voice.get('voice_id', ''))
            if search_term in voice_name.lower():
                matching_voices.append((voice_name, voice_id))

        if not matching_voices:
            print("No matching voices found.")
            return config

        print("\nMatching voices:")
        for i, (voice_name, voice_id) in enumerate(matching_voices):
            print(f"{i+1}. {voice_name} ({voice_id})")
        print(f"{len(matching_voices)+1}. Cancel")

        # Get user selection
        while True:
            try:
                choice = int(input("\nSelect voice (number): ")) - 1
                if choice == len(matching_voices):  # Cancel option
                    return config
                elif 0 <= choice < len(matching_voices):
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

    # Fallback to hardcoded voice list
    print("Using fallback voice list...")
    voice_list = engine_config["voice_list"]

    if not voice_list:
        print("Voice list not available for this engine.")
        voice_id = input("Enter voice ID manually (or press Enter to cancel): ")
        if voice_id:
            config.set(section_name, "voice_id", voice_id)
        return config

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
        return config

    print("\nMatching voices:")
    for i, (voice_name, voice_id) in enumerate(matching_voices):
        print(f"{i+1}. {voice_name} ({voice_id})")
    print(f"{len(matching_voices)+1}. Cancel")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect voice (number): ")) - 1
            if choice == len(matching_voices):  # Cancel option
                return config
            elif 0 <= choice < len(matching_voices):
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
    while True:
        print("\n===== Translation Configuration =====")

        # Show current translation settings
        current_provider = config.get("translate", "provider", fallback="Not configured")
        current_no_translate = config.get("translate", "no_translate", fallback="False")
        current_replace_pb = config.get("translate", "replace_pb", fallback="True")
        current_start_lang = config.get("translate", "start_lang", fallback="en")
        current_end_lang = config.get("translate", "end_lang", fallback="en")

        print(f"Current Translation Provider: {current_provider}")
        print(f"Translation Disabled: {current_no_translate}")
        print(f"Replace Clipboard: {current_replace_pb}")
        print(f"Source Language: {current_start_lang}")
        print(f"Target Language: {current_end_lang}")

        print("\nTranslation Configuration Options:")
        print("1. Select Translation Provider")
        print("2. Configure Translation Settings (enable/disable, clipboard)")
        print("3. Configure Languages")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            config = select_translation_provider(config)
        elif choice == "2":
            config = configure_translation_settings(config)
        elif choice == "3":
            # Get current provider for language configuration
            current_provider_key = None
            for key, provider in TRANSLATION_PROVIDERS.items():
                if provider["name"] == config.get("translate", "provider", fallback=""):
                    current_provider_key = key
                    break
            if current_provider_key:
                configure_languages(config, current_provider_key)
            else:
                print("Please select a translation provider first.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

    return config


def select_translation_provider(config):
    """Select and configure translation provider"""
    print("\n===== Select Translation Provider =====")
    print("Available Translation Providers:")

    # Display available providers
    providers = list(TRANSLATION_PROVIDERS.keys())
    for i, provider_key in enumerate(providers):
        print(f"{i+1}. {TRANSLATION_PROVIDERS[provider_key]['name']}")

    print(f"{len(providers)+1}. Cancel")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect translation provider (number): ")) - 1
            if choice == len(providers):  # Cancel option
                return config
            elif 0 <= choice < len(providers):
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


def configure_translation_settings(config):
    """Configure general translation settings like enable/disable, clipboard replacement"""
    print("\n===== Translation Settings =====")

    # Configure no_translate (disable translation)
    current_no_translate = config.get("translate", "no_translate", fallback="False")
    print("\nTranslation Status")
    print(f"Currently disabled: {current_no_translate}")
    print("Disable translation if your text is already in the target language")
    translate_choice = input("Disable translation? (y/n) [current]: ").lower()
    if translate_choice == 'y':
        config.set("translate", "no_translate", "True")
    elif translate_choice == 'n':
        config.set("translate", "no_translate", "False")

    # Configure replace_pb (replace clipboard)
    current_replace = config.get("translate", "replace_pb", fallback="True")
    print("\nClipboard Replacement")
    print(f"Currently enabled: {current_replace}")
    print("Replace clipboard content with translated text (useful for AAC apps)")
    replace_choice = input("Replace clipboard with translated text? (y/n) [current]: ").lower()
    if replace_choice == 'y':
        config.set("translate", "replace_pb", "True")
    elif replace_choice == 'n':
        config.set("translate", "replace_pb", "False")

    print("Translation settings updated.")
    return config


def configure_languages(config, provider_key):
    """Configure source and target languages for translation"""
    provider_config = TRANSLATION_PROVIDERS[provider_key]
    language_list = provider_config["language_list"]

    if not language_list:
        print("Language list not available for this provider.")
        start_lang = input("Enter source language code manually (or press Enter to cancel): ")
        if not start_lang:
            return config
        end_lang = input("Enter target language code manually (or press Enter to cancel): ")
        if not end_lang:
            return config
        config.set("translate", "start_lang", start_lang)
        config.set("translate", "end_lang", end_lang)
        return config

    # Configure source language
    print("\nAvailable source languages:")
    languages = list(language_list.items())
    for i, (lang_name, lang_code) in enumerate(languages):
        print(f"{i+1}. {lang_name} ({lang_code})")
    print(f"{len(languages)+1}. Cancel")

    # Get user selection for source language
    while True:
        try:
            choice = int(input("\nSelect source language (number): ")) - 1
            if choice == len(languages):  # Cancel option
                return config
            elif 0 <= choice < len(languages):
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
    print(f"{len(languages)+1}. Cancel")

    # Get user selection for target language
    while True:
        try:
            choice = int(input("\nSelect target language (number): ")) - 1
            if choice == len(languages):  # Cancel option
                return config
            elif 0 <= choice < len(languages):
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
