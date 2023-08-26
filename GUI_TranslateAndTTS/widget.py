# This Python file uses the following encoding: utf-8
import sys
import os
import configparser

from PySide6.QtWidgets import QApplication, QWidget, QDialogButtonBox, QFileDialog, QMessageBox
import PySide6.QtCore

import pyttsx3
import uuid


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

        self.ui.textBrowser.setStyleSheet("background-color: transparent; border: none;")


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
            "Kurdish (Kurmanji)":"ku",
            "Kurdish (Sorani)":"ckb",
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
        voices_google = sorted(voices_google) # Google voices

        self.ui.listWidget_voiceazure.addItems(voices)
        self.ui.listWidget_voicegoogle.addItems(voices_google)
        self.ui.comboBox_writeLang.addItems(self.translate_languages.keys())
        self.ui.comboBox_targetLang.addItems(self.translate_languages.keys())

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


        if getattr(sys, 'frozen', False):
            # Get the path to the user's app data folder
            home_directory = os.path.expanduser("~")
            app_data_path = os.path.join(home_directory, 'AppData', 'Roaming', 'TranslateAndTTS')
        elif __file__:
            app_data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir))

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

            item = self.ui.listWidget_voicegoogle.findItems(self.voiceidGoogle,PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voicegoogle.setCurrentItem(item[0])


            item = [key for key, value in self.voices_sapi_dict.items() if value == self.voiceid_sapi]

            item = self.ui.listWidget_sapi.findItems(item[0],PySide6.QtCore.Qt.MatchExactly)
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

        else:
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

            item = self.ui.listWidget_voiceazure.findItems(self.voiceidAzure,PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voiceazure.setCurrentItem(item[0])

            item = self.ui.listWidget_voicegoogle.findItems(self.voiceidGoogle,PySide6.QtCore.Qt.MatchExactly)
            self.ui.listWidget_voicegoogle.setCurrentItem(item[0])


        self.ui.radioButton_azure.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_google.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_nsss.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_coqui.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_espeak.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_sapi5.toggled.connect(self.onTTSEngineToggled)
        self.ui.radioButton_gspeak.toggled.connect(self.onTTSEngineToggled)

        self.ui.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.OnSavePressed)
        self.ui.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.OnDiscardPressed)

        self.ui.browseButton.clicked.connect(self.OnBrowseButtonPressed)

        self.ui.credsFilePathEdit.textChanged.connect(self.OnCredsFilePathChanged)

    def onTTSEngineToggled(self):
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

    def OnSavePressed(self):
        # Add sections and key-value pairs

        self.startLang = self.translate_languages[self.ui.comboBox_writeLang.currentText()]
        self.endLang = self.translate_languages[self.ui.comboBox_targetLang.currentText()]
        self.notranslate = not self.ui.checkBox_translate.isChecked()

        id = self.get_uuid()
        self.config.clear()

        self.config.add_section('App')
        self.config.set('App', 'uuid', str(id))
        self.config.set('App', 'collectstats', str(self.ui.checkBox_stats.isChecked()))


        self.config.add_section('translate')
        self.config.set('translate', 'noTranslate', str(self.notranslate))
        self.config.set('translate', 'startLang', self.startLang)
        self.config.set('translate', 'endLang', self.endLang)
        self.config.set('translate', 'replacepb', str(self.ui.checkBox_overwritepb.isChecked()))

        self.config.add_section('TTS')
        self.config.set('TTS', 'engine', self.ttsEngine)
        if self.ttsEngine == 'azureTTS':
            self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio.isChecked()))
        elif self.ttsEngine == 'gTTS':
            self.config.set('TTS', 'save_audio_file', str(self.ui.checkBox_saveAudio_gTTS.isChecked()))
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
        self.config.set('azureTTS', 'voiceid', self.ui.listWidget_voiceazure.currentItem().text())

        self.config.add_section('googleTTS')
        self.config.set('googleTTS', 'creds_file', self.credsFilePath)
        self.config.set('googleTTS', 'voiceid', self.ui.listWidget_voicegoogle.currentItem().text())

        self.config.add_section('sapi5TTS')
        self.config.set('sapi5TTS', 'voiceid', self.voices_sapi_dict[self.ui.listWidget_sapi.currentItem().text()])

        self.config.add_section('kurdishTTS')
        self.config.set('kurdishTTS', 'latin', str(self.ui.checkBox_latin.isChecked()).lower())
        self.config.set('kurdishTTS', 'punctuation', str(self.ui.checkBox_punctuation.isChecked()).lower())

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
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
        self.close()

    def OnDiscardPressed(self):
        self.close()

    def OnBrowseButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.credsFilePath, _ = QFileDialog.getOpenFileName(self, "Open JSON File containing OAuth 2.0 Credentials", "", "JSON Files (*.json)", options=options)
        self.ui.credsFilePathEdit.setText(self.credsFilePath)

    def OnCredsFilePathChanged(self):
        self.credsFilePath = self.ui.credsFilePathEdit.text()

    def get_uuid(self):
        try:
            # Code that may raise an exception
            id = uuid.UUID(self.config.get('App', 'uuid'))
        except Exception as e:
            # Code to handle other exceptions
            id = uuid.uuid4()
            pass

        return str(id)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
