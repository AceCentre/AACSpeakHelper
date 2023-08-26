import requests
import math
import time
from pygame import mixer
# from py_mini_racer import py_mini_racer
from io import BytesIO
import string
import random
import unicodedata
# import Normalizer as normalizer


class KurdishTTS:

    def __init__(self):
        mixer.init()
        # with open('Normalizer.js', encoding="utf8") as file:
        #     cf_js = file.read()
        # self.script = py_mini_racer.MiniRacer()
        # self.script.eval(cf_js)

    def normalize_text(self, text: str):
        # normalizedText = self.script.call("NormalizeUnicode", text)
        # normalizedText = self.script.call("clearFormatting", text)
        normalizedText = unicodedata.normalize('NFC', text)
        # normalizedText = normalizer.clearFormatting(text)
        print("Input Text: " + text)
        print("Normalized Text: " + normalizedText)
        return normalizedText

    def synth_to_bytes(self, text: str, latin: str = 'true', punctuation: str = 'false'):#, download: bool = True):
        # text = input text string
        # latin = either 'true' or 'false'
        # punctuation = either 'true' or 'false'
        # download = either True or False, choose if you need to download the audio file or not

        if len(text) > 2000:
            raise Exception("Text reached the maximum characters limit")
        words = self.normalize_text(text)
        url = 'https://tts.kurdishspeech.com'
        parameters = {'t': words, 'l': latin, 'p': punctuation}
        response = requests.post(url, data=parameters)
        audio = requests.get('https://tts.kurdishspeech.com/static/TTS/' + response.text + '.mp3')
        # if download:
        #     with open('{}.mp3.'.format(response.text), 'wb') as file:
        #         file.write(audio.content)
        # audioFile = BytesIO(audio.content)
        # audioMixer = mixer.Sound(audioFile)
        # mixer.Sound.play(audioMixer)
        # time.sleep(math.ceil(audioMixer.get_length()))
        return audio.content


# if __name__ == "__main__":
#     speech = KurdishTTS()
#     # length = 2001
#     # text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
#     # print("Generated random string : " + str(text))
#     text = "ەڵبەتە لەیەککات و لەیەک سەرزەمیندا دوو گۆڕانکاری مەزن و پڕ سەروەری دەبێتە مایەی هاتنەکایەی خۆشگوزەرانی و شادنوودی گەل و کۆمەلانی خەڵک ، ئەو دوو حاڵەتە پڕ سەروەرییەش ، یەکەمیان ئاشکراکردنی حکومەتی کابینەی شەشەمە بەپۆلێک عەقڵییەتی تازەو بەرنامەی تازەترەوە بۆ خزمەتکردن بە هەرێمی کوردستان ، دووەمیشیان گرێدانی پلینۆمی ( ی.ن.ک ) بۆ دووبارە "
#     # text = "Good Morning"
#     speech.synth_to_bytes(text)
