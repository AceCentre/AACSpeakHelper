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
from google.cloud import texttospeech
from google.oauth2 import service_account
from langcodes import *
from gtts import lang as gtts_language_list
from deep_translator import __all__ as providers
from deep_translator import constants as language_codes_list
from deep_translator import *


class Widget(QWidget):
    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.translate_instance = None
        self.available_language = None
        self.screenSize = size
        self.language_azure_list = None
        self.google_row = None
        self.google_client = None
        self.voice_google_list = None
        self.voice_list = None
        self.movie = None
        self.currentButton = None
        self.temp_config_file = None
        self.azure_row = None
        self.cleaning = False
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.textBrowser.setStyleSheet("background-color: transparent; border: none;")
        self.ui.copyApp.clicked.connect(self.copyAppPath)
        self.providers = []
        for translator in providers:
            if "Translator" in translator:
                self.providers.append(translator)
        self.ui.comboBox_provider.addItems(self.providers)
        self.ui.comboBox_provider.currentTextChanged.connect(self.setParameter)
        self.ui.deepl_secret_key.textChanged.connect(self.updateLanguage)
        self.ui.tabWidget.setTabText(0, "TTS Engine")
        self.ui.tabWidget.setTabText(1, "Translate Settings")
        self.ui.tabWidget.setTabText(2, "Application Settings")
        self.tts_dict = {}
        # self.generate_translate_list()
        # TODO: removed this translation list later
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
            self.app_data_path = os.path.join(home_directory, 'AppData', 'Roaming', 'TranslateAndTTS')
            self.ui.appPath.setText(os.path.join(self.app_data_path, "translatepb.exe"))
        elif __file__:
            self.app_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
            self.ui.appPath.setText(os.path.join(self.app_data_path, "translatepb.py"))
        self.audio_path = os.path.join(self.app_data_path, 'Audio Files')
        self.ui.clear_cache.clicked.connect(self.cache_clear)
        self.ui.open_cache.clicked.connect(self.cache_open)
        self.config_path = os.path.join(self.app_data_path, 'settings.cfg')

        self.config = configparser.ConfigParser()
        self.setWindowTitle("Configure TranslateAndTTS: {}".format(self.config_path))
        # Check if the file already exists
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
            self.generate_azure_voice_models()
            self.generate_google_voice_models()
            self.get_microsoft_language()
            self.notranslate = self.ttsEngine = self.config.getboolean('translate', 'noTranslate')
            self.startLang = self.config.get('translate', 'startLang')
            self.endLang = self.config.get('translate', 'endLang')
            self.overwritePb = self.config.getboolean('translate', 'replacepb')
            self.provider = self.config.get('translate', 'provider')
            self.ui.comboBox_provider.setCurrentIndex(self.ui.comboBox_provider.findText(self.provider))
            if self.provider == 'MyMemoryTranslator':
                self.ui.mymemory_secret_key.setText(self.config.get('translate', 'MyMemoryTranslator_secret_key'))
                self.ui.email_mymemory.setText(self.config.get('translate', 'email'))
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.mymemory))
            if self.provider == 'LibreTranslator':
                self.ui.LibreTranslate_secret_key.setText(self.config.get('translate', 'LibreTranslator_secret_key'))
                self.ui.LibreTranslate_url.setText(self.config.get('translate', 'url'))
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.libretranslate))
            if self.provider == 'DeeplTranslator':
                self.ui.deepl_secret_key.setText(self.config.get('translate', 'DeeplTranslator_secret_key'))
                self.ui.checkBox_pro.setChecked(self.config.getboolean('translate', 'deepl_pro'))
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.deepl))
            if self.provider == 'MicrosoftTranslator':
                self.ui.microsoft_secret_key.setText(self.config.get('translate', 'MicrosoftTranslator_secret_key'))
                self.ui.microsoft_region.setText(self.config.get('translate', 'region'))
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.microsoft))
            # TODO: Add other translators
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
                self.comboBox = 'Azure TTS'
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.ttsEngineBox.setCurrentText('Azure TTS')
            elif self.ttsEngine == "gTTS":
                self.comboBox = 'Google TTS'
                self.ui.stackedWidget.setCurrentIndex(1)
                self.ui.ttsEngineBox.setCurrentText('Google TTS')
            elif self.ttsEngine == "gspeak":
                self.comboBox = 'GSpeak'
                self.ui.stackedWidget.setCurrentIndex(2)
                self.ui.ttsEngineBox.setCurrentText('GSpeak')
            elif self.ttsEngine == "sapi5":
                self.comboBox = 'Sapi5 (Windows)'
                self.ui.stackedWidget.setCurrentIndex(3)
                self.ui.ttsEngineBox.setCurrentText('Sapi5 (Windows)')
            elif self.ttsEngine == "kurdishTTS":
                self.comboBox = 'Kurdish TTS'
                self.ui.stackedWidget.setCurrentIndex(4)
                self.ui.ttsEngineBox.setCurrentText('Kurdish TTS')
            elif self.ttsEngine == "espeak":
                self.comboBox = 'espeak (Unsupported)'
                self.ui.stackedWidget.setCurrentIndex(5)
                self.ui.ttsEngineBox.setCurrentText('espeak (Unsupported)')
            elif self.ttsEngine == "nsss":
                self.comboBox = 'NSS (Mac Only)'
                self.ui.stackedWidget.setCurrentIndex(5)
                self.ui.ttsEngineBox.setCurrentText('NSS (Mac Only)')
            elif self.ttsEngine == "coqui":
                self.comboBox = 'coqui_ai_tts (Unsupported)'
                self.ui.stackedWidget.setCurrentIndex(5)
                self.ui.ttsEngineBox.setCurrentText('coqui_ai_tts (Unsupported)')
            else:
                self.comboBox = 'Azure TTS'
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.ttsEngineBox.setCurrentText('Azure TTS')
            self.set_Translate_dropdown(self.translate_languages)
            # lang = [key for key, value in self.translate_languages.items() if value == self.startLang]
            # if not len(lang) == 0:
            #     lang = lang[0]
            # self.ui.comboBox_writeLang.setCurrentText(lang)
            #
            # lang = [key for key, value in self.translate_languages.items() if value == self.endLang]
            # if not len(lang) == 0:
            #     lang = lang[0]
            # self.ui.comboBox_targetLang.setCurrentText(lang)

            self.set_azure_voice(self.voiceidAzure)
            self.set_google_voice(self.voiceidGoogle)

            item = [key for key, value in self.voices_sapi_dict.items() if value == self.voiceid_sapi]

            if len(item) > 0:
                item = self.ui.listWidget_sapi.findItems(item[0], PySide6.QtCore.Qt.MatchExactly)
                self.ui.listWidget_sapi.setCurrentItem(item[0])
            elif self.ui.listWidget_sapi.count() > 0:
                self.ui.listWidget_sapi.setCurrentRow(0)
                self.ui.listWidget_sapi.setCurrentItem(self.ui.listWidget_sapi.item(0))

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
            self.ui.spinBox_threshold.setValue(int(self.config.get('appCache', 'threshold')))
            # use self.onTTSEngineToggled() to refresh TTS engine setting upon start-up
            # self.onTTSEngineToggled()

        else:
            self.generate_azure_voice_models()
            self.generate_google_voice_models()
            self.get_microsoft_language()
            self.ttsEngine = "azureTTS"
            self.comboBox = 'Azure TTS'
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

            self.set_azure_voice(self.voiceidAzure)
            self.set_google_voice(self.voiceidGoogle)
            self.ui.spinBox_threshold.setValue(7)

        self.ui.ttsEngineBox.currentTextChanged.connect(self.onTTSEngineToggled)

        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(lambda: self.OnSavePressed(True))
        self.ui.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.OnDiscardPressed)

        self.ui.browseButton.clicked.connect(self.OnBrowseButtonPressed)

        self.ui.credsFilePathEdit.textChanged.connect(self.OnCredsFilePathChanged)
        # use self.onTTSEngineToggled() to refresh TTS engine setting upon start-up
        self.onTTSEngineToggled(self.comboBox)

    def onTTSEngineToggled(self, text):
        # move this on every TTS "if" condition if necessary.
        index = self.ui.comboBox_targetLang.currentIndex()
        self.ui.comboBox_targetLang.clear()
        self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
        self.ui.comboBox_targetLang.setCurrentIndex(index)

        if text == "Azure TTS":
            self.ttsEngine = "azureTTS"
            self.ui.stackedWidget.setCurrentIndex(0)
            if self.screenSize.height() > 800:
                self.resize(588, 667)
        elif text == "Google TTS":
            self.ttsEngine = "gTTS"
            self.ui.stackedWidget.setCurrentIndex(1)
            if self.screenSize.height() > 800:
                self.resize(588, 667)
        elif text == "GSpeak":
            self.resize(588, 400)
            self.ttsEngine = "gspeak"
            self.ui.stackedWidget.setCurrentIndex(2)
        elif text == "Sapi5 (Windows)":
            self.resize(588, 400)
            self.ttsEngine = "sapi5"
            self.ui.stackedWidget.setCurrentIndex(3)
        elif text == "Kurdish TTS":
            self.resize(588, 400)
            self.ttsEngine = "kurdishTTS"
            self.ui.stackedWidget.setCurrentIndex(4)
            self.ui.comboBox_targetLang.clear()
            self.ui.comboBox_targetLang.addItems(["Kurdish (Kurmanji)", "Kurdish (Sorani)"])
        else:
            self.resize(588, 400)
            self.ui.stackedWidget.setCurrentIndex(5)
            if text == "espeak (Unsupported)":
                self.ttsEngine = "espeak"
            elif text == "NSS (Mac Only)":
                self.ttsEngine = "nsss"
            elif text == "coqui_ai_tts (Unsupported)":
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

        self.config.set('translate', 'MyMemoryTranslator_secret_key', self.ui.mymemory_secret_key.text())
        self.config.set('translate', 'email', self.ui.email_mymemory.text())
        self.config.set('translate', 'LibreTranslator_secret_key', self.ui.LibreTranslate_secret_key.text())
        self.config.set('translate', 'url', self.ui.LibreTranslate_url.text())
        self.config.set('translate', 'DeeplTranslator_secret_key', self.ui.deepl_secret_key.text())
        self.config.set('translate', 'deepL_pro', str(self.ui.checkBox_pro.isChecked()).lower())
        self.config.set('translate', 'MicrosoftTranslator_secret_key', self.ui.microsoft_secret_key.text())
        self.config.set('translate', 'region', self.ui.microsoft_region.text())
        # TODO: Add other translators

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
        self.config.set('azureTTS', 'voiceid', self.ui.listWidget_voiceazure.currentItem().toolTip())

        self.config.add_section('googleTTS')
        self.config.set('googleTTS', 'creds_file', self.credsFilePath)
        self.config.set('googleTTS', 'voiceid', self.ui.listWidget_voicegoogle.currentItem().toolTip())

        self.config.add_section('sapi5TTS')
        self.config.set('sapi5TTS', 'voiceid', self.voices_sapi_dict[self.ui.listWidget_sapi.currentItem().text()])

        self.config.add_section('kurdishTTS')
        self.config.set('kurdishTTS', 'latin', str(self.ui.checkBox_latin.isChecked()).lower())
        self.config.set('kurdishTTS', 'punctuation', str(self.ui.checkBox_punctuation.isChecked()).lower())

        self.config.add_section('appCache')
        self.config.set('appCache', 'threshold', str(self.ui.spinBox_threshold.value()))

        start_lang_is_Kurdish = self.startLang == 'ckb' or self.startLang == 'ku'
        end_lang_is_Kurdish = self.endLang == 'ckb' or self.endLang == 'ku'
        prompt1 = False
        prompt2 = False

        if not self.notranslate:
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
            # Code that may raise an exception
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
        if string == 'MyMemoryTranslator':
            try:
                if os.path.exists(self.config_path):
                    self.ui.mymemory_secret_key.setText(self.config.get('translate', 'MyMemoryTranslator_secret_key'))
                    self.ui.email_mymemory.setText(self.config.get('translate', 'email'))
                self.ui.comboBox_writeLang.clear()
                self.ui.comboBox_targetLang.clear()
                self.translate_instance = MyMemoryTranslator(source='af-ZA', target='en-GB')
                self.translate_languages = {k.capitalize(): v for k, v in
                                            self.translate_instance.get_supported_languages(as_dict=True).items()}
                self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
                self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
                self.set_Translate_dropdown(self.translate_languages)
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.mymemory))
        if string == 'LibreTranslator':
            try:
                if os.path.exists(self.config_path):
                    self.ui.LibreTranslate_secret_key.setText(
                        self.config.get('translate', 'LibreTranslator_secret_key'))
                    self.ui.LibreTranslate_url.setText(self.config.get('translate', 'url'))
                self.ui.comboBox_writeLang.clear()
                self.ui.comboBox_targetLang.clear()
                self.translate_instance = LibreTranslator()
                self.translate_languages = self.translate_instance.get_supported_languages(as_dict=True)
                self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
                self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
                self.set_Translate_dropdown(self.translate_languages)
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(
                self.ui.stackedWidget_provider.indexOf(self.ui.libretranslate))
        if string == 'DeeplTranslator':
            try:
                if os.path.exists(self.config_path):
                    self.ui.deepl_secret_key.setText(self.config.get('translate', 'DeeplTranslator_secret_key'))
                    self.ui.checkBox_pro.setChecked(self.config.getboolean('translate', 'deepl_pro'))
                self.ui.comboBox_writeLang.clear()
                self.ui.comboBox_targetLang.clear()
                self.translate_instance = DeeplTranslator(api_key=self.ui.deepl_secret_key.text(),
                                                          use_free_api=not self.ui.checkBox_pro.isChecked())
                self.translate_languages = self.translate_instance.get_supported_languages(as_dict=True)
                self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
                self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
                self.set_Translate_dropdown(self.translate_languages)
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.deepl))
        if string == 'MicrosoftTranslator':
            try:
                if os.path.exists(self.config_path):
                    self.ui.microsoft_secret_key.setText(self.config.get('translate', 'MicrosoftTranslator_secret_key'))
                    self.ui.microsoft_region.setText(self.config.get('translate', 'region'))
                self.ui.comboBox_writeLang.clear()
                self.ui.comboBox_targetLang.clear()
                self.translate_languages = self.language_azure_list
                self.ui.comboBox_writeLang.addItems(sorted(self.language_azure_list.keys()))
                self.ui.comboBox_targetLang.addItems(sorted(self.language_azure_list.keys()))
                self.set_Translate_dropdown(self.language_azure_list)
            except Exception as e:
                logging.error("Configuration Error: {}".format(e), exc_info=True)
            self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.microsoft))
        # TODO: Add other translators

    def updateLanguage(self, text):
        if self.ui.comboBox_provider.currentText() == "DeeplTranslator":
            self.ui.comboBox_writeLang.clear()
            self.ui.comboBox_targetLang.clear()
            self.translate_instance = DeeplTranslator(api_key=self.ui.deepl_secret_key.text(),
                                                      use_free_api=not self.ui.checkBox_pro.isChecked())
            self.translate_languages = self.translate_instance.get_supported_languages(as_dict=True)
            self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
            self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
            self.set_Translate_dropdown(self.translate_languages)
        # TODO: Add other translators

    def set_azure_voice(self, text):
        for index in range(self.ui.listWidget_voiceazure.count()):
            item = self.ui.listWidget_voiceazure.item(index)
            if text == item.toolTip():
                self.azure_row = self.ui.listWidget_voiceazure.row(item)
                self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                break

    def preview_pressed(self):
        self.currentButton = self.sender()
        text = self.sender().parent().parent().parent().objectName()
        if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
            for index in range(self.ui.listWidget_voiceazure.count()):
                item = self.ui.listWidget_voiceazure.item(index)
                if text == item.toolTip():
                    self.azure_row = self.ui.listWidget_voiceazure.row(item)
                    self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                    break
            if self.ui.lineEdit_key.text() == '':
                self.ui.lineEdit_key.setFocus()
                return
            if self.ui.lineEdit_region.text() == '':
                self.ui.lineEdit_region.setFocus()
                return
        elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
            for index in range(self.ui.listWidget_voicegoogle.count()):
                item = self.ui.listWidget_voicegoogle.item(index)
                if text == item.toolTip():
                    self.google_row = self.ui.listWidget_voicegoogle.row(item)
                    self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                    break
            if self.ui.credsFilePathEdit.text() == '':
                self.ui.credsFilePathEdit.setFocus()
                return

        self.OnSavePressed(False)
        # TODO: Change value to the desired text
        pyperclip.copy("Hello World")
        pool = QThreadPool.globalInstance()
        runnable = Player(self.temp_config_file)
        runnable.signals.completed.connect(self.enablePlayButtons)
        buttons = self.ui.listWidget_voiceazure.findChildren(QPushButton)
        self.movie = QMovie(":/images/images/loading.gif")
        self.movie.updated.connect(self.update_Buttons)
        self.movie.start()
        self.ui.ttsEngineBox.setEnabled(False)
        for button in buttons:
            button.setEnabled(False)
        pool.start(runnable)

    def update_Buttons(self):
        loading_icon = QIcon(self.movie.currentPixmap())
        self.currentButton.setIcon(loading_icon)

    def enablePlayButtons(self):
        if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
            buttons = self.ui.listWidget_voiceazure.findChildren(QPushButton)
        elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
            buttons = self.ui.listWidget_voiceazure.findChildren(QPushButton)

        self.ui.ttsEngineBox.setEnabled(True)
        for button in buttons:
            button.setEnabled(True)
        self.movie.stop()
        icon = QIcon()
        icon.addFile(":/images/images/play-round-icon.png")
        self.currentButton.setIcon(icon)
        self.temp_config_file.close()
        os.unlink(self.temp_config_file.name)

    def print_data(self, item):
        try:
            if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
                self.ui.listWidget_voiceazure.setCurrentItem(item)
            elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
                self.ui.listWidget_voicegoogle.setCurrentItem(item)
        except Exception as error:
            pass

    def updateRow(self, row):
        try:
            # Set the row when index become zero (no selected item)
            if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
                if self.ui.listWidget_voiceazure.currentRow() == 0:
                    self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                    self.ui.listWidget_voiceazure.setCurrentItem(self.ui.listWidget_voiceazure.item(self.azure_row))
            elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
                if self.ui.listWidget_voicegoogle.currentRow() == 0:
                    self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                    self.ui.listWidget_voicegoogle.setCurrentItem(self.ui.listWidget_voicegoogle.item(self.google_row))
        except Exception as error:
            pass

    def generate_azure_voice_models(self):
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
            response = requests.get(url=endpoint, headers={"Ocp-Apim-Subscription-Key": key}, timeout=5)
            self.voice_list = response.json()
            # print("Azure voice list fetched from API.")
            logging.info("Azure voice list fetched from API.")
        except Exception as error:
            file = PySide6.QtCore.QFile(":/binary/azure_voices.json")
            if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
                text = PySide6.QtCore.QTextStream(file).readAll()
                self.voice_list = json.loads(text.encode())
                print("Azure voice list fetched from Resource file.")
                logging.info("Azure voice list fetched from Resource file.")
                file.close()
        return self.voice_list

    def get_google_voices(self):
        try:
            key = self.config.get('googleTTS', 'creds_file')
            self.google_client = texttospeech.TextToSpeechClient(
                credentials=service_account.Credentials.from_service_account_file(key))
            google_list = self.google_client.list_voices()
            self.voice_google_list = []
            for voice in google_list.voices:
                voice_dict = {}
                voice_dict['name'] = voice.name
                for language_code in voice.language_codes:
                    voice_dict['country'] = Language.get(language_code).display_name()
                    codes = []
                    codes.append(language_code)
                voice_dict['languageCodes'] = codes
                ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)
                voice_dict['ssmlGender'] = ssml_gender.name.capitalize()
                voice_dict['naturalSampleRateHertz'] = voice.natural_sample_rate_hertz
                self.voice_google_list.append(voice_dict)
            unique = []
            for data in self.voice_google_list:
                if data not in unique:
                    unique.append(data)
            self.voice_google_list = sorted(unique, key=lambda d: d['country'])
            with open('google_voices.json', 'w') as json_file:
                json.dump(self.voice_google_list, json_file)
            # print("Google voice list fetched from API.")
            logging.info("Google voice list fetched from API.")
        except Exception as error:
            file = PySide6.QtCore.QFile(":/binary/google_voices.json")
            if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
                text = PySide6.QtCore.QTextStream(file).readAll()
                self.voice_google_list = json.loads(text.encode())
                print("Google voice list fetched from Resource file.")
                logging.info("Google voice list fetched from Resource file.")
                file.close()
        return self.voice_google_list

    def generate_google_voice_models(self):
        self.ui.listWidget_voicegoogle.currentRowChanged.connect(self.updateRow)
        self.ui.listWidget_voicegoogle.itemClicked.connect(self.print_data)
        voices = self.get_google_voices()
        voices.reverse()
        for index, voice in enumerate(voices):
            voice_country = voice['country']
            try:
                if voice_country == voices[index + 1]['country']:
                    item_widget = QWidget()
                    item_UI = Ui_item()
                    item_UI.setupUi(item_widget)
                    item_UI.data.setText(str(voice))
                    item_UI.name.setText(voice['name'])
                    font = QFont()
                    font.setBold(False)
                    font.setPointSize(8)
                    item_UI.gender.setFont(font)
                    item_UI.gender.setText(voice['ssmlGender'])
                    item_UI.play.clicked.connect(self.preview_pressed)
                    item_widget.setObjectName(voice['name'])

                    item = QListWidgetItem()
                    item.setToolTip(voice['name'])
                    item.setSizeHint(item_widget.sizeHint())
                    self.ui.listWidget_voicegoogle.insertItem(index, item)
                    self.ui.listWidget_voicegoogle.setItemWidget(item, item_widget)
                else:
                    item_widget = QWidget()
                    item_UI = Ui_item()
                    item_UI.setupUi(item_widget)
                    item_UI.data.setText(str(voice))
                    item_UI.name.setText(voice['name'])
                    font = QFont()
                    font.setBold(False)
                    font.setPointSize(8)
                    item_UI.gender.setFont(font)
                    item_UI.gender.setText(voice['ssmlGender'])
                    item_UI.play.clicked.connect(self.preview_pressed)
                    item_widget.setObjectName(voice['name'])

                    item = QListWidgetItem()
                    item.setToolTip(voice['name'])
                    item.setSizeHint(item_widget.sizeHint())
                    self.ui.listWidget_voicegoogle.insertItem(index, item)
                    self.ui.listWidget_voicegoogle.setItemWidget(item, item_widget)

                    label_widget = QLabel(voice_country)
                    label_widget.setObjectName(voice_country)
                    label_widget.setAlignment(Qt.AlignCenter)
                    item = QListWidgetItem()
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                    self.ui.listWidget_voicegoogle.addItem(item)
                    self.ui.listWidget_voicegoogle.setItemWidget(item, label_widget)
            except Exception as error:
                item_widget = QWidget()
                item_UI = Ui_item()
                item_UI.setupUi(item_widget)
                item_UI.data.setText(str(voice))
                item_UI.name.setText(voice['name'])
                font = QFont()
                font.setBold(False)
                font.setPointSize(8)
                item_UI.gender.setFont(font)
                item_UI.gender.setText(voice['ssmlGender'])
                item_UI.play.clicked.connect(self.preview_pressed)
                item_widget.setObjectName(voice['name'])

                item = QListWidgetItem()
                item.setToolTip(voice['name'])
                item.setSizeHint(item_widget.sizeHint())
                self.ui.listWidget_voicegoogle.insertItem(index, item)
                self.ui.listWidget_voicegoogle.setItemWidget(item, item_widget)

                label_widget = QLabel(voice_country)
                label_widget.setObjectName(voice_country)
                label_widget.setAlignment(Qt.AlignCenter)
                item = QListWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                self.ui.listWidget_voicegoogle.addItem(item)
                self.ui.listWidget_voicegoogle.setItemWidget(item, label_widget)

    def set_google_voice(self, text):
        for index in range(self.ui.listWidget_voicegoogle.count()):
            item = self.ui.listWidget_voicegoogle.item(index)
            if text == item.toolTip():
                self.google_row = self.ui.listWidget_voicegoogle.row(item)
                self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                break

    def cache_open(self):
        os.startfile(self.audio_path)

    def cache_clear(self):
        pool = QThreadPool.globalInstance()
        runnable = Cleaner(self.audio_path)
        runnable.signals.completed.connect(self.enableClearCache)
        self.ui.clear_cache.setEnabled(False)
        pool.start(runnable)

    def enableClearCache(self):
        self.ui.clear_cache.setEnabled(True)

    def get_microsoft_language(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebit/535.19'
                                     '(KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
            headers.update({"Content-type": "application/json"})
            base_url = 'https://api.cognitive.microsofttranslator.com/languages'
            params = {'api-version': '3.0', 'scope': 'translation'}
            session = requests.Session()
            response = session.get(base_url, params=params, headers=headers, timeout=5)
            language_azure_list = json.loads(response.text)['translation']
            # file = json.dumps(language_azure_list)
            # with open("azure_translation.json", "w") as outfile:
            #     outfile.write(file)
            print("Azure Translation list fetched from API.")
            logging.info("Azure Translation list fetched from API file.")
        except Exception as error:
            print(error)
            file = PySide6.QtCore.QFile(":/binary/azure_translation.json")
            if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
                text = PySide6.QtCore.QTextStream(file).readAll()
                language_azure_list = json.loads(text.encode())
                print("Azure Translation list fetched from Resource file.")
                logging.info("Azure Translation list fetched from Resource file.")
                file.close()
        self.language_azure_list = {}
        for value in language_azure_list:
            self.language_azure_list[language_azure_list[value]['name']] = value
        # print(self.language_azure_list)
        return self.language_azure_list

    def generate_translate_list(self):
        # TODO : Add Kurdish later "Kurdish (Kurmanji)": "ku", "Kurdish (Sorani)": "ckb"
        gtts_list = {v: k for k, v in gtts_language_list.tts_langs().items()}
        # print(str(gtts_list))
        # file = json.dumps(gtts_list)
        # with open("gspeak_voices.json", "w") as outfile:
        #     outfile.write(file)

    def set_Translate_dropdown(self, source):
        try:
            lang = [key for key, value in source.items() if value == self.startLang]
            if not len(lang) == 0:
                lang = lang[0]
            self.ui.comboBox_writeLang.setCurrentText(lang)

            lang = [key for key, value in source.items() if value == self.endLang]
            if not len(lang) == 0:
                lang = lang[0]
            self.ui.comboBox_targetLang.setCurrentText(lang)
        except Exception as error:
            logging.error("Error setting current text.", exc_info=False)

    def copyAppPath(self):
        pyperclip.copy(self.ui.appPath.text())


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
            process = subprocess.Popen([GUI_path, "--config", self.temp_config_file.name, "--preview"])
            process.wait()
        elif __file__:
            application_path = os.path.dirname(os.path.dirname(__file__))
            # TODO: GUI_script_path get the upper directory where translatepb.py is located
            GUI_script_path = os.path.join(application_path, 'translatepb.py')
            process = subprocess.Popen(["python", GUI_script_path, "--config", self.temp_config_file.name, "--preview"])
            process.wait()
        self.signals.completed.emit()


class Cleaner(QRunnable):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.signals = Signals()

    def run(self):
        try:
            files = os.listdir(self.path)
            for file in files:
                file_path = os.path.join(self.path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'{file_path} is deleted.')
            print("All files deleted successfully.")
        except OSError:
            logging.error("Error occurred while deleting files.", exc_info=True)
        self.signals.completed.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    # print('Size: %d x %d' % (size.width(), size.height()))
    widget = Widget(size)
    widget.show()
    sys.exit(app.exec())
