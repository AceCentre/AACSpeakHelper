import logging
import io
import os.path
import sys
import time
from pathlib import Path

import pyttsx3
from gtts import gTTS
from tts_wrapper import (
    AbstractTTS,
    MicrosoftClient,
    MicrosoftTTS,
    GoogleClient,
    GoogleTTS,
    SAPIClient,
    SAPIEngine,
    SherpaOnnxClient,
    SherpaOnnxTTS,
    GoogleTransTTS,
    GoogleTransClient,
)
import warnings
from threading import Thread
from configure_enc_utils import load_config, load_credentials

warnings.filterwarnings("ignore", category=RuntimeWarning)
utils = None
voices = None
ready = True
# Global dictionary to store TTS clients
tts_voiceid = {}

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
    "unfriendly",
]


def init(module):
    """Initialize utils module making it in memory instead of one time instance.

    Args:
        module: Instance of utils module.
    Returns: None
    """
    global utils
    utils = module


def init_azure_tts():
    """Initialize unique instance of MicrosoftTTS based on the changes in voiceid.

    Returns: MicrosoftTTS
    """
    key = utils.config.get("azureTTS", "key")
    config = load_config()
    if key == "":
        key = config.get("azureTTS")["key"]
    location = utils.config.get("azureTTS", "location")
    if location == "":
        location = config.get("azureTTS")["location"]
    voiceid = utils.config.get("azureTTS", "voiceid")
    parts = voiceid.split("-")
    lang = parts[0] + "-" + parts[1]
    client = MicrosoftClient((key, location))
    return MicrosoftTTS(client=client, voice=voiceid, lang=lang)


def init_google_tts():
    """Initialize unique instance of GoogleTTS based on the changes in voiceid.

    Returns: GoogleTTS
    """
    gcreds = utils.config.get("googleTTS", "creds")
    path = Path(gcreds)
    if not path.exists():
        path = Path("google_creds.enc")
    file_format = path.suffix
    if file_format == ".enc":
        gcreds = load_credentials(path)
        logging.info(f"Google TTS credentials file location: {path}")
    logging.info(f"Google TTS credentials file location: {path}")
    if not isinstance(gcreds, dict) and os.path.isfile(gcreds):
        logging.info(f"Google TTS credentials file: {gcreds}")
    voiceid = utils.config.get("googleTTS", "voiceid")
    client = GoogleClient(credentials=gcreds)
    tts = GoogleTTS(client=client, voice=voiceid)
    return tts


def init_sapi_tts():
    """Initialize unique instance of SAPIEngine based on the changes in voiceid.

    Returns: SAPIEngine
    """
    voiceid = utils.config.get("sapi5TTS", "voiceid")
    client = SAPIClient()
    client._client.setProperty("voice", voiceid)
    client._client.setProperty("rate", utils.config.get("TTS", "rate"))
    client._client.setProperty("volume", utils.config.get("TTS", "volume"))
    return SAPIEngine(client=client)


def init_onnx_tts():
    """Initialize unique instance of SherpaOnnxTTS based on the changes in voiceid.

    Returns: SherpaOnnxTTS
    """
    voiceid = utils.config.get("SherpaOnnxTTS", "voiceid")
    if getattr(sys, "frozen", False):
        home_directory = os.path.expanduser("~")
        onnx_cache_path = os.path.join(
            home_directory,
            "AppData",
            "Roaming",
            "Ace Centre",
            "AACSpeakHelper",
            "models",
        )
    elif __file__:
        app_data_path = os.path.abspath(os.path.dirname(__file__))
        onnx_cache_path = os.path.join(app_data_path, "models")
    if not os.path.isdir(onnx_cache_path):
        os.mkdir(onnx_cache_path)
    client = SherpaOnnxClient(model_path=onnx_cache_path, tokens_path=None)
    tts = SherpaOnnxTTS(client)
    tts.set_voice(voice_id=voiceid)
    return tts


def init_googleTrans_tts():
    """Initialize unique instance of GoogleTransTTS based on the changes in voiceid.

    Returns: GoogleTransTTS
    """
    voiceid = utils.config.get("googleTransTTS", "voiceid")
    client = GoogleTransClient(voiceid)
    return GoogleTransTTS(client)


def speak(text="", list_voices=False):
    """Speak function convert text parameter to speech. This function decides which TTS Engine will be used
    base on the config file received.
    Then, it will call the specific function that will create the TTS Engine Instance.

    Args:
        text (str): String to be spoken by specific TTS Engine.
        list_voices (bool): Use to return all available voices only instead of speech function .
    Returns: None
    """
    global voices
    global ready
    ready = False

    try:
        ttsengine = utils.config.get("TTS", "engine")
        voice_id = utils.config.get(ttsengine, "voiceid")
        if not voice_id:
            voice_id = utils.config.get("TTS", "voiceid")
    except Exception as e:
        logging.error(f"Error getting TTS engine or voice ID: {e}")
        return
    finally:
        ready = True

    try:
        file = utils.check_history(text)
        if file is not None and os.path.isfile(file):
            if list_voices:
                tts_client = tts_voiceid[ttsengine][voice_id]
                voices = tts_client.get_voices()
                return
            else:
                voices = None
            utils.play_audio(file, file=True)
            logging.info(f"Speech synthesized for text [{text}] from cache.")
            ready = True  # Make sure to update ready after cache playback
            return
    except Exception as e:
        logging.error(f"Error checking history or playing audio: {e}")
        ready = True  # In case of error, ensure ready is set back
        return

    logging.info(f"Speech synthesized for text [{text}].")

    try:
        if ttsengine in tts_voiceid and voice_id in tts_voiceid[ttsengine]:
            tts_client = tts_voiceid[ttsengine][voice_id]
        else:
            match ttsengine:
                case "azureTTS":
                    tts_client = init_azure_tts()
                case "googleTTS":
                    tts_client = init_google_tts()
                case "sapi5":
                    tts_client = init_sapi_tts()
                case "SherpaOnnxTTS":
                    tts_client = init_onnx_tts()
                case "googleTransTTS":
                    tts_client = init_googleTrans_tts()
                case _:
                    tts_client = pyttsx3.init(ttsengine)
    except Exception as e:
        logging.error(f"Error initializing TTS client: {e}")
        return

    try:
        if ttsengine not in tts_voiceid:
            tts_voiceid[ttsengine] = {voice_id: tts_client}
        else:
            if voice_id not in tts_voiceid[ttsengine]:
                tts_voiceid[ttsengine][voice_id] = tts_client
    except Exception as e:
        logging.error(f"Error storing TTS client: {e}")
        return

    if list_voices:
        try:
            voices = tts_client.get_voices()
            return
        except Exception as e:
            logging.error(f"Error getting voices: {e}")
            return
    else:
        voices = None

    try:
        match ttsengine:
            case "azureTTS":
                if utils.args["style"]:
                    azureSpeak(
                        text,
                        ttsengine,
                        tts_client,
                        utils.args["style"],
                        utils.args["styledegree"],
                    )
                else:
                    azureSpeak(text, ttsengine, tts_client)
            case "googleTTS":
                googleSpeak(text, ttsengine, tts_client)
            case "sapi5":
                sapiSpeak(text, ttsengine, tts_client)
            case "SherpaOnnxTTS":
                onnxSpeak(text, ttsengine, tts_client)
            case "googleTransTTS":
                googleTransSpeak(text, ttsengine, tts_client)
            case _:
                tts_client.setProperty("voice", utils.config.get("TTS", "voiceid"))
                tts_client.setProperty("rate", utils.config.get("TTS", "rate"))
                tts_client.setProperty("volume", utils.config.get("TTS", "volume"))
                tts_client.say(text)
                tts_client.runAndWait()
    except Exception as e:
        logging.error(f"Error during TTS processing: {e}")


def onnxSpeak(text: str, engine, tts_client):
    """This function received the input parameters and make necessary modification (if needed). Then, those parameter
    will be pass to ttsWrapperSpeak.

    Args:
        text (str): String to be spoken by the TTS Engine.
        engine (str): Name of the TTS Engine.
        tts_client: Instance of TTS Engine.
    Returns: None
    """

    ttsWrapperSpeak(text, tts_client, engine)


def azureSpeak(
    text: str, engine, tts_client, style: str = None, styledegree: float = None
):
    """This function received the input parameters and make necessary modification (if needed). Then, those parameter
    will be pass to ttsWrapperSpeak.

    Args:
        text (str): String to be spoken by the TTS Engine.
        engine (str): Name of the TTS Engine.
        tts_client: Instance of TTS Engine.
        style (str): Set the SSML style format and wrap the text string.
        styledegree (float): Set the SSML style degree format and wrap the text string.
    Returns: None
    """

    if style:
        # Check if the provided style is in the valid styles array
        if style in VALID_STYLES:
            # Construct SSML with the specified style
            ssml = f'<mstts:express-as style="{style}"'
            if styledegree:
                ssml += f' styledegree="{styledegree}"'
            ssml += f">{text}</mstts:express-as>"
        else:
            # Style is not valid, use default SSML without style
            ssml = text
    else:
        # Use default SSML without style
        ssml = text

    ttsWrapperSpeak(ssml, tts_client, engine)


def googleSpeak(text: str, engine, tts_client):
    """This function received the input parameters and make necessary modification (if needed). Then, those parameter
    will be pass to ttsWrapperSpeak.

    Args:
        text (str): String to be spoken by the TTS Engine.
        engine (str): Name of the TTS Engine.
        tts_client: Instance of TTS Engine.
    Returns: None
    """
    ttsWrapperSpeak(text, tts_client, engine)


def googleTransSpeak(text: str, engine, tts_client):
    """This function received the input parameters and make necessary modification (if needed). Then, those parameter
    will be pass to ttsWrapperSpeak.

    Args:
        text (str): String to be spoken by the TTS Engine.
        engine (str): Name of the TTS Engine.
        tts_client: Instance of TTS Engine.
    Returns: None
    """
    ttsWrapperSpeak(text, tts_client, engine)


def sapiSpeak(text: str, engine, tts_client):
    """This function received the input parameters and make necessary modification (if needed). Then, those parameter
    will be pass to ttsWrapperSpeak.

    Args:
        text (str): String to be spoken by the TTS Engine.
        engine (str): Name of the TTS Engine.
        tts_client: Instance of TTS Engine.
    Returns: None
    """
    ttsWrapperSpeak(text, tts_client, engine)


def ttsWrapperSpeak(text: str, tts, engine):
    """This function identifies the TTS Instance and set format of the text and audio format.
    Then, create a Thread that synthesize text to audio.

    Args:
        text (str): String to be spoken by the TTS Engine.
        tts: Instance of TTS Engine.
        engine (str): Name of the TTS Engine.
    Returns: None
    """
    fmt = "wav"
    match tts:
        case SherpaOnnxTTS():
            pass
        case GoogleTransTTS():
            fmt = "mp3"
        case SAPIEngine():
            pass
        case AbstractTTS():
            tts.ssml.clear_ssml()
            text = tts.ssml.add(text)
    try:
        playText = Thread(target=playSpeech, args=(text, engine, fmt, tts))
        playText.start()
    except Exception as e:
        print(e)


def playSpeech(text, engine, file_format, tts):
    """This function is run by a Thread which synthesize text to audio.
    While audio is streaming, the audio is also saving in parallel.

    Args:
        text (str): String to be spoken by the TTS Engine.
        engine (str): Name of the TTS Engine.
        file_format (str): Audio Format.
        tts: Instance of TTS Engine.
    Returns: None
    """
    global ready
    ready = False  # Start in an unready state

    start = time.perf_counter()
    try:
        save_audio_file = utils.config.getboolean("TTS", "save_audio_file")
        if save_audio_file:
            utils.save_audio(text=text, engine=engine, file_format=file_format, tts=tts)
            logging.info(f"Speech synthesized for text [{text}] saved in cache.")
        else:
            tts.speak_streamed(text)
    except Exception as e:
        logging.error(f"Error during TTS processing: {e}")
        return
    finally:
        stop = time.perf_counter() - start
        logging.info(f"Speech synthesis runtime is {stop:0.5f} seconds.")
        ready = True  # Ensure ready is set to True even after an exception
