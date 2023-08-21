# This Python file uses the following encoding: utf-8
import sys
import os
import configparser

from PySide6.QtWidgets import QApplication, QWidget, QDialogButtonBox, QMessageBox
import PySide6.QtCore

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Translate Language Dictionary
        self.translate_languages = {"Afrikaans":"af",
            "Arabic":"ar",
            "Bulgarian":"bg",
            "Bengali":"bn",
            "Bosnian":"bs",
            "Catalan":"ca",
            "Czech":"cs",
            "Danish":"da",
            "German":"de",
            "Greek":"el",
            "English":"en",
            "Spanish":"es",
            "Estonian":"et",
            "Finnish":"fi",
            "French":"fr",
            "Gujarati":"gu",
            "Hindi":"hi",
            "Croatian":"hr",
            "Hungarian":"hu",
            "Indonesian":"id",
            "Icelandic":"is",
            "Italian":"it",
            "Hebrew":"iw",
            "Japanese":"ja",
            "Javanese":"jw",
            "Khmer":"km",
            "Kannada":"kn",
            "Korean":"ko",
            "Latin":"la",
            "Latvian":"lv",
            "Malayalam":"ml",
            "Marathi":"mr",
            "Malay":"ms",
            "Myanmar(Burmese)":"my",
            "Nepali":"ne",
            "Dutch":"nl",
            "Norwegian":"no",
            "Polish":"pl",
            "Portuguese":"pt",
            "Romanian":"ro",
            "Russian":"ru",
            "Sinhala":"si",
            "Slovak":"sk",
            "Albanian":"sq",
            "Serbian":"sr",
            "Sundanese":"su",
            "Swedish":"sv",
            "Swahili":"sw",
            "Tamil":"ta",
            "Telugu":"te",
            "Thai":"th",
            "Filipino":"tl",
            "Turkish":"tr",
            "Ukrainian":"uk",
            "Urdu":"ur",
            "Vietnamese":"vi",
            "Chinese(Simplified)":"zh-CN",
            "Chinese(Mandarin/Taiwan)":"zh-TW",
            "Chinese(Mandarin)":"zh"}

        voices = """af-ZA-AdriNeural
        af-ZA-WillemNeural
        am-ET-MekdesNeural
        am-ET-AmehaNeural
        ar-AE-FatimaNeural
        ar-AE-HamdanNeural
        ar-BH-LailaNeural
        ar-BH-AliNeural
        ar-DZ-AminaNeural
        ar-DZ-IsmaelNeural
        ar-EG-SalmaNeural
        ar-EG-ShakirNeural
        ar-IQ-RanaNeural
        ar-IQ-BasselNeural
        ar-JO-SanaNeural
        ar-JO-TaimNeural
        ar-KW-NouraNeural
        ar-KW-FahedNeural
        ar-LB-LaylaNeural
        ar-LB-RamiNeural
        ar-LY-ImanNeural
        ar-LY-OmarNeural
        ar-MA-MounaNeural
        ar-MA-JamalNeural
        ar-OM-AyshaNeural
        ar-OM-AbdullahNeural
        ar-QA-AmalNeural
        ar-QA-MoazNeural
        ar-SA-ZariyahNeural
        ar-SA-HamedNeural
        ar-SY-AmanyNeural
        ar-SY-LaithNeural
        ar-TN-ReemNeural
        ar-TN-HediNeural
        ar-YE-MaryamNeural
        ar-YE-SalehNeural
        az-AZ-BanuNeural
        az-AZ-BabekNeural
        bg-BG-KalinaNeural
        bg-BG-BorislavNeural
        bn-BD-NabanitaNeural
        bn-BD-PradeepNeural
        bn-IN-TanishaaNeural
        bn-IN-BashkarNeural
        bs-BA-VesnaNeural
        bs-BA-GoranNeural
        ca-ES-JoanaNeural
        ca-ES-EnricNeural
        ca-ES-AlbaNeural
        cs-CZ-VlastaNeural
        cs-CZ-AntoninNeural
        cy-GB-NiaNeural
        cy-GB-AledNeural
        da-DK-ChristelNeural
        da-DK-JeppeNeural
        de-AT-IngridNeural
        de-AT-JonasNeural
        de-CH-LeniNeural
        de-CH-JanNeural
        de-DE-KatjaNeural
        de-DE-ConradNeural
        de-DE-AmalaNeural
        de-DE-BerndNeural
        de-DE-ChristophNeural
        de-DE-ElkeNeural
        de-DE-GiselaNeural
        de-DE-KasperNeural
        de-DE-KillianNeural
        de-DE-KlarissaNeural
        de-DE-KlausNeural
        de-DE-LouisaNeural
        de-DE-MajaNeural
        de-DE-RalfNeural
        de-DE-TanjaNeural
        el-GR-AthinaNeural
        el-GR-NestorasNeural
        en-AU-NatashaNeural
        en-AU-WilliamNeural
        en-AU-AnnetteNeural
        en-AU-CarlyNeural
        en-AU-DarrenNeural
        en-AU-DuncanNeural
        en-AU-ElsieNeural
        en-AU-FreyaNeural
        en-AU-JoanneNeural
        en-AU-KenNeural
        en-AU-KimNeural
        en-AU-NeilNeural
        en-AU-TimNeural
        en-AU-TinaNeural
        en-CA-ClaraNeural
        en-CA-LiamNeural
        en-GB-SoniaNeural
        en-GB-RyanNeural
        en-GB-LibbyNeural
        en-GB-AbbiNeural
        en-GB-AlfieNeural
        en-GB-BellaNeural
        en-GB-ElliotNeural
        en-GB-EthanNeural
        en-GB-HollieNeural
        en-GB-MaisieNeural
        en-GB-NoahNeural
        en-GB-OliverNeural
        en-GB-OliviaNeural
        en-GB-ThomasNeural
        en-GB-MiaNeural
        en-HK-YanNeural
        en-HK-SamNeural
        en-IE-EmilyNeural
        en-IE-ConnorNeural
        en-IN-NeerjaNeural
        en-IN-PrabhatNeural
        en-KE-AsiliaNeural
        en-KE-ChilembaNeural
        en-NG-EzinneNeural
        en-NG-AbeoNeural
        en-NZ-MollyNeural
        en-NZ-MitchellNeural
        en-PH-RosaNeural
        en-PH-JamesNeural
        en-SG-LunaNeural
        en-SG-WayneNeural
        en-TZ-ImaniNeural
        en-TZ-ElimuNeural
        en-US-JennyMultilingualNeural
        en-US-JennyNeural
        en-US-GuyNeural
        en-US-AriaNeural
        en-US-DavisNeural
        en-US-AmberNeural
        en-US-AnaNeural
        en-US-AshleyNeural
        en-US-BrandonNeural
        en-US-ChristopherNeural
        en-US-CoraNeural
        en-US-ElizabethNeural
        en-US-EricNeural
        en-US-JacobNeural
        en-US-JaneNeural
        en-US-JasonNeural
        en-US-MichelleNeural
        en-US-MonicaNeural
        en-US-NancyNeural
        en-US-RogerNeural
        en-US-SaraNeural
        en-US-SteffanNeural
        en-US-TonyNeural
        en-ZA-LeahNeural
        en-ZA-LukeNeural
        es-AR-ElenaNeural
        es-AR-TomasNeural
        es-BO-SofiaNeural
        es-BO-MarceloNeural
        es-CL-CatalinaNeural
        es-CL-LorenzoNeural
        es-CO-SalomeNeural
        es-CO-GonzaloNeural
        es-CR-MariaNeural
        es-CR-JuanNeural
        es-CU-BelkysNeural
        es-CU-ManuelNeural
        es-DO-RamonaNeural
        es-DO-EmilioNeural
        es-EC-AndreaNeural
        es-EC-LuisNeural
        es-ES-ElviraNeural
        es-ES-AlvaroNeural
        es-ES-AbrilNeural
        es-ES-ArnauNeural
        es-ES-DarioNeural
        es-ES-EliasNeural
        es-ES-EstrellaNeural
        es-ES-IreneNeural
        es-ES-LaiaNeural
        es-ES-LiaNeural
        es-ES-NilNeural
        es-ES-SaulNeural
        es-ES-TeoNeural
        es-ES-TrianaNeural
        es-ES-VeraNeural
        es-GQ-TeresaNeural
        es-GQ-JavierNeural
        es-GT-MartaNeural
        es-GT-AndresNeural
        es-HN-KarlaNeural
        es-HN-CarlosNeural
        es-MX-DaliaNeural
        es-MX-JorgeNeural
        es-MX-BeatrizNeural
        es-MX-CandelaNeural
        es-MX-CarlotaNeural
        es-MX-CecilioNeural
        es-MX-GerardoNeural
        es-MX-LarissaNeural
        es-MX-LibertoNeural
        es-MX-LucianoNeural
        es-MX-MarinaNeural
        es-MX-NuriaNeural
        es-MX-PelayoNeural
        es-MX-RenataNeural
        es-MX-YagoNeural
        es-NI-YolandaNeural
        es-NI-FedericoNeural
        es-PA-MargaritaNeural
        es-PA-RobertoNeural
        es-PE-CamilaNeural
        es-PE-AlexNeural
        es-PR-KarinaNeural
        es-PR-VictorNeural
        es-PY-TaniaNeural
        es-PY-MarioNeural
        es-SV-LorenaNeural
        es-SV-RodrigoNeural
        es-US-PalomaNeural
        es-US-AlonsoNeural
        es-UY-ValentinaNeural
        es-UY-MateoNeural
        es-VE-PaolaNeural
        es-VE-SebastianNeural
        et-EE-AnuNeural
        et-EE-KertNeural
        eu-ES-AinhoaNeural
        eu-ES-AnderNeural
        fa-IR-DilaraNeural
        fa-IR-FaridNeural
        fi-FI-SelmaNeural
        fi-FI-HarriNeural
        fi-FI-NooraNeural
        fil-PH-BlessicaNeural
        fil-PH-AngeloNeural
        fr-BE-CharlineNeural
        fr-BE-GerardNeural
        fr-CA-SylvieNeural
        fr-CA-JeanNeural
        fr-CA-AntoineNeural
        fr-CH-ArianeNeural
        fr-CH-FabriceNeural
        fr-FR-DeniseNeural
        fr-FR-HenriNeural
        fr-FR-AlainNeural
        fr-FR-BrigitteNeural
        fr-FR-CelesteNeural
        fr-FR-ClaudeNeural
        fr-FR-CoralieNeural
        fr-FR-EloiseNeural
        fr-FR-JacquelineNeural
        fr-FR-JeromeNeural
        fr-FR-JosephineNeural
        fr-FR-MauriceNeural
        fr-FR-YvesNeural
        fr-FR-YvetteNeural
        ga-IE-OrlaNeural
        ga-IE-ColmNeural
        gl-ES-SabelaNeural
        gl-ES-RoiNeural
        gu-IN-DhwaniNeural
        gu-IN-NiranjanNeural
        he-IL-HilaNeural
        he-IL-AvriNeural
        hi-IN-SwaraNeural
        hi-IN-MadhurNeural
        hr-HR-GabrijelaNeural
        hr-HR-SreckoNeural
        hu-HU-NoemiNeural
        hu-HU-TamasNeural
        hy-AM-AnahitNeural
        hy-AM-HaykNeural
        id-ID-GadisNeural
        id-ID-ArdiNeural
        is-IS-GudrunNeural
        is-IS-GunnarNeural
        it-IT-ElsaNeural
        it-IT-IsabellaNeural
        it-IT-DiegoNeural
        it-IT-BenignoNeural
        it-IT-CalimeroNeural
        it-IT-CataldoNeural
        it-IT-FabiolaNeural
        it-IT-FiammaNeural
        it-IT-GianniNeural
        it-IT-ImeldaNeural
        it-IT-IrmaNeural
        it-IT-LisandroNeural
        it-IT-PalmiraNeural
        it-IT-PierinaNeural
        it-IT-RinaldoNeural
        ja-JP-NanamiNeural
        ja-JP-KeitaNeural
        ja-JP-AoiNeural
        ja-JP-DaichiNeural
        ja-JP-MayuNeural
        ja-JP-NaokiNeural
        ja-JP-ShioriNeural
        jv-ID-SitiNeural
        jv-ID-DimasNeural
        ka-GE-EkaNeural
        ka-GE-GiorgiNeural
        kk-KZ-AigulNeural
        kk-KZ-DauletNeural
        km-KH-SreymomNeural
        km-KH-PisethNeural
        kn-IN-SapnaNeural
        kn-IN-GaganNeural
        ko-KR-SunHiNeural
        ko-KR-InJoonNeural
        ko-KR-BongJinNeural
        ko-KR-GookMinNeural
        ko-KR-JiMinNeural
        ko-KR-SeoHyeonNeural
        ko-KR-SoonBokNeural
        ko-KR-YuJinNeural
        lo-LA-KeomanyNeural
        lo-LA-ChanthavongNeural
        lt-LT-OnaNeural
        lt-LT-LeonasNeural
        lv-LV-EveritaNeural
        lv-LV-NilsNeural
        mk-MK-MarijaNeural
        mk-MK-AleksandarNeural
        ml-IN-SobhanaNeural
        ml-IN-MidhunNeural
        mn-MN-YesuiNeural
        mn-MN-BataaNeural
        mr-IN-AarohiNeural
        mr-IN-ManoharNeural
        ms-MY-YasminNeural
        ms-MY-OsmanNeural
        mt-MT-GraceNeural
        mt-MT-JosephNeural
        my-MM-NilarNeural
        my-MM-ThihaNeural
        nb-NO-PernilleNeural
        nb-NO-FinnNeural
        nb-NO-IselinNeural
        ne-NP-HemkalaNeural
        ne-NP-SagarNeural
        nl-BE-DenaNeural
        nl-BE-ArnaudNeural
        nl-NL-FennaNeural
        nl-NL-MaartenNeural
        nl-NL-ColetteNeural
        pl-PL-AgnieszkaNeural
        pl-PL-MarekNeural
        pl-PL-ZofiaNeural
        ps-AF-LatifaNeural
        ps-AF-GulNawazNeural
        pt-BR-FranciscaNeural
        pt-BR-AntonioNeural
        pt-BR-BrendaNeural
        pt-BR-DonatoNeural
        pt-BR-ElzaNeural
        pt-BR-FabioNeural
        pt-BR-GiovannaNeural
        pt-BR-HumbertoNeural
        pt-BR-JulioNeural
        pt-BR-LeilaNeural
        pt-BR-LeticiaNeural
        pt-BR-ManuelaNeural
        pt-BR-NicolauNeural
        pt-BR-ValerioNeural
        pt-BR-YaraNeural
        pt-PT-RaquelNeural
        pt-PT-DuarteNeural
        pt-PT-FernandaNeural
        ro-RO-AlinaNeural
        ro-RO-EmilNeural
        ru-RU-SvetlanaNeural
        ru-RU-DmitryNeural
        ru-RU-DariyaNeural
        si-LK-ThiliniNeural
        si-LK-SameeraNeural
        sk-SK-ViktoriaNeural
        sk-SK-LukasNeural
        sl-SI-PetraNeural
        sl-SI-RokNeural
        so-SO-UbaxNeural
        so-SO-MuuseNeural
        sq-AL-AnilaNeural
        sq-AL-IlirNeural
        sr-RS-SophieNeural
        sr-RS-NicholasNeural
        su-ID-TutiNeural
        su-ID-JajangNeural
        sv-SE-SofieNeural
        sv-SE-MattiasNeural
        sv-SE-HilleviNeural
        sw-KE-ZuriNeural
        sw-KE-RafikiNeural
        sw-TZ-RehemaNeural
        sw-TZ-DaudiNeural
        ta-IN-PallaviNeural
        ta-IN-ValluvarNeural
        ta-LK-SaranyaNeural
        ta-LK-KumarNeural
        ta-MY-KaniNeural
        ta-MY-SuryaNeural
        ta-SG-VenbaNeural
        ta-SG-AnbuNeural
        te-IN-ShrutiNeural
        te-IN-MohanNeural
        th-TH-PremwadeeNeural
        th-TH-NiwatNeural
        th-TH-AcharaNeural
        tr-TR-EmelNeural
        tr-TR-AhmetNeural
        uk-UA-PolinaNeural
        uk-UA-OstapNeural
        ur-IN-GulNeural
        ur-IN-SalmanNeural
        ur-PK-UzmaNeural
        ur-PK-AsadNeural
        uz-UZ-MadinaNeural
        uz-UZ-SardorNeural
        vi-VN-HoaiMyNeural
        vi-VN-NamMinhNeural
        wuu-CN-XiaotongNeural
        wuu-CN-YunzheNeural
        zh-CN-XiaoxiaoNeural
        zh-CN-YunxiNeural
        zh-CN-YunjianNeural
        zh-CN-XiaoyiNeural
        zh-CN-YunyangNeural
        zh-CN-XiaochenNeural
        zh-CN-XiaohanNeural
        zh-CN-XiaomengNeural
        zh-CN-XiaomoNeural
        zh-CN-XiaoqiuNeural
        zh-CN-XiaoruiNeural
        zh-CN-XiaoshuangNeural
        zh-CN-XiaoxuanNeural
        zh-CN-XiaoyanNeural
        zh-CN-XiaoyouNeural
        zh-CN-XiaozhenNeural
        zh-CN-YunfengNeural
        zh-CN-YunhaoNeural
        zh-CN-YunxiaNeural
        zh-CN-YunyeNeural
        zh-CN-YunzeNeural
        zh-CN-henan-YundengNeural
        zh-CN-liaoning-XiaobeiNeural
        zh-CN-shaanxi-XiaoniNeural
        zh-CN-shandong-YunxiangNeural
        zh-CN-sichuan-YunxiNeural
        zh-HK-HiuMaanNeural
        zh-HK-WanLungNeural
        zh-HK-HiuGaaiNeural
        zh-TW-HsiaoChenNeural
        zh-TW-YunJheNeural
        zh-TW-HsiaoYuNeural
        zu-ZA-ThandoNeural
        zu-ZA-ThembaNeural"""

        voices = voices.replace(" ", "")
        # Split the text into lines
        voices = voices.split("\n")
        voices = sorted(voices) # Azure voices

        self.ui.listWidget_voiceazure.addItems(voices)
        self.ui.comboBox_writeLang.addItems(self.translate_languages.keys())
        self.ui.comboBox_targetLang.addItems(self.translate_languages.keys())

        if getattr(sys, 'frozen', False):
            # Get the path to the user's app data folder
            home_directory = os.path.expanduser("~")
            app_data_path = os.path.join(home_directory, 'AppData', 'Roaming', 'TranslateAndTTS')
        elif __file__:
            app_data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir))

        self.config_path = os.path.join(app_data_path, 'settings.cfg')

        self.config = configparser.ConfigParser()

        # Check if the file already exists
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)


            self.notranslate = self.ttsEngine = self.config.getboolean('translate', 'noTranslate')
            self.startLang = self.config.get('translate', 'startLang')
            self.endLang = self.config.get('translate', 'endLang')
            self.overwritePb = self.config.getboolean('translate', 'replacepb')


            self.ttsEngine = self.config.get('TTS', 'engine')
            self.voiceid = self.config.get('TTS', 'voiceid')
            self.rate = self.config.getint('TTS', 'rate')
            self.volume = self.config.getint('TTS', 'volume')

            self.key = self.config.get('azureTTS', 'key')
            self.region = self.config.get('azureTTS', 'location')
            self.voiceidAzure = self.config.get('azureTTS', 'voiceid')
            self.saveToWav = self.config.getboolean('azureTTS', 'save_to_wav')

            if self.ttsEngine == "azureTTS":
                self.ui.stackedWidget.setCurrentIndex(0)
                self.ui.radioButton_azure.setChecked(True)
            else:
                self.ui.stackedWidget.setCurrentIndex(1)
                if self.ttsEngine == "gTTS":
                    self.ui.radioButton_google.setChecked(True)
                elif self.ttsEngine == "espeak":
                    self.ui.radioButton_espeak.setChecked(True)
                elif self.ttsEngine == "sapi5":
                    self.ui.radioButton_sapi5.setChecked(True)
                elif self.ttsEngine == "nsss":
                    self.ui.radioButton_nsss.setChecked(True)
                elif self.ttsEngine == "coqui":
                    self.ui.radioButton_coqui.setChecked(True)
                else:
                    self.ui.radioButton_azure.setChecked(True)


            lang = [key for key, value in self.translate_languages.items() if value == self.startLang.lower()]
            if not len(lang) == 0:
                lang = lang[0]
            self.ui.comboBox_writeLang.setCurrentText(lang)

            lang = [key for key, value in self.translate_languages.items() if value == self.endLang.lower()]
            if not len(lang) == 0:
                lang = lang[0]
            self.ui.comboBox_targetLang.setCurrentText(lang)

            item = self.ui.listWidget_voiceazure.findItems(self.voiceidAzure,PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voiceazure.setCurrentItem(item[0])

            self.ui.checkBox_translate.setChecked(not self.notranslate)
            self.ui.checkBox_overwritepb.setChecked(self.overwritePb)
            self.ui.checkBox_saveToWav.setChecked(self.saveToWav)

            self.ui.horizontalSlider_rate.setValue(self.rate)
            self.ui.horizontalSlider_volume.setValue(self.volume)
            self.ui.lineEdit_voiceID.setText(self.voiceid)
            self.ui.lineEdit_key.setText(self.key)
            self.ui.lineEdit_region.setText(self.region)

        else:
            self.ttsEngine = "azureTTS"
            self.ui.stackedWidget.setCurrentIndex(0)

            self.notranslate = False
            self.saveToWav = True
            self.overwritePb = True

            self.voiceid = None
            self.voiceidAzure = "en-US-JennyNeural"

            self.rate = None
            self.volume = None

            self.key = None
            self.region = None
            self.startLang = None
            self.endLang = None

            item = self.ui.listWidget_voiceazure.findItems(self.voiceidAzure,PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voiceazure.setCurrentItem(item[0])


        self.ui.radioButton_azure.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_google.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_nsss.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_coqui.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_espeak.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_sapi5.toggled.connect(self.onTTSEngineToggled)

        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.OnSavePressed)
        self.ui.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.OnDiscardPressed)

    def onTTSEngineToggled(self):
        if self.ui.radioButton_azure.isChecked():
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ttsEngine = "azureTTS"
        else:
            self.ui.stackedWidget.setCurrentIndex(1)
            if self.ui.radioButton_google.isChecked():
                self.ttsEngine = "gTTS"
            elif self.ui.radioButton_espeak.isChecked():
                self.ttsEngine = "espeak"
            elif self.ui.radioButton_espeak.isChecked():
                self.ttsEngine = "nsss"
            elif self.ui.radioButton_espeak.isChecked():
                self.ttsEngine = "coqui"
            elif self.ui.radioButton_sapi5.isChecked():
                self.ttsEngine = "sapi5"
            else:
                self.ttsEngine = "azureTTS"

    def OnSavePressed(self):
        # Add sections and key-value pairs
        self.config.clear()
        self.config.add_section('translate')
        self.config.set('translate', 'noTranslate', str(not self.ui.checkBox_translate.isChecked()))
        self.config.set('translate', 'startLang', self.translate_languages[self.ui.comboBox_writeLang.currentText()])
        self.config.set('translate', 'endLang', self.translate_languages[self.ui.comboBox_targetLang.currentText()])
        self.config.set('translate', 'replacepb', str(self.ui.checkBox_overwritepb.isChecked()))

        self.config.add_section('TTS')
        self.config.set('TTS', 'engine', self.ttsEngine)
        self.config.set('TTS', 'voiceid', self.ui.lineEdit_voiceID.text())
        self.config.set('TTS', 'rate', str(self.ui.horizontalSlider_rate.value()))
        self.config.set('TTS', 'volume', str(self.ui.horizontalSlider_volume.value()))

        self.config.add_section('azureTTS')
        self.config.set('azureTTS', 'key', self.ui.lineEdit_key.text())
        self.config.set('azureTTS', 'location', self.ui.lineEdit_region.text())
        self.config.set('azureTTS', 'voiceid', self.ui.listWidget_voiceazure.currentItem().text())
        self.config.set('azureTTS', 'save_to_wav', str(self.ui.checkBox_saveToWav.isChecked()))

        # Write the configuration to a file
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

        self.close()


    def OnDiscardPressed(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
