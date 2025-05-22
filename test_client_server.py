#!/usr/bin/env python
# test_client_server.py
# A script to test the AACSpeakHelper client and server with various configurations

import os
import sys
import subprocess
import configparser
import time
import argparse
import tempfile
import pyperclip
from pathlib import Path


def create_test_config(
    config_path,
    tts_engine="Sherpa-ONNX",
    translation_provider="GoogleTranslator",
    start_lang="en",
    end_lang="es",
    voice_id="eng",
):
    """Create a test configuration file with specified settings"""
    config = configparser.ConfigParser()

    # App section
    config["App"] = {"collectstats": "True"}

    # Translate section
    config["translate"] = {
        "no_translate": "False",
        "start_lang": str(start_lang),
        "end_lang": str(end_lang),
        "replace_pb": "True",
        "provider": str(translation_provider) if translation_provider else "",
        "microsoft_translator_secret_key": str(os.getenv("MICROSOFT_TOKEN_TRANS", "")),
        "papago_translator_client_id": "",
        "papago_translator_secret_key": "",
        "my_memory_translator_secret_key": "",
        "email": "",
        "libre_translator_secret_key": "",
        "url": "",
        "deep_l_translator_secret_key": "",
        "deepl_pro": "false",
        "region": str(os.getenv("MICROSOFT_REGION", "")),
        "yandex_translator_secret_key": "",
        "qcri_translator_secret_key": "",
        "baidu_translator_appid": "",
        "baidu_translator_secret_key": "",
    }

    # TTS section
    config["TTS"] = {
        "engine": str(tts_engine),
        "bypass_tts": "False",
        "save_audio_file": "True",
        "rate": "0",
        "volume": "100",
        "voice_id": str(voice_id),
    }

    # Azure TTS section
    config["azureTTS"] = {
        "key": str(os.getenv("MICROSOFT_TOKEN", "")),
        "location": str(os.getenv("MICROSOFT_REGION", "")),
        "voice_id": "en-US-JennyNeural",
    }

    # Google TTS section
    config["googleTTS"] = {
        "creds": str(os.getenv("GOOGLE_CREDS_PATH", "")),
        "voice_id": "en-US-Wavenet-C",
    }

    # Google Trans TTS section
    config["googleTransTTS"] = {"voice_id": ""}

    # SAPI5 TTS section
    config["sapi5TTS"] = {
        "voice_id": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
    }

    # Sherpa ONNX TTS section
    config["SherpaOnnxTTS"] = {"voice_id": str(voice_id)}

    # App Cache section
    config["appCache"] = {"threshold": "7"}

    # Save the configuration to the specified path
    with open(config_path, "w") as configfile:
        config.write(configfile)

    print(f"Test configuration created at {config_path}")
    return config_path


def run_client_with_config(config_path, text=None, list_voices=False, preview=False):
    """Run the client with the specified configuration and text"""
    # Set the text to the clipboard if provided
    if text:
        pyperclip.copy(text)
        print(f"Set clipboard text to: '{text}'")
    else:
        print("No text provided, using clipboard content")

    # Build the command
    cmd = [sys.executable, "client.py", "--config", config_path]

    # Add optional arguments
    if list_voices:
        cmd.append("--listvoices")
    if preview:
        cmd.append("--preview")

    print(f"Running client with command: {' '.join(cmd)}")

    # Wait a moment for the clipboard to be updated
    time.sleep(0.5)

    # Run the client
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("Client executed successfully")
        else:
            print(f"Client execution failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")

        return result
    except Exception as e:
        print(f"Exception running client: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Test AACSpeakHelper client and server"
    )
    parser.add_argument(
        "--text",
        help="Text to send to the server",
        default="Hello, this is a test message.",
    )
    parser.add_argument("--config", help="Path to a custom config file", default=None)
    parser.add_argument(
        "--tts-engine",
        help="TTS engine to use",
        choices=["Sherpa-ONNX", "Azure TTS", "Google TTS", "Google Trans"],
        default="Sherpa-ONNX",
    )
    parser.add_argument("--translation", help="Enable translation", action="store_true")
    parser.add_argument("--start-lang", help="Source language", default="en")
    parser.add_argument("--end-lang", help="Target language", default="es")
    parser.add_argument("--voice", help="Voice ID to use", default="eng")
    parser.add_argument(
        "--list-voices", help="List available voices", action="store_true"
    )
    parser.add_argument(
        "--preview", help="Preview only, don't speak", action="store_true"
    )

    args = parser.parse_args()

    # Create a temporary config file if no custom config is provided
    if args.config:
        config_path = args.config
    else:
        # Create a temporary directory for the config file
        temp_dir = tempfile.mkdtemp()
        config_path = os.path.join(temp_dir, "test_settings.cfg")

        # Create the config file
        create_test_config(
            config_path,
            tts_engine=args.tts_engine,
            translation_provider="GoogleTranslator" if args.translation else None,
            start_lang=args.start_lang,
            end_lang=args.end_lang,
            voice_id=args.voice,
        )

    # Run the client with the config
    run_client_with_config(
        config_path, args.text, list_voices=args.list_voices, preview=args.preview
    )


if __name__ == "__main__":
    main()
