import requests
from pygame import mixer
import unicodedata
import logging


class KurdishTTS:

    def __init__(self):
        mixer.init()

    def normalize_text(self, text: str):
        # normalizedText = self.script.call("NormalizeUnicode", text)
        # normalizedText = self.script.call("clearFormatting", text)
        normalizedText = unicodedata.normalize('NFC', text)
        # normalizedText = normalizer.clearFormatting(text)
        print("Normalized Text: " + normalizedText)
        logging.info("Normalized Text: {}".format(normalizedText))
        return normalizedText

    def synth_to_bytes(self, text: str, latin: str = 'true', punctuation: str = 'false'):#, download: bool = True):
        # text = input text string
        # latin = either 'true' or 'false'
        # punctuation = either 'true' or 'false'
        # download = either True or False, choose if you need to download the audio file or not

        if len(text) > 2000:
            logging.error("Text reached the maximum characters limit", exc_info=True)
            raise Exception("Text reached the maximum characters limit")
        words = self.normalize_text(text)
        url = 'https://tts.kurdishspeech.com'
        parameters = {'t': words, 'l': latin, 'p': punctuation}
        response = requests.post(url, data=parameters)
        audio = requests.get('https://tts.kurdishspeech.com/static/TTS/' + response.text + '.mp3')
        return audio.content

