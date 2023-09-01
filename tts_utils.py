import logging

import pyttsx3

from tts_wrapper import AbstractTTS
from tts_wrapper import MicrosoftClient, MicrosoftTTS
from tts_wrapper import GoogleClient, GoogleTTS
from tts_wrapper import SAPIClient, SAPITTS

from KurdishTTS.kurdishTTS import KurdishTTS
from utils import play_audio, save_audio, config


def speak(text=''):
    ttsengine = config.get('TTS', 'engine')
    if (ttsengine == 'gspeak'):
        from gspeak import speak
        speak(text, lang=config.get('translate', 'endLang').lower())
    elif (ttsengine == 'azureTTS'):
        azureSpeak(text)
    elif (ttsengine == 'gTTS'):
        googleSpeak(text)
    elif (ttsengine == 'sapi5'):
        sapiSpeak(text)
    elif (ttsengine == 'kurdishTTS'):
        kurdishSpeak(text)
    else:  # Unsupported Engines
        engine = pyttsx3.init(ttsengine)
        engine.setProperty('voice', config.get('TTS', 'voiceid'))
        engine.setProperty('rate', config.get('TTS', 'rate'))
        engine.setProperty('volume', config.get('TTS', 'volume'))
        engine.say(text)
        engine.runAndWait()


def azureSpeak(text: str):
    # Add your key and endpoint
    key = config.get('azureTTS', 'key')
    location = config.get('azureTTS', 'location')
    voiceid = config.get('azureTTS', 'voiceid')

    client = MicrosoftClient(credentials=key, region=location)
    tts = MicrosoftTTS(client=client, voice=voiceid)

    ttsWrapperSpeak(text, tts)


def googleSpeak(text: str):
    # Add your key and endpoint
    creds_file = config.get('googleTTS', 'creds_file')
    voiceid = config.get('googleTTS', 'voiceid')

    client = GoogleClient(credentials=creds_file)
    tts = GoogleTTS(client=client, voice=voiceid)
    ttsWrapperSpeak(text, tts)


def sapiSpeak(text: str):
    # Add your key and endpoint
    voiceid = config.get('sapi5TTS', 'voiceid')

    client = SAPIClient()
    client._client.setProperty('voice', voiceid)
    client._client.setProperty('rate', config.get('TTS', 'rate'))
    client._client.setProperty('volume', config.get('TTS', 'volume'))
    tts = SAPITTS(client=client)
    ttsWrapperSpeak(text, tts)


def kurdishSpeak(text: str):
    tts = KurdishTTS()
    # tts.synth_to_bytes(text)
    ttsWrapperSpeak(text, tts)


def ttsWrapperSpeak(text: str, tts):
    save_audio_file = bool(config.get('TTS', 'save_audio_file'))
    fmt = 'wav'
    if isinstance(tts, SAPITTS):
        audio_bytes = tts.synth_to_bytes(text, 'wav')
    elif isinstance(tts, KurdishTTS):
        latin = config.get('kurdishTTS', 'latin')
        punctuation = config.get('kurdishTTS', 'punctuation')
        audio_bytes = tts.synth_to_bytes(text, latin, punctuation)  # Beyanî baş Good Morning
        fmt = 'mp3'
    elif isinstance(tts, AbstractTTS):
        audio_bytes = tts.synth_to_bytes(tts.ssml.add(text), 'wav')
    else:
        raise Exception(str(type(tts)) + " TTS Engine is Invalid.")

    play_audio(audio_bytes)
    print("Speech synthesized for text [{}]".format(text))
    logging.info("Speech synthesized for text [{}]".format(text))

    if save_audio_file:
        save_audio(audio_bytes, format=fmt)
    # What a beautiful day today!
