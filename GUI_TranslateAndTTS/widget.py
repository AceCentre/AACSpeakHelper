# This Python file uses the following encoding: utf-8
import configparser
import json
import logging
import os
import subprocess
import tempfile
import sys
import time
import uuid
import warnings
warnings.filterwarnings('ignore')
import PySide6.QtCore
import pyperclip
import pyttsx3
from PySide6.QtCore import Qt, QObject, Signal, QRunnable, QThreadPool, QCoreApplication
from PySide6.QtGui import QFont, QIcon, QMovie, QColor
from PySide6.QtWidgets import *
from deep_translator import __all__ as providers
from tts_wrapper import MicrosoftClient, GoogleClient, SherpaOnnxClient


from item import Ui_item
from language_dictionary import *
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget
from dotenv import load_dotenv

if os.path.isfile('../.env'):
    load_dotenv(dotenv_path='../.env')

ms_token = os.getenv('MICROSOFT_TOKEN')
ms_region = os.getenv('MICROSOFT_REGION')
google_cred_path = os.getenv('GOOGLE_CREDS_JSON')
ms_token_trans = os.getenv('MICROSOFT_TOKEN_TRANS')


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
        self.lock = True
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.onnx_progressBar.setVisible(False)
        self.ui.onnx_listWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical { width: 30px; }")
        self.ui.listWidget_voiceazure.verticalScrollBar().setStyleSheet("QScrollBar:vertical { width: 30px; }")
        self.ui.listWidget_voicegoogle.verticalScrollBar().setStyleSheet("QScrollBar:vertical { width: 30px; }")
        self.ui.textBrowser.setStyleSheet("background-color: transparent; border: none;")
        self.ui.copyApp.clicked.connect(self.copyAppPath)
        self.providers = []
        for translator in providers:
            if "Translator" in translator:
                self.providers.append(translator)
        self.ui.comboBox_provider.addItems(self.providers)
        self.ui.comboBox_provider.currentTextChanged.connect(self.setParameter)
        self.ui.tabWidget.setTabText(0, "TTS Engine")
        self.ui.tabWidget.setTabText(1, "Translate Settings")
        self.ui.tabWidget.setTabText(2, "Application Settings")
        self.tts_dict = {}
        # self.generate_translate_list()
        self.ui.comboBox_targetLang.currentTextChanged.connect(self.updateLanguage)
        self.translate_languages = gSpeak_TTS_list

        self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
        self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))

        voices_sapi = pyttsx3.init('sapi5').getProperty('voices')
        self.voices_sapi_dict = {}
        for voice in voices_sapi:
            import re
            # Define regular expressions to extract voice ID and name
            voice_id_pattern = r"id=(.*?)\n"
            name_pattern = r"name=(.*?)\n"
            # print(str(os.path.basename(voice.id)))
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
            self.app_data_path = os.path.join(home_directory,
                                              'AppData', 'Local', 'Programs', 'Ace Centre', 'AACSpeakHelper')
            self.ui.appPath.setText(self.app_data_path)
            self.config_path = os.path.join(home_directory, 'AppData', 'Roaming', 'Ace Centre',
                                            'AACSpeakHelper', 'settings.cfg')
            self.audio_path = os.path.join(home_directory, 'AppData', 'Roaming', 'Ace Centre',
                                           'AACSpeakHelper', 'Audio Files')
            self.onnx_cache_path = os.path.join(home_directory, 'AppData', 'Roaming', 'Ace Centre',
                                                'AACSpeakHelper', 'models')
        elif __file__:
            self.app_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
            self.ui.appPath.setText(os.path.join(self.app_data_path, "AACSpeakHelperServer.py"))
            self.config_path = os.path.join(self.app_data_path, 'settings.cfg')
            self.audio_path = os.path.join(self.app_data_path, 'Audio Files')
            self.onnx_cache_path = os.path.join(self.app_data_path, 'models')
        if not os.path.isdir(self.onnx_cache_path):
            os.makedirs(self.onnx_cache_path)
        self.ui.clear_cache.clicked.connect(self.cache_clear)
        self.ui.open_cache.clicked.connect(self.cache_open)
        self.ui.cache_pushButton.clicked.connect(self.open_onnx_cache)
        self.config = configparser.ConfigParser()
        self.setWindowTitle("Configure TranslateAndTTS: {}".format(self.config_path))
        # Check if the file already exists
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
            self.generate_azure_voice_models()
            self.generate_google_voice_models()
            self.generate_onnx_voice_model()
            self.get_microsoft_language()
            self.notranslate = self.ttsEngine = self.config.getboolean('translate', 'noTranslate')
            self.startLang = self.config.get('translate', 'startLang')
            self.endLang = self.config.get('translate', 'endLang')
            self.overwritePb = self.config.getboolean('translate', 'replacepb')
            self.bypassTTS = self.config.getboolean('TTS', 'bypass_tts')
            self.provider = self.config.get('translate', 'provider')
            self.ui.comboBox_provider.setCurrentIndex(self.ui.comboBox_provider.findText(self.provider))
            match self.provider:
                case 'MyMemoryTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.mymemory))
                case 'LibreTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.libretranslate))
                case 'DeeplTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.deepl))
                case 'MicrosoftTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.microsoft))
                case 'YandexTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.yandex))
                case 'GoogleTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.google))
                case 'LingueeTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.linguee))
                case 'PonsTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.pons))
                case 'QCRITranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.qcri))
                case 'PapagoTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.papago))
                case 'BaiduTranslator':
                    self.ui.stackedWidget_provider.setCurrentIndex(
                        self.ui.stackedWidget_provider.indexOf(self.ui.baidu))
            self.ui.mymemory_secret_key.setText(self.config.get('translate', 'MyMemoryTranslator_secret_key'))
            self.ui.email_mymemory.setText(self.config.get('translate', 'email'))
            self.ui.LibreTranslate_secret_key.setText(self.config.get('translate', 'LibreTranslator_secret_key'))
            self.ui.LibreTranslate_url.setText(self.config.get('translate', 'url'))
            self.ui.deepl_secret_key.setText(self.config.get('translate', 'DeeplTranslator_secret_key'))
            self.ui.checkBox_pro.setChecked(self.config.getboolean('translate', 'deepl_pro'))
            self.ui.microsoft_secret_key.setText(self.config.get('translate', 'MicrosoftTranslator_secret_key'))
            self.ui.microsoft_region.setText(self.config.get('translate', 'region'))
            self.ui.yandex_secret_key.setText(self.config.get('translate', 'YandexTranslator_secret_key'))
            self.ui.qcri_secret_key.setText(self.config.get('translate', 'QCRITranslator_secret_key'))
            self.ui.papago_secret_key.setText(self.config.get('translate', 'PapagoTranslator_secret_key'))
            self.ui.papago_client_id.setText(self.config.get('translate', 'papagotranslator_client_id'))
            self.ui.baidu_secret_key.setText(self.config.get('translate', 'BaiduTranslator_secret_key'))
            self.ui.baidu_appid.setText(self.config.get('translate', 'baidutranslator_appid'))
            # TODO: Add ChatGPT translator
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
            self.voiceid_onnx = self.config.get('SherpaOnnxTTS', 'voiceid')
            match self.ttsEngine:
                case "azureTTS":
                    self.comboBox = 'Azure TTS'
                    self.ui.stackedWidget.setCurrentIndex(0)
                    self.ui.ttsEngineBox.setCurrentText('Azure TTS')
                case "googleTTS":
                    self.comboBox = 'Google TTS'
                    self.ui.stackedWidget.setCurrentIndex(1)
                    self.ui.ttsEngineBox.setCurrentText('Google TTS')
                case "gspeak":
                    self.comboBox = 'GSpeak'
                    self.ui.stackedWidget.setCurrentIndex(2)
                    self.ui.ttsEngineBox.setCurrentText('GSpeak')
                case "sapi5":
                    self.comboBox = 'Sapi5 (Windows)'
                    self.ui.stackedWidget.setCurrentIndex(3)
                    self.ui.ttsEngineBox.setCurrentText('Sapi5 (Windows)')
                case "SherpaOnnxTTS":
                    self.comboBox = 'Sherpa-ONNX'
                    self.ui.stackedWidget.setCurrentIndex(6)
                    self.ui.ttsEngineBox.setCurrentText('Sherpa-ONNX')
                case "espeak":
                    self.comboBox = 'espeak (Unsupported)'
                    self.ui.stackedWidget.setCurrentIndex(5)
                    self.ui.ttsEngineBox.setCurrentText('espeak (Unsupported)')
                case "nsss":
                    self.comboBox = 'NSS (Mac Only)'
                    self.ui.stackedWidget.setCurrentIndex(5)
                    self.ui.ttsEngineBox.setCurrentText('NSS (Mac Only)')
                case "coqui":
                    self.comboBox = 'coqui_ai_tts (Unsupported)'
                    self.ui.stackedWidget.setCurrentIndex(5)
                    self.ui.ttsEngineBox.setCurrentText('coqui_ai_tts (Unsupported)')
                case _:
                    self.comboBox = 'GSpeak'
                    self.ui.stackedWidget.setCurrentIndex(2)
                    self.ui.ttsEngineBox.setCurrentText('GSpeak')
            self.set_Translate_dropdown(self.translate_languages)

            self.set_azure_voice(self.voiceidAzure)
            self.set_google_voice(self.voiceidGoogle)
            self.set_onnx_voice(self.voiceid_onnx)

            item = [key for key, value in self.voices_sapi_dict.items() if value == self.voiceid_sapi]

            if len(item) > 0:
                item = self.ui.listWidget_sapi.findItems(item[0], PySide6.QtCore.Qt.MatchExactly)
                self.ui.listWidget_sapi.setCurrentItem(item[0])
            elif self.ui.listWidget_sapi.count() > 0:
                self.ui.listWidget_sapi.setCurrentRow(0)
                self.ui.listWidget_sapi.setCurrentItem(self.ui.listWidget_sapi.item(0))

            self.ui.checkBox_translate.setChecked(not self.notranslate)
            self.ui.checkBox_overwritepb.setChecked(self.overwritePb)
            self.ui.bypass_tts_checkBox.setChecked(self.bypassTTS)
            self.ui.checkBox_saveAudio.setChecked(self.saveAudio)

            self.ui.horizontalSlider_rate.setValue(self.rate)
            self.ui.horizontalSlider_volume.setValue(self.volume)
            self.ui.horizontalSlider_rate_sapi.setValue(self.rate)
            self.ui.horizontalSlider_volume_sapi.setValue(self.volume)
            self.ui.onnx_cache.setText(self.onnx_cache_path)
            self.ui.lineEdit_voiceID.setText(self.voiceid)
            self.ui.lineEdit_key.setText(self.key)
            self.ui.lineEdit_region.setText(self.region)

            self.ui.checkBox_saveAudio_gTTS.setChecked(self.saveAudio)
            self.ui.credsFilePathEdit.setText(self.credsFilePath)

            self.ui.checkBox_saveAudio_sapi.setChecked(self.saveAudio)
            self.ui.onnx_checkBox.setChecked(self.saveAudio)

            # self.ui.checkBox_latin.setChecked(self.config.getboolean('kurdishTTS', 'latin'))
            # self.ui.checkBox_punctuation.setChecked(self.config.getboolean('kurdishTTS', 'punctuation'))

            self.ui.checkBox_stats.setChecked(self.config.getboolean('App', 'collectstats'))
            self.ui.spinBox_threshold.setValue(int(self.config.get('appCache', 'threshold')))

        else:
            self.generate_azure_voice_models()
            self.generate_google_voice_models()
            self.generate_onnx_voice_model()
            self.get_microsoft_language()
            # self.ttsEngine = "azureTTS"
            # self.comboBox = 'Azure TTS'
            self.ui.onnx_cache.setText(self.onnx_cache_path)
            self.ttsEngine = "SherpaOnnxTTS"
            self.comboBox = 'Sherpa-ONNX'
            self.ui.stackedWidget.setCurrentIndex(0)

            self.notranslate = False
            self.saveAudio_azure = True
            self.overwritePb = True
            self.bypassTTS = False

            self.voiceid = None
            self.voiceidAzure = "en-US-JennyNeural"
            self.voiceidGoogle = "en-US-Wavenet-C"
            self.voiceidonnx = "eng"

            self.rate = None
            self.volume = None

            self.key = None
            self.region = None
            self.startLang = None
            self.endLang = None

            self.credsFilePath = ""
            self.saveAudio_google = True

            self.saveAudio_sapi5 = True
            self.saveAudio_onnx = True

            # self.set_azure_voice(self.voiceidAzure)
            # self.set_google_voice(self.voiceidGoogle)
            # self.set_onnx_voice(self.voiceidonnx)

            self.ui.spinBox_threshold.setValue(7)

        self.ui.ttsEngineBox.currentTextChanged.connect(self.onTTSEngineToggled)

        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(lambda: self.OnSavePressed(True))
        self.ui.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.OnDiscardPressed)

        self.ui.browseButton.clicked.connect(self.OnBrowseButtonPressed)

        self.ui.credsFilePathEdit.textChanged.connect(self.OnCredsFilePathChanged)
        self.onTTSEngineToggled(self.comboBox)
        self.lock = False

    def onTTSEngineToggled(self, text):
        match text:
            case "Azure TTS":
                self.ttsEngine = "azureTTS"
                self.ui.stackedWidget.setCurrentIndex(0)
                if self.screenSize.height() > 800:
                    self.resize(588, 667)
            case "Google TTS":
                self.ttsEngine = "googleTTS"
                self.ui.stackedWidget.setCurrentIndex(1)
                if self.screenSize.height() > 800:
                    self.resize(588, 667)
            case "GSpeak":
                self.resize(588, 400)
                self.ttsEngine = "gspeak"
                self.ui.stackedWidget.setCurrentIndex(2)
            case "Sapi5 (Windows)":
                self.resize(588, 400)
                self.ttsEngine = "sapi5"
                self.ui.stackedWidget.setCurrentIndex(3)
            case "Sherpa-ONNX":
                # self.resize(588, 400)
                self.ttsEngine = "SherpaOnnxTTS"
                self.ui.stackedWidget.setCurrentIndex(6)
                if self.screenSize.height() > 800:
                    self.resize(588, 667)
            case _:
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
        self.setParameter(self.ui.comboBox_provider.currentText())

    def OnSavePressed(self, permanent=True):
        self.ui.statusBar.clear()
        if self.ui.listWidget_voiceazure.currentItem() is None or self.ui.listWidget_voiceazure.currentItem().toolTip() == '' and self.ui.stackedWidget.currentIndex() == 0:
            self.ui.statusBar.setText("Failed to save settings. Please select voice model.")
            return
        if self.ui.listWidget_voicegoogle.currentItem() is None or self.ui.listWidget_voicegoogle.currentItem().toolTip() == '' and self.ui.stackedWidget.currentIndex() == 1:
            self.ui.statusBar.setText("Failed to save settings. Please select voice model.")
            return
        if self.ui.onnx_listWidget.currentItem() is None or self.ui.onnx_listWidget.currentItem().toolTip() == '' and self.ui.stackedWidget.currentIndex() == 6:
            self.ui.statusBar.setText("Failed to save settings. Please select voice model.")
            return
        # TODO: Block saving if API-key is blank
        # Add sections and key-value pairs
        self.startLang = self.translate_languages[self.ui.comboBox_writeLang.currentText()]
        self.endLang = self.translate_languages[self.ui.comboBox_targetLang.currentText()]
        self.notranslate = not self.ui.checkBox_translate.isChecked()

        identifier = self.get_uuid()
        # TODO: check this function later
        # self.config.clear()

        self.config.add_section('App') if not self.config.has_section('App') else print('')
        self.config.set('App', 'uuid', str(identifier))
        self.config.set('App', 'collectstats', str(self.ui.checkBox_stats.isChecked()))

        self.config.add_section('translate') if not self.config.has_section('translate') else print('')
        self.config.set('translate', 'noTranslate', str(self.notranslate))
        self.config.set('translate', 'startLang', self.startLang)
        self.config.set('translate', 'endLang', self.endLang)
        self.config.set('translate', 'replacepb', str(self.ui.checkBox_overwritepb.isChecked()))
        self.config.set('translate', 'provider', str(self.ui.comboBox_provider.currentText()))

        self.config.set('translate', 'mymemorytranslator_secret_key', self.ui.mymemory_secret_key.text())
        self.config.set('translate', 'email', self.ui.email_mymemory.text())
        self.config.set('translate', 'libretranslator_secret_key', self.ui.LibreTranslate_secret_key.text())
        self.config.set('translate', 'url', self.ui.LibreTranslate_url.text())
        self.config.set('translate', 'deepltranslator_secret_key', self.ui.deepl_secret_key.text())
        self.config.set('translate', 'deepL_pro', str(self.ui.checkBox_pro.isChecked()).lower())
        self.config.set('translate', 'microsofttranslator_secret_key', self.ui.microsoft_secret_key.text())
        self.config.set('translate', 'region', self.ui.microsoft_region.text())
        self.config.set('translate', 'yandextranslator_secret_key', self.ui.yandex_secret_key.text())
        self.config.set('translate', 'papagotranslator_client_id', self.ui.papago_client_id.text())
        self.config.set('translate', 'papagotranslator_secret_key', self.ui.papago_secret_key.text())
        self.config.set('translate', 'baidutranslator_appid', self.ui.baidu_appid.text())
        self.config.set('translate', 'baidutranslator_secret_key', self.ui.baidu_secret_key.text())
        self.config.set('translate', 'qcritranslator_secret_key', self.ui.qcri_secret_key.text())

        self.config.add_section('TTS') if not self.config.has_section('TTS') else print('')
        self.config.set('TTS', 'engine', self.ttsEngine)
        if self.ttsEngine == 'azureTTS':
            if permanent:
                self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio.isChecked()))
            else:
                self.config.set('TTS', 'save_audio_file', str(False))
        elif self.ttsEngine == 'googleTTS':
            if permanent:
                self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio_gTTS.isChecked()))
            else:
                self.config.set('TTS', 'save_audio_file', str(False))
        elif self.ttsEngine == 'sapi5':
            self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio_sapi.isChecked()))
        elif self.ttsEngine == 'SherpaOnnxTTS':
            if permanent:
                self.config.set('TTS', 'save_audio_file', str(self.ui.onnx_checkBox.isChecked()))
            else:
                self.config.set('TTS', 'save_audio_file', str(False))
        else:
            self.config.set('TTS', 'save_audio_file', str(False))

        self.config.set('TTS', 'voiceid', self.ui.lineEdit_voiceID.text())
        if self.ttsEngine == 'sapi5':
            self.config.set('TTS', 'rate', str(self.ui.horizontalSlider_rate_sapi.value()))
            self.config.set('TTS', 'volume', str(self.ui.horizontalSlider_volume_sapi.value()))
        else:
            self.config.set('TTS', 'rate', str(self.ui.horizontalSlider_rate.value()))
            self.config.set('TTS', 'volume', str(self.ui.horizontalSlider_volume.value()))
        self.config.set('TTS', 'bypass_tts', str(self.ui.bypass_tts_checkBox.isChecked()))

        self.config.add_section('azureTTS') if not self.config.has_section('azureTTS') else print('')
        if self.ui.lineEdit_key.text() == '' and not permanent:
            self.config.set('azureTTS', 'key', ms_token)
        else:
            self.config.set('azureTTS', 'key', self.ui.lineEdit_key.text())
        if self.ui.lineEdit_region.text() == '' and not permanent:
            self.config.set('azureTTS', 'location', ms_region)
        else:
            self.config.set('azureTTS', 'location', self.ui.lineEdit_region.text())
        if self.ui.listWidget_voiceazure.currentItem() is None:
            self.config.set('azureTTS', 'voiceid', "en-US-JennyNeural")
        else:
            self.config.set('azureTTS', 'voiceid', self.ui.listWidget_voiceazure.currentItem().toolTip())

        self.config.add_section('googleTTS') if not self.config.has_section('googleTTS') else print('')
        if self.credsFilePath == '' and not permanent:
            self.config.set('googleTTS', 'creds_file', google_cred_path)
        else:
            self.config.set('googleTTS', 'creds_file', self.credsFilePath)
        if self.ui.listWidget_voicegoogle.currentItem() is None:
            self.config.set('googleTTS', 'voiceid', "en-US-Wavenet-C")
        else:
            self.config.set('googleTTS', 'voiceid', self.ui.listWidget_voicegoogle.currentItem().toolTip())

        self.config.add_section('sapi5TTS') if not self.config.has_section('sapi5TTS') else print('')
        self.config.set('sapi5TTS', 'voiceid', self.voices_sapi_dict[self.ui.listWidget_sapi.currentItem().text()])

        self.config.add_section('SherpaOnnxTTS') if not self.config.has_section('SherpaOnnxTTS') else print('')
        if self.ui.onnx_listWidget.currentItem() is None:
            self.config.set('SherpaOnnxTTS', 'voiceid', 'eng')
        else:
            self.config.set('SherpaOnnxTTS', 'voiceid', self.ui.onnx_listWidget.currentItem().toolTip())

        self.config.add_section('appCache') if not self.config.has_section('appCache') else print('')
        self.config.set('appCache', 'threshold', str(self.ui.spinBox_threshold.value()))

        # Write the configuration to a file
        if permanent:
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
                logging.info("Configuration file is saved on {}".format(self.config_path))
                self.ui.statusBar.setText("Saving settings is successful.")
            # self.close()
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
            else:
                identifier = uuid.uuid4()
        except Exception as e:
            # Code to handle other exceptions
            identifier = uuid.uuid4()
            logging.error("UUID Error: {}. Generating UUID is successful.".format(e), exc_info=False)
        return identifier

    def setParameter(self, string):
        self.ui.comboBox_writeLang.clear()
        self.ui.comboBox_targetLang.clear()
        match string:
            case 'GoogleTranslator':
                try:
                    self.translate_languages = Google_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.google))
            case 'MyMemoryTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.mymemory_secret_key.setText(
                            self.config.get('translate', 'MyMemoryTranslator_secret_key'))
                        self.ui.email_mymemory.setText(self.config.get('translate', 'email'))
                    self.translate_languages = MyMemory_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.mymemory))
            case 'LibreTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.LibreTranslate_secret_key.setText(
                            self.config.get('translate', 'LibreTranslator_secret_key'))
                        self.ui.LibreTranslate_url.setText(self.config.get('translate', 'url'))
                    self.translate_languages = Libre_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.libretranslate))
            case 'DeeplTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.deepl_secret_key.setText(self.config.get('translate', 'DeeplTranslator_secret_key'))
                        self.ui.checkBox_pro.setChecked(self.config.getboolean('translate', 'deepl_pro'))
                    self.translate_languages = DeepL_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.deepl))
            case 'MicrosoftTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.microsoft_secret_key.setText(
                            self.config.get('translate', 'MicrosoftTranslator_secret_key'))
                        self.ui.microsoft_region.setText(self.config.get('translate', 'region'))
                    self.translate_languages = Microsoft_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(
                    self.ui.stackedWidget_provider.indexOf(self.ui.microsoft))
            case 'PonsTranslator':
                try:
                    self.translate_languages = Pons_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.pons))
            case 'LingueeTranslator':
                try:
                    self.translate_languages = Linguee_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.linguee))
            case 'PapagoTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.papago_secret_key.setText(self.config.get('translate', 'PapagoTranslator_secret_key'))
                        self.ui.papago_client_id.setText(self.config.get('translate', 'Papagotranslator_client_id'))
                    self.translate_languages = Papago_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.papago))
            case 'QcriTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.qcri_secret_key.setText(self.config.get('translate', 'QCRITranslator_secret_key'))
                    self.translate_languages = Qcri_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.qcri))
            case 'BaiduTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.baidu_secret_key.setText(self.config.get('translate', 'BaiduTranslator_secret_key'))
                        self.ui.baidu_appid.setText(self.config.get('translate', 'BaiduTranslator_appid'))
                    self.translate_languages = Baidu_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.baidu))
            case 'YandexTranslator':
                try:
                    if os.path.exists(self.config_path):
                        self.ui.yandex_secret_key.setText(self.config.get('translate', 'YandexTranslator_secret_key'))
                    self.translate_languages = Yandex_Translator
                except Exception as e:
                    logging.error("Configuration Error: {}".format(e), exc_info=True)
                self.ui.stackedWidget_provider.setCurrentIndex(self.ui.stackedWidget_provider.indexOf(self.ui.yandex))
        self.ui.comboBox_writeLang.addItems(sorted(self.translate_languages.keys()))
        self.ui.comboBox_targetLang.addItems(sorted(self.translate_languages.keys()))
        self.set_Translate_dropdown(self.translate_languages)

    def updateLanguage(self, language_input):
        self.ui.statusBar.setText("")
        if self.lock:
            return
        match self.ui.ttsEngineBox.currentText():
            case 'Azure TTS':
                for text in list(azure_tts_list.keys()):
                    if self.ui.comboBox_targetLang.currentText() in text:
                        self.ui.statusBar.setText("Azure TTS might be compatible to the Translation Engine")
                        return
            case 'Google TTS':
                for text in list(google_TTS_list.keys()):
                    if self.ui.comboBox_targetLang.currentText() in text:
                        self.ui.statusBar.setText("Google TTS might be compatible to the Translation Engine")
                        return
            case 'GSpeak':
                for text in list(gSpeak_TTS_list.keys()):
                    if self.ui.comboBox_targetLang.currentText() in text:
                        self.ui.statusBar.setText("GSpeak might be compatible to the Translation Engine")
                        return
            case _:
                pass
            # if self.ui.ttsEngineBox.currentText() == 'Sapi5 (Windows)':
            #     pass
            # if self.ui.ttsEngineBox.currentText() == 'NSS (Mac Only)':
            #     pass
            # if self.ui.ttsEngineBox.currentText() == 'coqui_ai_tts (Unsupported)':
            #     pass
            # if self.ui.ttsEngineBox.currentText() == 'espeak (Unsupported)':
            #     pass
        # # TODO: Iterate targetlang and text to check compatibility

    def set_azure_voice(self, text):
        if text == '':
            text = "en-US-JennyNeural"
        for index in range(self.ui.listWidget_voiceazure.count()):
            item = self.ui.listWidget_voiceazure.item(index)
            if text == item.toolTip():
                self.azure_row = self.ui.listWidget_voiceazure.row(item)
                self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                break

    def preview_pressed(self):
        self.currentButton = self.sender()
        text = self.sender().parent().parent().parent().objectName()
        # print(text)
        if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
            parentWidget = self.ui.listWidget_voiceazure
            for index in range(self.ui.listWidget_voiceazure.count()):
                item = self.ui.listWidget_voiceazure.item(index)
                if text == item.toolTip():
                    self.azure_row = self.ui.listWidget_voiceazure.row(item)
                    self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                    break
            # if self.ui.lineEdit_key.text() == '':
            #     self.ui.lineEdit_key.setFocus()
            #     return
            # if self.ui.lineEdit_region.text() == '':
            #     self.ui.lineEdit_region.setFocus()
            #     return
        elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
            parentWidget = self.ui.listWidget_voicegoogle
            for index in range(self.ui.listWidget_voicegoogle.count()):
                item = self.ui.listWidget_voicegoogle.item(index)
                if text == item.toolTip():
                    self.google_row = self.ui.listWidget_voicegoogle.row(item)
                    self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                    break
            # if self.ui.credsFilePathEdit.text() == '':
            #     self.ui.credsFilePathEdit.setFocus()
            #     return
        elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
            parentWidget = self.ui.onnx_listWidget
            for index in range(self.ui.onnx_listWidget.count()):
                item = self.ui.onnx_listWidget.item(index)
                # print(item.toolTip())
                # if f'({item.toolTip()})' in text:
                if text == item.text():
                    self.onnx_row = self.ui.onnx_listWidget.row(item)
                    self.ui.onnx_listWidget.setCurrentRow(self.onnx_row)
                    break
            if self.sender().objectName() == 'Play':
                self.ui.statusBar.setText(f'Playing: {text}')
            else:
                self.ui.statusBar.setText(f'Downloading: {text}')

        self.OnSavePressed(False)
        if self.temp_config_file is None:
            return
        pyperclip.copy("Hello World")
        pool = QThreadPool.globalInstance()
        runnable = Player(self.temp_config_file)
        runnable.signals.completed.connect(self.enablePlayButtons)
        # buttons = self.ui.listWidget_voiceazure.findChildren(QPushButton)
        buttons = parentWidget.findChildren(QPushButton)
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
            buttons = self.ui.listWidget_voicegoogle.findChildren(QPushButton)
        elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
            buttons = self.ui.onnx_listWidget.findChildren(QPushButton)
        self.ui.ttsEngineBox.setEnabled(True)
        for button in buttons:
            button.setEnabled(True)
        self.movie.stop()
        icon = QIcon()
        icon.addFile(":/images/images/play-round-icon.png")
        self.currentButton.setIcon(icon)
        self.temp_config_file.close()
        os.unlink(self.temp_config_file.name)
        self.ui.statusBar.setText(f'')
        self.temp_config_file = None

    def print_data(self, item):
        try:
            if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
                self.ui.listWidget_voiceazure.setCurrentItem(item)
            elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
                self.ui.listWidget_voicegoogle.setCurrentItem(item)
            elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
                self.ui.onnx_listWidget.setCurrentItem(item)
        except Exception as error:
            pass

    def updateRow(self, row):
        try:
            # Set the row when index become zero (no selected item)
            if self.ui.stackedWidget.currentWidget() == self.ui.azure_page:
                # if self.ui.listWidget_voiceazure.currentRow() == 0:
                if self.ui.listWidget_voiceazure.currentItem() is None:
                    self.ui.listWidget_voiceazure.setCurrentRow(self.azure_row)
                    self.ui.listWidget_voiceazure.setCurrentItem(self.ui.listWidget_voiceazure.item(self.azure_row))
            elif self.ui.stackedWidget.currentWidget() == self.ui.gTTS_page:
                # if self.ui.listWidget_voicegoogle.currentRow() == 0:
                if self.ui.listWidget_voicegoogle.currentItem() is None:
                    self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                    self.ui.listWidget_voicegoogle.setCurrentItem(self.ui.listWidget_voicegoogle.item(self.google_row))
            elif self.ui.stackedWidget.currentWidget() == self.ui.onnx_page:
                # if self.ui.onnx_listWidget.currentRow() == 0:
                if self.ui.onnx_listWidget.currentItem() is None:
                    self.ui.onnx_listWidget.setCurrentRow(self.onnx_row)
                    self.ui.onnx_listWidget.setCurrentItem(self.ui.listWidget_voicegoogle.item(self.onnx_row))
        except Exception as error:
            pass

    def generate_azure_voice_models(self):
        try:
            self.ui.listWidget_voiceazure.currentRowChanged.connect(self.updateRow)
            self.ui.listWidget_voiceazure.itemClicked.connect(self.print_data)
            self.ui.listWidget_voiceazure.setUniformItemSizes(True)
            pool = QThreadPool.globalInstance()
            azureThread = VoiceLoader(parent=self, tts="Azure TTS")
            azureThread.signals.started.connect(lambda: self.load_progress_azure(True))
            azureThread.signals.itemGenerated.connect(self.load_Azure_items)
            azureThread.signals.completed.connect(lambda: self.load_progress_azure(False))
            pool.start(azureThread)
        except Exception as azureError:
            print(str(azureError))

    def get_azure_voices(self):
        file = PySide6.QtCore.QFile(":/binary/azure_voices.json")
        if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
            text = PySide6.QtCore.QTextStream(file).readAll()
            self.voice_list = json.loads(text.encode())
            logging.info("Azure voice list fetched from Resource file.")
            file.close()
        return self.voice_list

    def get_google_voices(self):
        file = PySide6.QtCore.QFile(":/binary/google_voices.json")
        if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
            text = PySide6.QtCore.QTextStream(file).readAll()
            self.voice_google_list = json.loads(text.encode())
            logging.info("Google voice list fetched from Resource file.")
            file.close()
        return self.voice_google_list

    def generate_google_voice_models(self):
        try:
            self.ui.listWidget_voicegoogle.currentRowChanged.connect(self.updateRow)
            self.ui.listWidget_voicegoogle.itemClicked.connect(self.print_data)
            self.ui.listWidget_voicegoogle.setUniformItemSizes(True)
            pool = QThreadPool.globalInstance()
            googleThread = VoiceLoader(parent=self, tts="Google TTS")
            googleThread.signals.started.connect(lambda: self.load_progress_google(True))
            googleThread.signals.itemGenerated.connect(self.load_Google_items)
            googleThread.signals.completed.connect(lambda: self.load_progress_google(False))
            pool.start(googleThread)
        except Exception as googleError:
            print(str(googleError))

    def set_google_voice(self, text):
        if text == '':
            text = "en-US-Wavenet-C"
        for index in range(self.ui.listWidget_voicegoogle.count()):
            item = self.ui.listWidget_voicegoogle.item(index)
            if text == item.toolTip():
                self.google_row = self.ui.listWidget_voicegoogle.row(item)
                self.ui.listWidget_voicegoogle.setCurrentRow(self.google_row)
                break

    def cache_open(self):
        if os.path.isdir(self.audio_path):
            self.ui.statusBar.setText(f"Opened {self.audio_path}")
            os.startfile(self.audio_path)
        else:
            self.ui.statusBar.setText(f"No cached detected. Try using main application first.")

    def open_onnx_cache(self):
        if os.path.isdir(self.onnx_cache_path):
            self.ui.statusBar.setText(f"Opened {self.onnx_cache_path}")
            os.startfile(self.onnx_cache_path)
        else:
            os.makedirs(self.onnx_cache_path)
            os.startfile(self.onnx_cache_path)
            self.ui.statusBar.setText(f"No cached detected. Creating model directory...")

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
            file = PySide6.QtCore.QFile(":/binary/azure_translation.json")
            if file.open(PySide6.QtCore.QIODevice.ReadOnly | PySide6.QtCore.QFile.Text):
                text = PySide6.QtCore.QTextStream(file).readAll()
                language_azure_list = json.loads(text.encode())
                file.close()
        except Exception as error:
            print(error)
            language_azure_list = {}
        self.language_azure_list = {}
        for value in language_azure_list:
            self.language_azure_list[language_azure_list[value]['name']] = value
        return self.language_azure_list

    def set_Translate_dropdown(self, source):
        try:
            lang = [key for key, value in source.items() if value == self.startLang]
            if not len(lang) == 0:
                lang = lang[0]
            copy_lang = lang
            self.ui.comboBox_writeLang.setCurrentText(lang)

            lang = [key for key, value in source.items() if value == self.endLang]
            if not len(lang) == 0:
                lang = lang[0]
            else:
                lang = copy_lang
            self.ui.comboBox_targetLang.setCurrentText(lang)
        except Exception as error:
            logging.error(f"Error setting current text; {error}", exc_info=False)

    def copyAppPath(self):
        pyperclip.copy(self.ui.appPath.text())

    def generate_onnx_voice_model(self):
        try:
            self.iconDownload = QIcon(":/images/images/download.ico")
            self.iconPlayed = QIcon(":/images/images/play-round-icon.png")
            self.onnx_location = self.onnx_cache_path
            self.ui.onnx_listWidget.itemClicked.connect(self.print_data)
            self.ui.search_language.textChanged.connect(self.searchItem)
            self.ui.onnx_listWidget.setUniformItemSizes(True)
            pool = QThreadPool.globalInstance()
            onnxThread = VoiceLoader(parent=self, tts="Sherpa-ONNX")
            onnxThread.signals.started.connect(lambda: self.load_progress_onnx(True))
            onnxThread.signals.itemGenerated.connect(self.load_Onnx_Items)
            onnxThread.signals.completed.connect(lambda: self.load_progress_onnx(False))
            pool.start(onnxThread)
        except Exception as e:
            print(e)

    def load_progress_onnx(self, state):
        policy = self.ui.onnx_listWidget.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.ui.onnx_listWidget.setSizePolicy(policy)
        self.ui.onnx_listWidget.setHidden(state)
        self.ui.onnx_progressBar.setVisible(state)
        if not state:
            self.set_onnx_voice(self.voiceid_onnx)

    def load_progress_azure(self, state):
        policy = self.ui.listWidget_voiceazure.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.ui.listWidget_voiceazure.setSizePolicy(policy)
        self.ui.listWidget_voiceazure.setHidden(state)
        self.ui.azure_progressBar.setVisible(state)
        if not state:
            self.set_azure_voice(self.voiceidAzure)

    def load_progress_google(self, state):
        policy = self.ui.listWidget_voicegoogle.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.ui.listWidget_voicegoogle.setSizePolicy(policy)
        self.ui.listWidget_voicegoogle.setHidden(state)
        self.ui.gTTS_progressBar.setVisible(state)
        if not state:
            self.set_google_voice(self.voiceidGoogle)

    def printItem(self, item):
        self.ui.onnx_listWidget.setCurrentItem(item)

    def action_pressed(self):
        widget = self.sender().parent().parent().parent()
        name = widget.objectName()
        items = self.ui.onnx_listWidget.findItems(name, Qt.MatchContains)
        for item in items:
            self.ui.onnx_listWidget.setCurrentItem(item)
        if self.sender().objectName() == 'Play':
            pass
        else:
            pass

    def searchItem(self, text):
        match_items = self.ui.onnx_listWidget.findItems(text, Qt.MatchContains)
        for i in range(self.ui.onnx_listWidget.count()):
            it = self.ui.onnx_listWidget.item(i)
            it.setHidden(it not in match_items)

    def set_onnx_voice(self, text):
        if text == '':
            text = "eng"
        for index in range(self.ui.onnx_listWidget.count()):
            item = self.ui.onnx_listWidget.item(index)
            if text == item.toolTip():
                self.onnx_row = self.ui.onnx_listWidget.row(item)
                self.ui.onnx_listWidget.setCurrentRow(self.onnx_row)
                break

    def load_Onnx_Items(self, index, data, count):
        try:
            self.ui.onnx_progressBar.setValue((index + 1) * 100 / count)
            item_widget = QWidget()
            item_UI = Ui_item()
            item_UI.setupUi(item_widget)
            item_UI.name.setText(data['name'])
            font = QFont()
            font.setBold(False)
            font.setPointSize(8)
            item_UI.gender.setFont(font)
            item_UI.gender.setText(data['gender'])
            item_UI.play.clicked.connect(self.preview_pressed)
            item_widget.setObjectName(data['name'])

            item = QListWidgetItem()
            item.setForeground(QColor(0, 0, 0, 0))
            item.setText(data['name'])
            item.setToolTip(data['language_codes'][0])
            item.setSizeHint(item_widget.sizeHint())
            self.ui.onnx_listWidget.insertItem(index, item)
            self.ui.onnx_listWidget.setItemWidget(item, item_widget)
            model_path = os.path.join(self.onnx_location, data['language_codes'][0])
            if os.path.exists(model_path):
                item_UI.play.setIcon(self.iconPlayed)
                item_UI.play.setObjectName('Play')
            else:
                item_UI.play.setIcon(self.iconDownload)
                item_UI.play.setObjectName('Download')
        except Exception as onnxError:
            print(str(onnxError))

    def load_Azure_items(self, index, data, count):
        try:
            self.ui.azure_progressBar.setValue((index + 1) * 100 / count)
            item_widget = QWidget()
            item_UI = Ui_item()
            item_UI.setupUi(item_widget)
            item_UI.name.setText(data['name'])
            font = QFont()
            font.setBold(False)
            font.setPointSize(8)
            item_UI.gender.setFont(font)
            item_UI.gender.setText(data['gender'])
            item_UI.play.clicked.connect(self.preview_pressed)
            item_widget.setObjectName(data['name'])

            item = QListWidgetItem()
            item.setForeground(QColor(0, 0, 0, 0))
            item.setText(data['name'])
            # item.setToolTip(data['language_codes'][0])
            item.setToolTip(data['id'])
            item.setSizeHint(item_widget.sizeHint())
            self.ui.listWidget_voiceazure.insertItem(index, item)
            self.ui.listWidget_voiceazure.setItemWidget(item, item_widget)
        except Exception as azureError:
            print(str(azureError))

    def load_Google_items(self, index, data, count):
        self.ui.gTTS_progressBar.setValue((index + 1) * 100 / count)
        item_widget = QWidget()
        item_UI = Ui_item()
        item_UI.setupUi(item_widget)
        item_UI.name.setText(data['name'])
        font = QFont()
        font.setBold(False)
        font.setPointSize(8)
        item_UI.gender.setFont(font)
        item_UI.gender.setText(data['gender'])
        item_UI.play.clicked.connect(self.preview_pressed)
        item_widget.setObjectName(data['name'])

        item = QListWidgetItem()
        item.setForeground(QColor(0, 0, 0, 0))
        item.setText(data['name'])
        # item.setToolTip(data['language_codes'][0])
        item.setToolTip(data['id'])
        item.setSizeHint(item_widget.sizeHint())
        self.ui.listWidget_voicegoogle.insertItem(index, item)
        self.ui.listWidget_voicegoogle.setItemWidget(item, item_widget)


class Signals(QObject):
    started = Signal()
    completed = Signal()
    itemGenerated = Signal(int, dict, int)
    voicesFetched = Signal(list)


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
                    if "client.exe" in file:
                        exe_name = file
            GUI_path = os.path.join(application_path, exe_name)
            # Use subprocess.Popen to run the executable
            cache_location = os.path.join(os.path.dirname(self.temp_config_file.name), 'Audio Files')
            process = subprocess.Popen([GUI_path, "--config", self.temp_config_file.name, "--preview"])
            process.wait()
        elif __file__:
            application_path = os.path.dirname(os.path.dirname(__file__))
            # TODO: GUI_script_path get the upper directory where translatepb.py is located
            GUI_script_path = os.path.join(application_path, 'client.py')
            cache_location = os.path.join(os.path.dirname(self.temp_config_file.name), 'Audio Files')
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


class VoiceLoader(QRunnable):

    def __init__(self, parent, tts=None):
        super().__init__()
        self.tts = tts
        self.signals = Signals()
        self.parent = parent

    def run(self):
        try:
            self.signals.started.emit()
            start = time.perf_counter()
            voices = []
            if self.tts == 'Azure TTS':
                client = MicrosoftClient((ms_token, ms_region))
                try:
                    voices = client.get_available_voices()
                except Exception as getVoicesError:
                    logging.error(str(getVoicesError))
            elif self.tts == 'Google TTS':
                client = GoogleClient(credentials=google_cred_path)
                try:
                    voices = client.get_voices()
                except Exception as getVoicesError:
                    logging.error(str(getVoicesError))
            elif self.tts == 'Sherpa-ONNX':
                client = SherpaOnnxClient()
                try:
                    voices = client.get_voices()
                except Exception as getVoicesError:
                    logging.error(str(getVoicesError))
            self.signals.voicesFetched.emit(voices)
            count = len(voices)
            print(f"Voice fetch time: {time.perf_counter() - start}")
            for index, x in enumerate(voices):
                time.sleep(0.001)
                self.signals.itemGenerated.emit(index, x, count)
            self.signals.completed.emit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    widget = Widget(size)
    widget.show()
    sys.exit(app.exec())
