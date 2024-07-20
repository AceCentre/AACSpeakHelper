import logging
import io
import os.path
import sys
import time
import pyttsx3
from gtts import gTTS
from tts_wrapper import AbstractTTS
from tts_wrapper import MicrosoftClient, MicrosoftTTS
from tts_wrapper import GoogleClient, GoogleTTS
from tts_wrapper import SAPIClient, SAPITTS
from tts_wrapper import MMSClient, MMSTTS
# from KurdishTTS.kurdishTTS import KurdishTTS
from utils import play_audio, save_audio, config, check_history, args
import warnings
from threading import Thread
# import dl_translate as dlt

warnings.filterwarnings("ignore")

VALID_STYLES = [
    "advertisement_upbeat",
    "affectionate",
    "angry",
    "assistant",
    "calm",
    "chat",
    "cheerful",
    "customerservice",
    "depressed",
    "disgruntled",
    "documentary-narration",
    "embarrassed",
    "empathetic",
    "envious",
    "excited",
    "fearful",
    "friendly",
    "gentle",
    "hopeful",
    "lyrical",
    "narration-professional",
    "narration-relaxed",
    "newscast",
    "newscast-casual",
    "newscast-formal",
    "poetry-reading",
    "sad",
    "serious",
    "shouting",
    "sports_commentary",
    "sports_commentary_excited",
    "whispering",
    "terrified",
    "unfriendly"
]


class GSPEAK:

    def __init__(self):
        self.audio = io.BytesIO()

    def synth_to_bytes(self, text: str):
        with self.audio as file:
            gTTS(text=text, lang=config.get('translate', 'endLang')).write_to_fp(file)
            file.seek(0)
            return file.read()


def speak(text=''):
    # start = time.time()
    file = check_history(text)
    if file is not None and os.path.isfile(file):
        play_audio(file, file=True)
        print("Speech synthesized for text [{}] from cache.".format(text))
        logging.info("Speech synthesized for text [{}] from cache.".format(text))
        # print(f'Playback from cache: {time.time() - start}')
        return
    ttsengine = config.get('TTS', 'engine')
    if ttsengine == 'gspeak':
        gSpeak(text, ttsengine)
    elif ttsengine == 'azureTTS':
        if args['style']:
            azureSpeak(text, ttsengine, args['style'], args['styledegree'])
        else:
            azureSpeak(text, ttsengine)
    elif ttsengine == 'gTTS':
        googleSpeak(text, ttsengine)
    elif ttsengine == 'sapi5':
        sapiSpeak(text, ttsengine)
    elif ttsengine == 'mms':
        mmsSpeak(text, ttsengine)
    else:  # Unsupported Engines
        engine = pyttsx3.init(ttsengine)
        engine.setProperty('voice', config.get('TTS', 'voiceid'))
        engine.setProperty('rate', config.get('TTS', 'rate'))
        engine.setProperty('volume', config.get('TTS', 'volume'))
        engine.say(text)
        engine.runAndWait()
    # print(f'Realtime Playback: {time.time() - start}')


def mmsSpeak(text: str, engine):
    voiceid = config.get('mmsTTS', 'voiceid')
    if getattr(sys, 'frozen', False):
        home_directory = os.path.expanduser("~")
        mms_cache_path = os.path.join(home_directory, 'AppData', 'Roaming', 'Ace Centre', 'AACSpeechHelper', 'models')
    elif __file__:
        app_data_path = os.path.abspath(os.path.dirname(__file__))
        mms_cache_path = os.path.join(app_data_path, 'models')
    if not os.path.isdir(mms_cache_path):
        os.mkdir(mms_cache_path)
    client = MMSClient((mms_cache_path, voiceid))
    tts = MMSTTS(client)
    ttsWrapperSpeak(text, tts, engine)


def azureSpeak(text: str, engine, style: str = None, styledegree: float = None):
    # Add your key and endpoint
    key = config.get('azureTTS', 'key')
    location = config.get('azureTTS', 'location')
    voiceid = config.get('azureTTS', 'voiceid')
    if not voiceid:
        raise ValueError("voiceid is empty or None")
    if '-' not in voiceid:
        raise ValueError("voiceid does not contain a hyphen")
    parts = voiceid.split('-')
    if len(parts) < 2:
        raise ValueError("voiceid does not have enough parts separated by hyphens")
    lang = parts[0] + '-' + parts[1]
    # client = MicrosoftClient(credentials=key, region=location)
    client = MicrosoftClient((key, location))
    tts = MicrosoftTTS(client=client, voice=voiceid, lang=lang)

    if style:
        # Check if the provided style is in the valid styles array
        if style in VALID_STYLES:
            # Construct SSML with the specified style
            ssml = f'<mstts:express-as style="{style}"'
            if styledegree:
                ssml += f' styledegree="{styledegree}"'
            ssml += f'>{text}</mstts:express-as>'
        else:
            # Style is not valid, use default SSML without style
            ssml = text
    else:
        # Use default SSML without style
        ssml = text

    ttsWrapperSpeak(ssml, tts, engine)


def googleSpeak(text: str, engine):
    # Add your key and endpoint
    creds_file = config.get('googleTTS', 'creds_file')
    voiceid = config.get('googleTTS', 'voiceid')

    client = GoogleClient(credentials=creds_file)
    tts = GoogleTTS(client=client, voice=voiceid)
    ttsWrapperSpeak(text, tts, engine)


def sapiSpeak(text: str, engine):
    # Add your key and endpoint
    voiceid = config.get('sapi5TTS', 'voiceid')

    client = SAPIClient()
    client._client.setProperty('voice', voiceid)
    client._client.setProperty('rate', config.get('TTS', 'rate'))
    client._client.setProperty('volume', config.get('TTS', 'volume'))
    tts = SAPITTS(client=client)
    ttsWrapperSpeak(text, tts, engine)


def gSpeak(text: str, engine):
    tts = GSPEAK()
    ttsWrapperSpeak(text, tts, engine)


def ttsWrapperSpeak(text: str, tts, engine):
    # Render the audio to bytes
    fmt = 'wav'
    if isinstance(tts, SAPITTS):
        audio_bytes = tts.synth_to_bytes(text, 'wav')
    elif isinstance(tts, MMSTTS):
        audio_bytes = tts.synth_to_bytes(text, 'wav')
    elif isinstance(tts, AbstractTTS):
        audio_bytes = tts.synth_to_bytes(tts.ssml.add(text), 'wav')
    elif isinstance(tts, GSPEAK):
        audio_bytes = tts.synth_to_bytes(text)
        fmt = 'mp3'
    else:
        logging.error(str(type(tts)) + " TTS Engine is Invalid.")
        raise Exception(str(type(tts)) + " TTS Engine is Invalid.")
    try:
        playText = Thread(target=playSpeech, args=(audio_bytes, text, tts))
        saveText = Thread(target=saveSpeech, args=(audio_bytes, text, engine, fmt, tts))
        playText.start()
        saveText.start()
    except Exception as e:
        print(e)


def playSpeech(audio_bytes, text, tts):
    # start = time.perf_counter()
    if not isinstance(tts, MMSTTS):
        play_audio(audio_bytes)
    else:
        tts.speak(text)
    # stop = time.perf_counter() - start
    # print(f"Speech synthesis runtime is {stop:0.5f} seconds.")
    # logging.info(f"Speech synthesis runtime is {stop:0.5f} seconds.")


def saveSpeech(audio_bytes, text, engine, format, tts):
    # start = time.perf_counter()
    save_audio_file = config.getboolean('TTS', 'save_audio_file')
    if save_audio_file:
        save_audio(audio_bytes, text=text, engine=engine, format=format, tts=tts)
    # stop = time.perf_counter() - start
    # print(f"Speech file saving runtime is {stop:0.5f} seconds.")
    # logging.info(f"Speech file saving runtime is {stop:0.5f} seconds.")


def load_deep_learning_translation():
    start = time.time()
    global dl
    # dl = dlt.TranslationModel("dlt/cached_model_nllb200", model_family="nllb200")
    print(dl)
    print(time.time() - start)


def deep_learning_translation():
    pass


# dl = None
# dlTranslate = Thread(target=load_deep_learning_translation)
# dlTranslate.start()
