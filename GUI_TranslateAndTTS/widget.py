# This Python file uses the following encoding: utf-8
import sys
import os
import configparser

from PySide6.QtWidgets import *
import PySide6.QtCore
from PySide6.QtCore import Qt, QObject, Signal, QRunnable, QThreadPool
from PySide6.QtGui import QFont, QIcon, QMovie

import pyttsx3
import uuid
import logging
import translate
import json
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget
from item import Ui_item
import requests
import tempfile
import subprocess
import pyperclip


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.movie = None
        self.currentButton = None
        self.temp_config_file = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.azure_row = None
        self.ui.textBrowser.setStyleSheet("background-color: transparent; border: none;")
        self.ui.comboBox_provider.addItems(translate.providers.__all__)
        self.ui.comboBox_provider.currentTextChanged.connect(self.setParameter)

        # Translate Language Dictionary
        self.translate_languages = {"Afrikaans": "af",
                                    "Arabic": "ar",
                                    "Bulgarian": "bg",
                                    "Bengali": "bn",
                                    "Bosnian": "bs",
                                    "Catalan": "ca",
                                    "Czech": "cs",
                                    "Danish": "da",
                                    "German": "de",
                                    "Greek": "el",
                                    "English": "en",
                                    "Spanish": "es",
                                    "Estonian": "et",
                                    "Finnish": "fi",
                                    "French": "fr",
                                    "Gujarati": "gu",
                                    "Hindi": "hi",
                                    "Croatian": "hr",
                                    "Hungarian": "hu",
                                    "Indonesian": "id",
                                    "Icelandic": "is",
                                    "Italian": "it",
                                    "Hebrew": "iw",
                                    "Japanese": "ja",
                                    "Javanese": "jw",
                                    "Khmer": "km",
                                    "Kannada": "kn",
                                    "Korean": "ko",
                                    "Kurdish (Kurmanji)": "ku",
                                    "Kurdish (Sorani)": "ckb",
                                    "Latin": "la",
                                    "Latvian": "lv",
                                    "Malayalam": "ml",
                                    "Marathi": "mr",
                                    "Malay": "ms",
                                    "Myanmar(Burmese)": "my",
                                    "Nepali": "ne",
                                    "Dutch": "nl",
                                    "Norwegian": "no",
                                    "Polish": "pl",
                                    "Portuguese": "pt",
                                    "Romanian": "ro",
                                    "Russian": "ru",
                                    "Sinhala": "si",
                                    "Slovak": "sk",
                                    "Albanian": "sq",
                                    "Serbian": "sr",
                                    "Sundanese": "su",
                                    "Swedish": "sv",
                                    "Swahili": "sw",
                                    "Tamil": "ta",
                                    "Telugu": "te",
                                    "Thai": "th",
                                    "Filipino": "tl",
                                    "Turkish": "tr",
                                    "Ukrainian": "uk",
                                    "Urdu": "ur",
                                    "Vietnamese": "vi",
                                    "Chinese(Simplified)": "zh-CN",
                                    "Chinese(Mandarin/Taiwan)": "zh-TW",
                                    "Chinese(Mandarin)": "zh"}

        voices_google = """mr-IN-Standard-A
        mr-IN-Standard-B
        mr-IN-Standard-C
        pa-IN-Standard-A
        pa-IN-Standard-B
        pa-IN-Standard-C
        pa-IN-Standard-D
        sv-SE-Standard-B
        sv-SE-Standard-C
        sv-SE-Standard-D
        sv-SE-Standard-E
        sv-SE-Standard-A
        ta-IN-Standard-C
        ta-IN-Standard-D
        yue-HK-Standard-A
        yue-HK-Standard-B
        yue-HK-Standard-C
        yue-HK-Standard-D
        bn-IN-Standard-A
        bn-IN-Standard-B
        cmn-CN-Standard-C
        cmn-CN-Standard-B
        cmn-CN-Standard-A
        cmn-CN-Standard-D
        cmn-TW-Standard-A
        cmn-TW-Standard-B
        cmn-TW-Standard-C
        gu-IN-Standard-A
        gu-IN-Standard-B
        ja-JP-Standard-A
        ja-JP-Standard-B
        ja-JP-Standard-C
        ja-JP-Standard-D
        kn-IN-Standard-A
        kn-IN-Standard-B
        ml-IN-Standard-A
        ml-IN-Standard-B
        ta-IN-Standard-A
        ta-IN-Standard-B
        af-ZA-Standard-A
        ar-XA-Standard-A
        ar-XA-Standard-B
        ar-XA-Standard-C
        ar-XA-Standard-D
        bg-BG-Standard-A
        cs-CZ-Standard-A
        da-DK-Standard-C
        da-DK-Standard-D
        da-DK-Standard-E
        da-DK-Standard-A
        de-DE-Standard-A
        de-DE-Standard-B
        de-DE-Standard-C
        de-DE-Standard-D
        de-DE-Standard-E
        de-DE-Standard-F
        en-AU-Standard-A
        en-AU-Standard-B
        en-AU-Standard-C
        en-AU-Standard-D
        en-GB-Standard-A
        en-GB-Standard-B
        en-GB-Standard-C
        en-GB-Standard-D
        en-GB-Standard-F
        en-IN-Standard-D
        en-IN-Standard-A
        en-IN-Standard-B
        en-IN-Standard-C
        en-US-Standard-A
        en-US-Standard-B
        en-US-Standard-C
        en-US-Standard-D
        en-US-Standard-E
        en-US-Standard-F
        en-US-Standard-G
        en-US-Standard-H
        en-US-Standard-I
        en-US-Standard-J
        es-ES-Standard-A
        es-ES-Standard-C
        es-ES-Standard-D
        es-ES-Standard-B
        es-US-Standard-A
        es-US-Standard-B
        es-US-Standard-C
        eu-ES-Standard-A
        fi-FI-Standard-A
        fr-CA-Standard-A
        fr-CA-Standard-B
        fr-CA-Standard-C
        fr-CA-Standard-D
        fr-FR-Standard-A
        fr-FR-Standard-B
        fr-FR-Standard-C
        fr-FR-Standard-D
        fr-FR-Standard-E
        gl-ES-Standard-A
        he-IL-Standard-D
        he-IL-Standard-A
        he-IL-Standard-B
        he-IL-Standard-C
        hi-IN-Standard-D
        hi-IN-Standard-A
        hi-IN-Standard-B
        hi-IN-Standard-C
        hu-HU-Standard-A
        is-IS-Standard-A
        lt-LT-Standard-A
        lv-LV-Standard-A
        ms-MY-Standard-A
        ms-MY-Standard-B
        ms-MY-Standard-C
        ms-MY-Standard-D
        nb-NO-Standard-A
        nb-NO-Standard-B
        nb-NO-Standard-E
        nb-NO-Standard-C
        nb-NO-Standard-D
        nl-BE-Standard-A
        nl-BE-Standard-B
        nl-NL-Standard-B
        nl-NL-Standard-C
        nl-NL-Standard-D
        nl-NL-Standard-A
        nl-NL-Standard-E
        pt-BR-Standard-A
        pt-BR-Standard-B
        pt-BR-Standard-C
        pt-PT-Standard-A
        pt-PT-Standard-B
        pt-PT-Standard-C
        pt-PT-Standard-D
        ro-RO-Standard-A
        ru-RU-Standard-E
        ru-RU-Standard-A
        ru-RU-Standard-B
        ru-RU-Standard-C
        ru-RU-Standard-D
        sk-SK-Standard-A
        sr-RS-Standard-A
        th-TH-Standard-A
        uk-UA-Standard-A
        te-IN-Standard-A
        te-IN-Standard-B
        vi-VN-Standard-A
        vi-VN-Standard-B
        vi-VN-Standard-C
        vi-VN-Standard-D
        pl-PL-Standard-A
        pl-PL-Standard-B
        pl-PL-Standard-C
        pl-PL-Standard-E
        pl-PL-Standard-D
        it-IT-Standard-B
        it-IT-Standard-C
        it-IT-Standard-D
        it-IT-Standard-A
        tr-TR-Standard-B
        tr-TR-Standard-C
        tr-TR-Standard-D
        tr-TR-Standard-A
        tr-TR-Standard-E
        ko-KR-Standard-A
        ko-KR-Standard-B
        ko-KR-Standard-C
        ko-KR-Standard-D
        id-ID-Standard-A
        id-ID-Standard-B
        id-ID-Standard-C
        id-ID-Standard-D
        el-GR-Standard-A
        ca-ES-Standard-A
        fil-PH-Standard-A
        fil-PH-Standard-B
        fil-PH-Standard-C
        fil-PH-Standard-D
        ar-XA-Wavenet-A
        ar-XA-Wavenet-B
        ar-XA-Wavenet-C
        ar-XA-Wavenet-D
        bn-IN-Wavenet-A
        bn-IN-Wavenet-B
        cmn-CN-Wavenet-A
        cmn-CN-Wavenet-B
        cmn-CN-Wavenet-C
        cmn-CN-Wavenet-D
        cmn-TW-Wavenet-A
        cmn-TW-Wavenet-B
        cmn-TW-Wavenet-C
        cs-CZ-Wavenet-A
        da-DK-Wavenet-C
        da-DK-Wavenet-D
        da-DK-Wavenet-E
        da-DK-Wavenet-A
        de-DE-Wavenet-F
        de-DE-Wavenet-A
        de-DE-Wavenet-B
        de-DE-Wavenet-C
        de-DE-Wavenet-D
        de-DE-Wavenet-E
        el-GR-Wavenet-A
        en-AU-News-E
        en-AU-News-F
        en-AU-News-G
        en-AU-Wavenet-A
        en-AU-Wavenet-B
        en-AU-Wavenet-C
        en-AU-Wavenet-D
        en-GB-News-G
        en-GB-News-H
        en-GB-News-I
        en-GB-News-J
        en-GB-News-K
        en-GB-News-L
        en-GB-News-M
        en-GB-Wavenet-A
        en-GB-Wavenet-B
        en-GB-Wavenet-C
        en-GB-Wavenet-D
        en-GB-Wavenet-F
        en-IN-Wavenet-D
        en-IN-Wavenet-A
        en-IN-Wavenet-B
        en-IN-Wavenet-C
        en-US-News-K
        en-US-News-L
        en-US-News-M
        en-US-News-N
        en-US-Wavenet-G
        en-US-Wavenet-H
        en-US-Wavenet-I
        en-US-Wavenet-J
        en-US-Wavenet-A
        en-US-Wavenet-B
        en-US-Wavenet-C
        en-US-Wavenet-D
        en-US-Wavenet-E
        en-US-Wavenet-F
        es-ES-Wavenet-C
        es-ES-Wavenet-D
        es-ES-Wavenet-B
        es-US-Wavenet-A
        es-US-Wavenet-B
        es-US-Wavenet-C
        es-US-News-G
        es-US-News-F
        es-US-News-E
        es-US-News-D
        fi-FI-Wavenet-A
        fil-PH-Wavenet-A
        fil-PH-Wavenet-B
        fil-PH-Wavenet-C
        fil-PH-Wavenet-D
        fr-CA-Wavenet-A
        fr-CA-Wavenet-B
        fr-CA-Wavenet-C
        fr-CA-Wavenet-D
        fr-FR-Wavenet-E
        fr-FR-Wavenet-A
        fr-FR-Wavenet-B
        fr-FR-Wavenet-C
        fr-FR-Wavenet-D
        gu-IN-Wavenet-A
        gu-IN-Wavenet-B
        he-IL-Wavenet-D
        he-IL-Wavenet-A
        he-IL-Wavenet-B
        he-IL-Wavenet-C
        hi-IN-Wavenet-D
        hi-IN-Wavenet-A
        hi-IN-Wavenet-B
        hi-IN-Wavenet-C
        hu-HU-Wavenet-A
        id-ID-Wavenet-D
        id-ID-Wavenet-A
        id-ID-Wavenet-B
        id-ID-Wavenet-C
        it-IT-Wavenet-A
        it-IT-Wavenet-B
        it-IT-Wavenet-C
        it-IT-Wavenet-D
        ja-JP-Wavenet-B
        ja-JP-Wavenet-C
        ja-JP-Wavenet-D
        ja-JP-Wavenet-A
        kn-IN-Wavenet-A
        kn-IN-Wavenet-B
        ko-KR-Wavenet-A
        ko-KR-Wavenet-B
        ko-KR-Wavenet-C
        ko-KR-Wavenet-D
        ml-IN-Wavenet-A
        ml-IN-Wavenet-B
        ml-IN-Wavenet-C
        ml-IN-Wavenet-D
        mr-IN-Wavenet-A
        mr-IN-Wavenet-B
        mr-IN-Wavenet-C
        ms-MY-Wavenet-A
        ms-MY-Wavenet-B
        ms-MY-Wavenet-C
        ms-MY-Wavenet-D
        nb-NO-Wavenet-A
        nb-NO-Wavenet-B
        nb-NO-Wavenet-C
        nb-NO-Wavenet-D
        nb-NO-Wavenet-E
        nl-BE-Wavenet-A
        nl-BE-Wavenet-B
        nl-NL-Wavenet-B
        nl-NL-Wavenet-C
        nl-NL-Wavenet-D
        nl-NL-Wavenet-A
        nl-NL-Wavenet-E
        pa-IN-Wavenet-A
        pa-IN-Wavenet-B
        pa-IN-Wavenet-C
        pa-IN-Wavenet-D
        pl-PL-Wavenet-A
        pl-PL-Wavenet-B
        pl-PL-Wavenet-C
        pl-PL-Wavenet-E
        pl-PL-Wavenet-D
        pt-BR-Wavenet-A
        pt-BR-Wavenet-B
        pt-BR-Wavenet-C
        pt-PT-Wavenet-A
        pt-PT-Wavenet-B
        pt-PT-Wavenet-C
        pt-PT-Wavenet-D
        ro-RO-Wavenet-A
        ru-RU-Wavenet-E
        ru-RU-Wavenet-A
        ru-RU-Wavenet-B
        ru-RU-Wavenet-C
        ru-RU-Wavenet-D
        sk-SK-Wavenet-A
        sv-SE-Wavenet-B
        sv-SE-Wavenet-D
        sv-SE-Wavenet-C
        sv-SE-Wavenet-E
        sv-SE-Wavenet-A
        ta-IN-Wavenet-A
        ta-IN-Wavenet-B
        ta-IN-Wavenet-C
        ta-IN-Wavenet-D
        tr-TR-Wavenet-B
        tr-TR-Wavenet-C
        tr-TR-Wavenet-D
        tr-TR-Wavenet-E
        tr-TR-Wavenet-A
        uk-UA-Wavenet-A
        vi-VN-Wavenet-A
        vi-VN-Wavenet-B
        vi-VN-Wavenet-C
        vi-VN-Wavenet-D
        en-US-Studio-M
        en-US-Studio-O
        es-US-Studio-B
        da-DK-Neural2-D
        de-DE-Neural2-B
        de-DE-Neural2-C
        de-DE-Neural2-D
        de-DE-Neural2-F
        de-DE-Polyglot-1
        en-AU-Polyglot-1
        en-GB-Neural2-A
        en-GB-Neural2-B
        en-GB-Neural2-C
        en-GB-Neural2-D
        en-GB-Neural2-F
        en-US-Neural2-A
        en-US-Neural2-C
        en-US-Neural2-D
        en-US-Neural2-E
        en-US-Neural2-F
        en-US-Neural2-G
        en-US-Neural2-H
        en-US-Neural2-I
        en-US-Neural2-J
        en-US-Polyglot-1
        es-ES-Neural2-A
        es-ES-Neural2-B
        es-ES-Neural2-C
        es-ES-Neural2-D
        es-ES-Neural2-E
        es-ES-Neural2-F
        es-ES-Polyglot-1
        es-US-Neural2-A
        es-US-Neural2-B
        es-US-Neural2-C
        es-US-Polyglot-1
        fil-ph-Neural2-D
        fil-ph-Neural2-A
        fr-CA-Neural2-A
        fr-CA-Neural2-B
        fr-CA-Neural2-C
        fr-CA-Neural2-D
        fr-FR-Neural2-A
        fr-FR-Neural2-B
        fr-FR-Neural2-C
        fr-FR-Neural2-D
        fr-FR-Neural2-E
        fr-FR-Polyglot-1
        hi-IN-Neural2-A
        hi-IN-Neural2-B
        hi-IN-Neural2-C
        hi-IN-Neural2-D
        it-IT-Neural2-A
        it-IT-Neural2-C
        ja-JP-Neural2-B
        ja-JP-Neural2-C
        ja-JP-Neural2-D
        ko-KR-Neural2-A
        ko-KR-Neural2-B
        ko-KR-Neural2-C
        pt-BR-Neural2-A
        pt-BR-Neural2-B
        pt-BR-Neural2-C
        vi-VN-Neural2-A
        vi-VN-Neural2-D
        th-TH-Neural2-C
        en-AU-Neural2-A
        en-AU-Neural2-B
        en-AU-Neural2-C
        en-AU-Neural2-D
        af-ZA-Standard-A
        ar-XA-Standard-A
        ar-XA-Standard-B
        ar-XA-Standard-C
        ar-XA-Standard-D
        bg-BG-Standard-A
        ca-ES-Standard-A
        cs-CZ-Standard-A
        da-DK-Standard-A
        da-DK-Standard-C
        da-DK-Standard-D
        da-DK-Standard-E
        nl-NL-Standard-A
        nl-NL-Standard-B
        nl-NL-Standard-C
        nl-NL-Standard-D
        nl-NL-Standard-E
        en-AU-Standard-A
        en-AU-Standard-B
        en-AU-Standard-C
        en-AU-Standard-D
        en-IN-Standard-A
        en-IN-Standard-B
        en-IN-Standard-C
        en-IN-Standard-D
        en-GB-Standard-A
        en-GB-Standard-B
        en-GB-Standard-C
        en-GB-Standard-D
        en-GB-Standard-F
        en-US-Standard-A
        en-US-Standard-B
        en-US-Standard-C
        en-US-Standard-D
        en-US-Standard-E
        en-US-Standard-F
        en-US-Standard-G
        en-US-Standard-H
        en-US-Standard-I
        en-US-Standard-J
        fil-PH-Standard-A
        fil-PH-Standard-B
        fil-PH-Standard-C
        fil-PH-Standard-D
        fi-FI-Standard-A
        fr-CA-Standard-A
        fr-CA-Standard-B
        fr-CA-Standard-C
        fr-CA-Standard-D
        fr-FR-Standard-A
        fr-FR-Standard-B
        fr-FR-Standard-C
        fr-FR-Standard-D
        fr-FR-Standard-E
        de-DE-Standard-A
        de-DE-Standard-B
        de-DE-Standard-C
        de-DE-Standard-D
        de-DE-Standard-E
        de-DE-Standard-F
        el-GR-Standard-A
        he-IL-Standard-A
        he-IL-Standard-B
        he-IL-Standard-C
        he-IL-Standard-D
        hi-IN-Standard-A
        hi-IN-Standard-B
        hi-IN-Standard-C
        hi-IN-Standard-D
        hu-HU-Standard-A
        is-IS-Standard-A
        id-ID-Standard-A
        id-ID-Standard-B
        id-ID-Standard-C
        id-ID-Standard-D
        it-IT-Standard-A
        it-IT-Standard-B
        it-IT-Standard-C
        it-IT-Standard-D
        ko-KR-Standard-A
        ko-KR-Standard-B
        ko-KR-Standard-C
        ko-KR-Standard-D
        lv-LV-Standard-A
        lt-LT-Standard-A
        ms-MY-Standard-A
        ms-MY-Standard-B
        ms-MY-Standard-C
        ms-MY-Standard-D
        nb-NO-Standard-A
        nb-NO-Standard-B
        nb-NO-Standard-C
        nb-NO-Standard-D
        nb-NO-Standard-E
        pl-PL-Standard-A
        pl-PL-Standard-B
        pl-PL-Standard-C
        pl-PL-Standard-D
        pl-PL-Standard-E
        pt-BR-Standard-A
        pt-BR-Standard-B
        pt-BR-Standard-C
        pt-PT-Standard-A
        pt-PT-Standard-B
        pt-PT-Standard-C
        pt-PT-Standard-D
        ro-RO-Standard-A
        ru-RU-Standard-A
        ru-RU-Standard-B
        ru-RU-Standard-C
        ru-RU-Standard-D
        ru-RU-Standard-E
        sr-RS-Standard-A
        sk-SK-Standard-A
        es-ES-Standard-A
        es-ES-Standard-B
        es-ES-Standard-D
        th-TH-Standard-A
        tr-TR-Standard-A
        tr-TR-Standard-B
        tr-TR-Standard-C
        tr-TR-Standard-D
        tr-TR-Standard-E
        uk-UA-Standard-A
        vi-VN-Standard-A
        vi-VN-Standard-B
        vi-VN-Standard-C
        vi-VN-Standard-D
        es-US-Standard-A
        es-US-Standard-B
        es-US-Standard-C
        eu-ES-Standard-A
        gl-ES-Standard-A
        nl-BE-Standard-A
        nl-BE-Standard-B
        pa-IN-Standard-A
        pa-IN-Standard-B
        pa-IN-Standard-C
        pa-IN-Standard-D
        sv-SE-Standard-A
        sv-SE-Standard-B
        sv-SE-Standard-C
        sv-SE-Standard-D
        sv-SE-Standard-E
        ta-IN-Standard-C
        ta-IN-Standard-D
        yue-HK-Standard-A
        yue-HK-Standard-B
        yue-HK-Standard-C
        yue-HK-Standard-D
        bn-IN-Standard-A
        bn-IN-Standard-B
        cmn-CN-Standard-A
        cmn-CN-Standard-B
        cmn-CN-Standard-C
        cmn-CN-Standard-D
        cmn-TW-Standard-A
        cmn-TW-Standard-B
        cmn-TW-Standard-C
        gu-IN-Standard-A
        gu-IN-Standard-B
        ja-JP-Standard-A
        ja-JP-Standard-B
        ja-JP-Standard-C
        ja-JP-Standard-D
        kn-IN-Standard-A
        kn-IN-Standard-B
        ml-IN-Standard-A
        ml-IN-Standard-B
        mr-IN-Standard-A
        mr-IN-Standard-B
        mr-IN-Standard-C
        ta-IN-Standard-A
        ta-IN-Standard-B
        te-IN-Standard-A
        te-IN-Standard-B"""

        voices_google = voices_google.replace(" ", "")
        # Split the text into lines
        voices_google = voices_google.split("\n")
        voices_google = sorted(voices_google)  # Google voices

        self.ui.listWidget_voicegoogle.addItems(voices_google)
        self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
        self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))

        voices_sapi = pyttsx3.init('sapi5').getProperty('voices')
        self.voices_sapi_dict = {}
        for voice in voices_sapi:
            import re
            # Define regular expressions to extract voice ID and name
            voice_id_pattern = r"id=(.*?)\n"
            name_pattern = r"name=(.*?)\n"

            # Search for the patterns in the text
            voice_id_match = re.search(voice_id_pattern, str(voice))
            name_match = re.search(name_pattern, str(voice))

            if voice_id_match and name_match:
                voice_id = voice_id_match.group(1).strip()
                name = name_match.group(1).strip()

                self.voices_sapi_dict[name] = voice_id

        self.ui.listWidget_sapi.addItems(self.voices_sapi_dict.keys())
        self.ui.listWidget_sapi.setCurrentRow(0)
        if getattr(sys, 'frozen', False):
            # Get the path to the user's app data folder
            home_directory = os.path.expanduser("~")
            app_data_path = os.path.join(home_directory, 'AppData', 'Roaming', 'TranslateAndTTS')
        elif __file__:
            app_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        self.config_path = os.path.join(app_data_path, 'settings.cfg')

        self.config = configparser.ConfigParser()
        self.setWindowTitle("Configure TranslateAndTTS: {}".format(self.config_path))
        # Check if the file already exists
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
            self.generate_azure_voice_models()

            self.notranslate = self.ttsEngine = self.config.getboolean('translate', 'noTranslate')
            self.startLang = self.config.get('translate', 'startLang')
            self.endLang = self.config.get('translate', 'endLang')
            self.overwritePb = self.config.getboolean('translate', 'replacepb')
            self.provider = self.config.get('translate', 'provider')
            self.ui.comboBox_provider.setCurrentIndex(self.ui.comboBox_provider.findText(self.provider))
            if self.provider == 'MyMemoryProvider':
                self.ui.mymemory_secret_key.setText(self.config.get('translate', 'MyMemoryProvider_secret_key'))
                self.ui.email_mymemory.setText(self.config.get('translate', 'email'))
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.mymemory))
            if self.provider == 'LibreProvider':
                self.ui.LibreTranslate_secret_key.setText(self.config.get('translate', 'LibreProvider_secret_key'))
                self.ui.LibreTranslate_url.setText(self.config.get('translate', 'url'))
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.libretranslate))
            if self.provider == 'DeeplProvider':
                self.ui.deepl_secret_key.setText(self.config.get('translate', 'DeeplProvider_secret_key'))
                self.ui.checkBox_pro.setChecked(self.config.getboolean('translate', 'deepl_pro'))
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.deepl))
            if self.provider == 'MicrosoftProvider':
                self.ui.microsoft_secret_key.setText(self.config.get('translate', 'MicrosoftProvider_secret_key'))
                self.ui.microsoft_region.setText(self.config.get('translate', 'region'))
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.microsoft))

            self.ttsEngine = self.config.get('TTS', 'engine')
            self.voiceid = self.config.get('TTS', 'voiceid')
            self.rate = self.config.getint('TTS', 'rate')
            self.volume = self.config.getint('TTS', 'volume')

            self.key = self.config.get('azureTTS', 'key')
            self.region = self.config.get('azureTTS', 'location')
            self.voiceidAzure = self.config.get('azureTTS', 'voiceid')
            self.saveAudio = self.config.getboolean('TTS', 'save_audio_file')

            self.credsFilePath = self.config.get('googleTTS', 'creds_file')
            self.voiceidGoogle = self.config.get('googleTTS', 'voiceid')

            self.voiceid_sapi = self.config.get('sapi5TTS', 'voiceid')

            if self.ttsEngine == "azureTTS":
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.radioButton_azure.setChecked(True)
            elif self.ttsEngine == "gTTS":
                self.ui.stackedWidget.setCurrentIndex(1)
                self.ui.radioButton_google.setChecked(True)
            elif self.ttsEngine == "gspeak":
                self.ui.stackedWidget.setCurrentIndex(2)
                self.ui.radioButton_gspeak.setChecked(True)
            elif self.ttsEngine == "sapi5":
                self.ui.stackedWidget.setCurrentIndex(3)
                self.ui.radioButton_sapi5.setChecked(True)
            elif self.ttsEngine == "kurdishTTS":
                self.ui.stackedWidget.setCurrentIndex(4)
                self.ui.radioButton_kurdish.setChecked(True)
            elif self.ttsEngine == "espeak":
                self.ui.stackedWidget.setCurrentIndex(5)
                self.ui.radioButton_espeak.setChecked(True)
            elif self.ttsEngine == "nsss":
                self.ui.stackedWidget.setCurrentIndex(5)
                self.ui.radioButton_nsss.setChecked(True)
            elif self.ttsEngine == "coqui":
                self.ui.stackedWidget.setCurrentIndex(5)
                self.ui.radioButton_coqui.setChecked(True)
            else:
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.radioButton_azure.setChecked(True)

            lang = [key for key, value in self.translate_languages.items() if value == self.startLang]
            if not len(lang) == 0:
                lang = lang[0]
            self.ui.comboBox_writeLang.setCurrentText(lang)

            lang = [key for key, value in self.translate_languages.items() if value == self.endLang]
            if not len(lang) == 0:
                lang = lang[0]
            self.ui.comboBox_targetLang.setCurrentText(lang)

            # item = self.ui.listWidget_voiceazure.findItems(self.voiceidAzure, PySide6.QtCore.Qt.MatchExactly)
            # self.ui.listWidget_voiceazure.setCurrentItem(item[0])
            self.set_azure_voice(self.voiceidAzure)
            # TODO: Uncomment later

            item = self.ui.listWidget_voicegoogle.findItems(self.voiceidGoogle, PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voicegoogle.setCurrentItem(item[0])

            item = [key for key, value in self.voices_sapi_dict.items() if value == self.voiceid_sapi]

            item = self.ui.listWidget_sapi.findItems(item[0], PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_sapi.setCurrentItem(item[0])

            self.ui.checkBox_translate.setChecked(not self.notranslate)
            self.ui.checkBox_overwritepb.setChecked(self.overwritePb)
            self.ui.checkBox_saveAudio.setChecked(self.saveAudio)

            self.ui.horizontalSlider_rate.setValue(self.rate)
            self.ui.horizontalSlider_volume.setValue(self.volume)
            self.ui.horizontalSlider_rate_sapi.setValue(self.rate)
            self.ui.horizontalSlider_volume_sapi.setValue(self.volume)
            self.ui.lineEdit_voiceID.setText(self.voiceid)
            self.ui.lineEdit_key.setText(self.key)
            self.ui.lineEdit_region.setText(self.region)

            self.ui.checkBox_saveAudio_gTTS.setChecked(self.saveAudio)
            self.ui.credsFilePathEdit.setText(self.credsFilePath)

            self.ui.checkBox_saveAudio_sapi.setChecked(self.saveAudio)
            self.ui.checkBox_saveAudio_kurdish.setChecked(self.saveAudio)

            self.ui.checkBox_latin.setChecked(self.config.getboolean('kurdishTTS', 'latin'))
            self.ui.checkBox_punctuation.setChecked(self.config.getboolean('kurdishTTS', 'punctuation'))

            self.ui.checkBox_stats.setChecked(self.config.getboolean('App', 'collectstats'))
            # use self.onTTSEngineToggled() to refresh TTS engine setting upon start-up
            self.onTTSEngineToggled()

        else:
            self.generate_azure_voice_models()
            self.ttsEngine = "azureTTS"
            self.ui.stackedWidget.setCurrentIndex(0)

            self.notranslate = False
            self.saveAudio_azure = True
            self.overwritePb = True

            self.voiceid = None
            self.voiceidAzure = "en-US-JennyNeural"
            self.voiceidGoogle = "en-US-Wavenet-C"

            self.rate = None
            self.volume = None

            self.key = None
            self.region = None
            self.startLang = None
            self.endLang = None

            self.credsFilePath = ""
            self.saveAudio_google = True

            self.saveAudio_sapi5 = True

            item = self.ui.listWidget_voiceazure.findItems(self.voiceidAzure, PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voiceazure.setCurrentItem(item[0])

            item = self.ui.listWidget_voicegoogle.findItems(self.voiceidGoogle, PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voicegoogle.setCurrentItem(item[0])

        self.ui.radioButton_azure.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_google.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_nsss.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_coqui.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_espeak.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_sapi5.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_gspeak.toggled.connect(self.onTTSEngineToggled)

        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(lambda: self.OnSavePressed(True))
        self.ui.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.OnDiscardPressed)

        self.ui.browseButton.clicked.connect(self.OnBrowseButtonPressed)
        self.ui.groupBox_translate.setVisible(self.ui.checkBox_translate.isChecked())

        self.ui.credsFilePathEdit.textChanged.connect(self.OnCredsFilePathChanged)
        # use self.onTTSEngineToggled() to refresh TTS engine setting upon start-up
        self.onTTSEngineToggled()

    def onTTSEngineToggled(self):
        # move this on every TTS "if" condition if necessary.
        index = self.ui.comboBox_targetLang.currentIndex()
        self.ui.comboBox_targetLang.clear()
        self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
        self.ui.comboBox_targetLang.setCurrentIndex(index)

        if self.ui.radioButton_azure.isChecked():
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ttsEngine = "azureTTS"
        elif self.ui.radioButton_google.isChecked():
            self.ttsEngine = "gTTS"
            self.ui.stackedWidget.setCurrentIndex(1)
        elif self.ui.radioButton_gspeak.isChecked():
            self.ttsEngine = "gspeak"
            self.ui.stackedWidget.setCurrentIndex(2)
        elif self.ui.radioButton_sapi5.isChecked():
            self.ttsEngine = "sapi5"
            self.ui.stackedWidget.setCurrentIndex(3)
        elif self.ui.radioButton_kurdish.isChecked():
            self.ttsEngine = "kurdishTTS"
            self.ui.stackedWidget.setCurrentIndex(4)
            self.ui.comboBox_targetLang.clear()
            self.ui.comboBox_targetLang.addItems(["Kurdish (Kurmanji)", "Kurdish (Sorani)"])
        else:
            self.ui.stackedWidget.setCurrentIndex(5)
            if self.ui.radioButton_espeak.isChecked():
                self.ttsEngine = "espeak"
            elif self.ui.radioButton_espeak.isChecked():
                self.ttsEngine = "nsss"
            elif self.ui.radioButton_espeak.isChecked():
                self.ttsEngine = "coqui"
            else:
                self.ttsEngine = "azureTTS"

    def OnSavePressed(self, permanent=True):
        # Add sections and key-value pairs
        self.startLang = self.translate_languages[self.ui.comboBox_writeLang.currentText()]
        self.endLang = self.translate_languages[self.ui.comboBox_targetLang.currentText()]
        self.notranslate = not self.ui.checkBox_translate.isChecked()

        identifier = self.get_uuid()
        # TODO: check this function later
        self.config.clear()

        self.config.add_section('App')
        self.config.set('App', 'uuid', str(identifier))
        self.config.set('App', 'collectstats', str(self.ui.checkBox_stats.isChecked()))

        self.config.add_section('translate')
        self.config.set('translate', 'noTranslate', str(self.notranslate))
        self.config.set('translate', 'startLang', self.startLang)
        self.config.set('translate', 'endLang', self.endLang)
        self.config.set('translate', 'replacepb', str(self.ui.checkBox_overwritepb.isChecked()))
        self.config.set('translate', 'provider', str(self.ui.comboBox_provider.currentText()))

        self.config.set('translate', 'MyMemoryProvider_secret_key', self.ui.mymemory_secret_key.text())
        self.config.set('translate', 'email', self.ui.email_mymemory.text())
        self.config.set('translate', 'LibreProvider_secret_key', self.ui.LibreTranslate_secret_key.text())
        self.config.set('translate', 'url', self.ui.LibreTranslate_url.text())
        self.config.set('translate', 'DeeplProvider_secret_key', self.ui.deepl_secret_key.text())
        self.config.set('translate', 'deepL_pro', str(self.ui.checkBox_pro.isChecked()).lower())
        self.config.set('translate', 'MicrosoftProvider_secret_key', self.ui.microsoft_secret_key.text())
        self.config.set('translate', 'region', self.ui.microsoft_region.text())

        self.config.add_section('TTS')
        self.config.set('TTS', 'engine', self.ttsEngine)
        if self.ttsEngine == 'azureTTS':
            if permanent:
                self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio.isChecked()))
            else:
                self.config.set('TTS', 'save_audio_file', str(False))
        elif self.ttsEngine == 'gTTS':
            if permanent:
                self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio_gTTS.isChecked()))
            else:
                self.config.set('TTS', 'save_audio_file', str(False))
        elif self.ttsEngine == 'sapi5':
            self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio_sapi.isChecked()))
        elif self.ttsEngine == 'kurdishTTS':
            self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio_kurdish.isChecked()))
        else:
            self.config.set('TTS', 'save_audio_file', str(False))

        self.config.set('TTS', 'voiceid', self.ui.lineEdit_voiceID.text())
        if self.ttsEngine == 'sapi5':
            self.config.set('TTS', 'rate', str(self.ui.horizontalSlider_rate_sapi.value()))
            self.config.set('TTS', 'volume', str(self.ui.horizontalSlider_volume_sapi.value()))
        else:
            self.config.set('TTS', 'rate', str(self.ui.horizontalSlider_rate.value()))
            self.config.set('TTS', 'volume', str(self.ui.horizontalSlider_volume.value()))

        self.config.add_section('azureTTS')
        self.config.set('azureTTS', 'key', self.ui.lineEdit_key.text())
        self.config.set('azureTTS', 'location', self.ui.lineEdit_region.text())
        # TODO: Set this data after finishing groupbox of azure
        # print(self.ui.listWidget_voiceazure.currentItem().toolTip())
        self.config.set('azureTTS', 'voiceid', self.ui.listWidget_voiceazure.currentItem().toolTip())

        self.config.add_section('googleTTS')
        self.config.set('googleTTS', 'creds_file', self.credsFilePath)
        self.config.set('googleTTS', 'voiceid', self.ui.listWidget_voicegoogle.currentItem().text())

        self.config.add_section('sapi5TTS')
        self.config.set('sapi5TTS', 'voiceid', self.voices_sapi_dict[self.ui.listWidget_sapi.currentItem().text()])

        self.config.add_section('kurdishTTS')
        self.config.set('kurdishTTS', 'latin', str(self.ui.checkBox_latin.isChecked()).lower())
        self.config.set('kurdishTTS', 'punctuation', str(self.ui.checkBox_punctuation.isChecked()).lower())

        self.config.add_section('appCache')
        self.config.set('appCache', 'threshold', '7')

        start_lang_is_Kurdish = self.startLang == 'ckb' or self.startLang == 'ku'
        end_lang_is_Kurdish = self.endLang == 'ckb' or self.endLang == 'ku'
        prompt1 = False
        prompt2 = False
        if self.notranslate:
            if self.ttsEngine != "kurdishTTS":
                if start_lang_is_Kurdish:
                    prompt1 = True
            else:
                if not start_lang_is_Kurdish:
                    prompt2 = True

        else:
            if self.ttsEngine != "kurdishTTS":
                if end_lang_is_Kurdish:
                    prompt1 = True
            else:
                if not end_lang_is_Kurdish:
                    prompt2 = True

        msg = ""
        if prompt1:
            msg = 'Do you really want to save?\n'
            msg += 'Tip:\n'
            msg += 'Choose Kurdish TTS Engine for these settings.'

        if prompt2:
            msg = 'Do you really want to save?\n'
            msg += 'Tip:\n'
            msg += 'Choose TTS Engine other than Kurdish TTS.'

        if prompt1 or prompt2:
            reply = QMessageBox.question(self, 'Confirmation', msg,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.No:
                return

        # Write the configuration to a file
        if permanent:
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
                logging.info("Configuration file is saved on {}".format(self.config_path))
            self.close()
        else:
            self.temp_config_file = tempfile.NamedTemporaryFile(delete=False)
            with open(self.temp_config_file.name, 'w') as configfile:
                self.config.write(configfile)
                logging.info("Configuration file is saved on {}".format(self.temp_config_file.name))

    def OnDiscardPressed(self):
        self.close()

    def OnBrowseButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.credsFilePath, _ = QFileDialog.getOpenFileName(self, "Open JSON File containing OAuth 2.0 Credentials", "",
                                                            "JSON Files (*.json)", options=options)
        self.ui.credsFilePathEdit.setText(self.credsFilePath)

    def OnCredsFilePathChanged(self):
        self.credsFilePath = self.ui.credsFilePathEdit.text()

    def get_uuid(self):
        try:
            # Code that may raise an exception\
            if os.path.isfile(self.config_path) and self.config.has_section('App'):
                id = self.config.get('App', 'uuid')
                identifier = uuid.UUID(id)
        except Exception as e:
            # Code to handle other exceptions
            identifier = uuid.uuid4()
            logging.error("UUID Error: {}".format(e), exc_info=False)
            pass

        return identifier

    def setParameter(self, string):
        if string == 'MyMemoryProvider':
            try:
                if os.path.exists(self.config_path):
                    self.ui.mymemory_secret_key.setText(self.config.get('translate', 'MyMemoryProvider_secret_key'))
                    self.ui.email_mymemory.setText(self.config.get('translate', 'email'))
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.mymemory))
        if string == 'LibreProvider':
            try:
                if os.path.exists(self.config_path):
                    self.ui.LibreTranslate_secret_key.setText(self.config.get('translate', 'LibreProvider_secret_key'))
                    self.ui.LibreTranslate_url.setText(self.config.get('translate', 'url'))
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(
                self.ui.stackedWidget_provider.indexOf(self.ui.libretranslate))
        if string == 'DeeplProvider':
            try:
                if os.path.exists(self.config_path):
                    self.ui.deepl_secret_key.setText(self.config.get('translate', 'DeeplProvider_secret_key'))
                    self.ui.checkBox_pro.setChecked(self.config.getboolean('translate', 'deepl_pro'))
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.deepl))
        if string == 'MicrosoftProvider':
            try:
                if os.path.exists(self.config_path):
                    self.ui.microsoft_secret_key.setText(self.config.get('translate', 'MicrosoftProvider_secret_key'))
                    self.ui.microsoft_region.setText(self.config.get('translate', 'region'))
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.microsoft))

    def set_azure_voice(self, text):
        for index in range(self.ui.listWidget_voiceazure.count()):
            item = self.ui.listWidget_voiceazure.item(index)
            if text == item.toolTip():
                self.azure_row = self.ui.listWidget_voiceazure.row(item)
                self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                # print(self.ui.listWidget_voiceazure.row(item))
                break

    def preview_pressed(self):
        self.currentButton = self.sender()
        parent = self.sender().parent().parent()
        widget_page = parent.widget(1)
        child = widget_page.findChild(QLabel)
        # print(child.text())
        text = self.sender().parent().parent().parent().objectName()
        for index in range(self.ui.listWidget_voiceazure.count()):
            item = self.ui.listWidget_voiceazure.item(index)
            if text == item.toolTip():
                self.azure_row = self.ui.listWidget_voiceazure.row(item)
                self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                print(text)
                break
        if self.ui.lineEdit_key.text() == '':
            self.ui.lineEdit_key.setFocus()
            return
        if self.ui.lineEdit_region == '':
            self.ui.lineEdit_region.setFocus()
            return
        self.OnSavePressed(False)
        # print(self.temp_config_file.name)
        pyperclip.copy("Hello World")
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        print(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()
        runnable = Player(self.temp_config_file)
        runnable.signals.completed.connect(self.enablePlayButtons)
        buttons = self.ui.listWidget_voiceazure.findChildren(QPushButton)
        self.movie = QMovie(":/images/images/loading.gif")
        self.movie.updated.connect(self.update_Buttons)
        self.movie.start()
        for button in buttons:
            button.setEnabled(False)
        pool.start(runnable)
    
    def update_Buttons(self):
        loading_icon = QIcon(self.movie.currentPixmap())
        self.currentButton.setIcon(loading_icon)
        
    def enablePlayButtons(self):
        buttons = self.ui.listWidget_voiceazure.findChildren(QPushButton)
        for button in buttons:
            button.setEnabled(True)
        self.movie.stop()
        icon = QIcon()
        icon.addFile(":/images/images/play-round-icon.png")
        self.currentButton.setIcon(icon)
        self.temp_config_file.close()
        self.azure_playback = False
        os.unlink(self.temp_config_file.name)

    def print_data(self, item):
        try:
            widget = self.ui.listWidget_voiceazure.itemWidget(item)
            # child = widget.findChild(QLabel)
            # print(child.text())
            self.ui.listWidget_voiceazure.setCurrentItem(item)
            print(item.toolTip())
        except Exception as error:
            pass

    def updateRow(self, row):
        try:
            if self.ui.listWidget_voiceazure.currentRow() == 0:
                self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                self.ui.listWidget_voiceazure.setCurrentItem(self.ui.listWidget_voiceazure.item(self.azure_row))
        except Exception as error:
            pass

    def generate_azure_voice_models(self):
        list_widget = QListWidget()
        self.ui.listWidget_voiceazure.currentRowChanged.connect(self.updateRow)
        self.ui.listWidget_voiceazure.itemClicked.connect(self.print_data)
        voices = self.get_azure_voices()
        voices.reverse()
        for index, voice in enumerate(voices):
            voice_country = voice['LocaleName']
            try:
                if voice_country == voices[index + 1]['LocaleName']:
                    item_widget = QWidget()
                    item_UI = Ui_item()
                    item_UI.setupUi(item_widget)
                    item_UI.data.setText(str(voice))
                    item_UI.name.setText(voice['DisplayName'] + " " + voice['VoiceType'])
                    font = QFont()
                    font.setBold(False)
                    font.setPointSize(8)
                    item_UI.gender.setFont(font)
                    item_UI.gender.setText(voice['Gender'])
                    item_UI.play.clicked.connect(self.preview_pressed)
                    item_widget.setObjectName(voice['ShortName'])

                    item = QListWidgetItem()
                    item.setToolTip(voice['ShortName'])
                    item.setSizeHint(item_widget.sizeHint())
                    self.ui.listWidget_voiceazure.insertItem(index, item)
                    self.ui.listWidget_voiceazure.setItemWidget(item, item_widget)
                else:
                    item_widget = QWidget()
                    item_UI = Ui_item()
                    item_UI.setupUi(item_widget)
                    item_UI.data.setText(str(voice))
                    item_UI.name.setText(voice['DisplayName'] + " " + voice['VoiceType'])
                    font = QFont()
                    font.setBold(False)
                    font.setPointSize(8)
                    item_UI.gender.setFont(font)
                    item_UI.gender.setText(voice['Gender'])
                    item_UI.play.clicked.connect(self.preview_pressed)
                    item_widget.setObjectName(voice['ShortName'])

                    item = QListWidgetItem()
                    item.setToolTip(voice['ShortName'])
                    item.setSizeHint(item_widget.sizeHint())
                    self.ui.listWidget_voiceazure.insertItem(index, item)
                    self.ui.listWidget_voiceazure.setItemWidget(item, item_widget)

                    label_widget = QLabel(voice_country)
                    label_widget.setObjectName(voice_country)
                    label_widget.setAlignment(Qt.AlignCenter)
                    item = QListWidgetItem()
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                    self.ui.listWidget_voiceazure.addItem(item)
                    self.ui.listWidget_voiceazure.setItemWidget(item, label_widget)
            except Exception as error:
                item_widget = QWidget()
                item_UI = Ui_item()
                item_UI.setupUi(item_widget)
                item_UI.data.setText(str(voice))
                item_UI.name.setText(voice['DisplayName'] + " " + voice['VoiceType'])
                font = QFont()
                font.setBold(False)
                font.setPointSize(8)
                item_UI.gender.setFont(font)
                item_UI.gender.setText(voice['Gender'])
                item_UI.play.clicked.connect(self.preview_pressed)
                item_widget.setObjectName(voice['ShortName'])

                item = QListWidgetItem()
                item.setToolTip(voice['ShortName'])
                item.setSizeHint(item_widget.sizeHint())
                self.ui.listWidget_voiceazure.insertItem(index, item)
                self.ui.listWidget_voiceazure.setItemWidget(item, item_widget)

                label_widget = QLabel(voice_country)
                label_widget.setObjectName(voice_country)
                label_widget.setAlignment(Qt.AlignCenter)
                item = QListWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                self.ui.listWidget_voiceazure.addItem(item)
                self.ui.listWidget_voiceazure.setItemWidget(item, label_widget)

    def get_azure_voices(self):
        try:
            key = self.config.get('azureTTS', 'key')
            location = self.config.get('azureTTS', 'location')
            endpoint = f'https://{location}.tts.speech.microsoft.com/cognitiveservices/voices/list'
            response = requests.get(url=endpoint, headers={"Ocp-Apim-Subscription-Key": key})
            self.voice_list = response.json()
            print("Azure voice list fetched from API.")
            logging.info("Azure voice list fetched from API.")
        except Exception as error:
            file = PySide6.QtCore.QFile(":/binary/azure_voices.json")
            if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
                text = PySide6.QtCore.QTextStream(file).readAll()
                self.voice_list = json.loads(text.encode())
                print("Azure voice list fetched from Resource file.")
                logging.info("Azure voice list fetched from Resource file.")
                file.close()

        # print(voice_list)
        return self.voice_list


class Signals(QObject):
    started = Signal()
    completed = Signal()


class Player(QRunnable):

    def __init__(self, file):
        super().__init__()
        self.temp_config_file = file
        self.signals = Signals()

    def run(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            exe_name = ""
            for root, dirs, files in os.walk(application_path):
                for file in files:
                    if "translatepb.exe" in file:
                        exe_name = file
            GUI_path = os.path.join(application_path, exe_name)
            print(GUI_path)
            # Use subprocess.Popen to run the executable
            process = subprocess.Popen(GUI_path)
            process.wait()
        elif __file__:
            application_path = os.path.dirname(os.path.dirname(__file__))
            GUI_script_path = os.path.join(application_path, 'translatepb.py')
            process = subprocess.Popen(["python", GUI_script_path, "--config", self.temp_config_file.name, "--preview"])
            process.wait()
        self.signals.completed.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
