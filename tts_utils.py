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
import warnings
from threading import Thread

# import dl_translate as dlt
warnings.filterwarnings("ignore")
utils = None
# Global dictionary to store TTS clients
tts_clients = {}

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


def init(module):
    # from utils import play_audio, save_audio, config, check_history, args
    global utils
    utils = module


class GSPEAK:

    def __init__(self):
        self.audio = io.BytesIO()

    def synth_to_bytes(self, text: str):
        with self.audio as file:
            gTTS(text=text, lang=utils.config.get('translate', 'endLang')).write_to_fp(file)
            file.seek(0)
            return file.read()

def init_azure_tts():
    key = utils.config.get('azureTTS', 'key')
    location = utils.config.get('azureTTS', 'location')
    voiceid = utils.config.get('azureTTS', 'voiceid')
    parts = voiceid.split('-')
    lang = parts[0] + '-' + parts[1]
    client = MicrosoftClient((key, location))
    return MicrosoftTTS(client=client, voice=voiceid, lang=lang)

def init_google_tts():
    creds_file = utils.config.get('googleTTS', 'creds_file')
    voiceid = utils.config.get('googleTTS', 'voiceid')
    client = GoogleClient(credentials=creds_file)
    return GoogleTTS(client=client, voice=voiceid)

def init_sapi_tts():
    voiceid = utils.config.get('sapi5TTS', 'voiceid')
    client = SAPIClient()
    client._client.setProperty('voice', voiceid)
    client._client.setProperty('rate', utils.config.get('TTS', 'rate'))
    client._client.setProperty('volume', utils.config.get('TTS', 'volume'))
    return SAPITTS(client=client)

def init_mms_tts():
    voiceid = utils.config.get('mmsTTS', 'voiceid')
    if getattr(sys, 'frozen', False):
        home_directory = os.path.expanduser("~")
        mms_cache_path = os.path.join(home_directory, 'AppData', 'Roaming', 'Ace Centre', 'AACSpeakHelper', 'models')
    elif __file__:
        app_data_path = os.path.abspath(os.path.dirname(__file__))
        mms_cache_path = os.path.join(app_data_path, 'models')
    if not os.path.isdir(mms_cache_path):
        os.mkdir(mms_cache_path)
    client = MMSClient((mms_cache_path, voiceid))
    return MMSTTS(client)

def speak(text=''):
    file = utils.check_history(text)
    if file is not None and os.path.isfile(file):
        utils.play_audio(file, file=True)
        print("Speech synthesized for text [{}] from cache.".format(text))
        logging.info("Speech synthesized for text [{}] from cache.".format(text))
        return

    ttsengine = utils.config.get('TTS', 'engine')
    
    # Check if the TTS client is already in memory
    if ttsengine in tts_clients:
        tts_client = tts_clients[ttsengine]
    else:
        # Initialize the TTS client based on the engine
        if ttsengine == 'gspeak':
            tts_client = GSPEAK()
        elif ttsengine == 'azureTTS':
            tts_client = init_azure_tts()
        elif ttsengine == 'gTTS':
            tts_client = init_google_tts()
        elif ttsengine == 'sapi5':
            tts_client = init_sapi_tts()
        elif ttsengine == 'mms':
            tts_client = init_mms_tts()
        else:
            tts_client = pyttsx3.init(ttsengine)
        
        # Store the client for future use
        tts_clients[ttsengine] = tts_client

    # Use the TTS client
    if ttsengine == 'gspeak':
        gSpeak(text, ttsengine, tts_client)
    elif ttsengine == 'azureTTS':
        if utils.args['style']:
            azureSpeak(text, ttsengine, tts_client, utils.args['style'], utils.args['styledegree'])
        else:
            azureSpeak(text, ttsengine, tts_client)
    elif ttsengine == 'gTTS':
        googleSpeak(text, ttsengine, tts_client)
    elif ttsengine == 'sapi5':
        sapiSpeak(text, ttsengine, tts_client)
    elif ttsengine == 'mms':
        mmsSpeak(text, ttsengine, tts_client)
    else:
        tts_client.setProperty('voice', utils.config.get('TTS', 'voiceid'))
        tts_client.setProperty('rate', utils.config.get('TTS', 'rate'))
        tts_client.setProperty('volume', utils.config.get('TTS', 'volume'))
        tts_client.say(text)
        tts_client.runAndWait()


def mmsSpeak(text: str, engine, tts_client):
    ttsWrapperSpeak(text, tts_client, engine)

def azureSpeak(text: str, engine, tts_client, style: str = None, styledegree: float = None):
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

    ttsWrapperSpeak(ssml, tts_client, engine)

def googleSpeak(text: str, engine, tts_client):
    ttsWrapperSpeak(text, tts_client, engine)

def sapiSpeak(text: str, engine, tts_client):
    ttsWrapperSpeak(text, tts_client, engine)

def gSpeak(text: str, engine, tts_client):
    ttsWrapperSpeak(text, tts_client, engine)


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
    start = time.perf_counter()
    if not isinstance(tts, MMSTTS):
        utils.play_audio(audio_bytes)
    else:
        tts.speak(text)
    stop = time.perf_counter() - start
    print(f"Speech synthesis runtime is {stop:0.5f} seconds.")
    # logging.info(f"Speech synthesis runtime is {stop:0.5f} seconds.")


def saveSpeech(audio_bytes, text, engine, format, tts):
    # start = time.perf_counter()
    save_audio_file = utils.config.getboolean('TTS', 'save_audio_file')
    if save_audio_file:
        utils.save_audio(audio_bytes, text=text, engine=engine, format=format, tts=tts)
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
