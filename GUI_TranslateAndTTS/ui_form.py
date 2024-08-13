# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDialogButtonBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QStackedWidget, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(817, 616)
        icon = QIcon()
        icon.addFile(u":/images/images/configure.ico", QSize(), QIcon.Normal, QIcon.Off)
        Widget.setWindowIcon(icon)
        self.verticalLayout_18 = QVBoxLayout(Widget)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.TextToSpeechSetting = QWidget()
        self.TextToSpeechSetting.setObjectName(u"TextToSpeechSetting")
        self.verticalLayout_19 = QVBoxLayout(self.TextToSpeechSetting)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ttsEngineBox = QComboBox(self.TextToSpeechSetting)
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.addItem("")
        self.ttsEngineBox.setObjectName(u"ttsEngineBox")
        self.ttsEngineBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_3.addWidget(self.ttsEngineBox)

        self.horizontalSpacer = QSpacerItem(299, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_19.addLayout(self.horizontalLayout_3)

        self.stackedWidget = QStackedWidget(self.TextToSpeechSetting)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.azure_page = QWidget()
        self.azure_page.setObjectName(u"azure_page")
        self.gridLayout_10 = QGridLayout(self.azure_page)
        self.gridLayout_10.setSpacing(2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.formWidget_4 = QWidget(self.azure_page)
        self.formWidget_4.setObjectName(u"formWidget_4")
        self.gridLayout_4 = QGridLayout(self.formWidget_4)
        self.gridLayout_4.setSpacing(3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.formWidget_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet(u"border: ")
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.groupBox_2.setFlat(False)
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.listWidget_voiceazure = QListWidget(self.groupBox_2)
        self.listWidget_voiceazure.setObjectName(u"listWidget_voiceazure")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget_voiceazure.sizePolicy().hasHeightForWidth())
        self.listWidget_voiceazure.setSizePolicy(sizePolicy1)
        self.listWidget_voiceazure.setStyleSheet(u"")
        self.listWidget_voiceazure.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.listWidget_voiceazure.setSortingEnabled(True)

        self.verticalLayout_7.addWidget(self.listWidget_voiceazure)


        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 2)


        self.gridLayout_10.addWidget(self.formWidget_4, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.azure_page)
        self.gTTS_page = QWidget()
        self.gTTS_page.setObjectName(u"gTTS_page")
        self.gridLayout_11 = QGridLayout(self.gTTS_page)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridWidget_2 = QWidget(self.gTTS_page)
        self.gridWidget_2.setObjectName(u"gridWidget_2")
        self.gridLayout_6 = QGridLayout(self.gridWidget_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.groupBox_3 = QGroupBox(self.gridWidget_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(Qt.AlignCenter)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.listWidget_voicegoogle = QListWidget(self.groupBox_3)
        self.listWidget_voicegoogle.setObjectName(u"listWidget_voicegoogle")
        self.listWidget_voicegoogle.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.listWidget_voicegoogle.setSortingEnabled(True)

        self.verticalLayout_8.addWidget(self.listWidget_voicegoogle)


        self.gridLayout_6.addWidget(self.groupBox_3, 1, 0, 1, 2)


        self.gridLayout_11.addWidget(self.gridWidget_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.gTTS_page)
        self.gspeak_page = QWidget()
        self.gspeak_page.setObjectName(u"gspeak_page")
        self.verticalLayout_11 = QVBoxLayout(self.gspeak_page)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.textBrowser = QTextBrowser(self.gspeak_page)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy2)
        self.textBrowser.setAutoFillBackground(True)

        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.verticalLayout_11.addLayout(self.gridLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 140, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.gspeak_page)
        self.sapi_page = QWidget()
        self.sapi_page.setObjectName(u"sapi_page")
        self.verticalLayout_10 = QVBoxLayout(self.sapi_page)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_8 = QLabel(self.sapi_page)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_8.addWidget(self.label_8, 1, 0, 1, 1)

        self.listWidget_sapi = QListWidget(self.sapi_page)
        self.listWidget_sapi.setObjectName(u"listWidget_sapi")

        self.gridLayout_8.addWidget(self.listWidget_sapi, 3, 1, 1, 1)

        self.horizontalSlider_rate_sapi = QSlider(self.sapi_page)
        self.horizontalSlider_rate_sapi.setObjectName(u"horizontalSlider_rate_sapi")
        self.horizontalSlider_rate_sapi.setMaximum(100)
        self.horizontalSlider_rate_sapi.setValue(100)
        self.horizontalSlider_rate_sapi.setOrientation(Qt.Horizontal)

        self.gridLayout_8.addWidget(self.horizontalSlider_rate_sapi, 1, 1, 1, 1)

        self.label_12 = QLabel(self.sapi_page)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_8.addWidget(self.label_12, 3, 0, 1, 1)

        self.horizontalSlider_volume_sapi = QSlider(self.sapi_page)
        self.horizontalSlider_volume_sapi.setObjectName(u"horizontalSlider_volume_sapi")
        self.horizontalSlider_volume_sapi.setMaximum(100)
        self.horizontalSlider_volume_sapi.setValue(100)
        self.horizontalSlider_volume_sapi.setOrientation(Qt.Horizontal)

        self.gridLayout_8.addWidget(self.horizontalSlider_volume_sapi, 0, 1, 1, 1)

        self.label_7 = QLabel(self.sapi_page)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_8.addWidget(self.label_7, 0, 0, 1, 1)

        self.checkBox_saveAudio_sapi = QCheckBox(self.sapi_page)
        self.checkBox_saveAudio_sapi.setObjectName(u"checkBox_saveAudio_sapi")
        self.checkBox_saveAudio_sapi.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_saveAudio_sapi, 2, 1, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout_8)

        self.verticalSpacer = QSpacerItem(20, 61, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.sapi_page)
        self.kurdish_page = QWidget()
        self.kurdish_page.setObjectName(u"kurdish_page")
        self.verticalLayout_12 = QVBoxLayout(self.kurdish_page)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.checkBox_saveAudio_kurdish = QCheckBox(self.kurdish_page)
        self.checkBox_saveAudio_kurdish.setObjectName(u"checkBox_saveAudio_kurdish")
        self.checkBox_saveAudio_kurdish.setChecked(True)

        self.gridLayout_7.addWidget(self.checkBox_saveAudio_kurdish, 0, 0, 1, 1)

        self.checkBox_latin = QCheckBox(self.kurdish_page)
        self.checkBox_latin.setObjectName(u"checkBox_latin")
        self.checkBox_latin.setChecked(True)

        self.gridLayout_7.addWidget(self.checkBox_latin, 1, 0, 1, 1)

        self.checkBox_punctuation = QCheckBox(self.kurdish_page)
        self.checkBox_punctuation.setObjectName(u"checkBox_punctuation")
        self.checkBox_punctuation.setChecked(False)

        self.gridLayout_7.addWidget(self.checkBox_punctuation, 2, 0, 1, 1)


        self.verticalLayout_12.addLayout(self.gridLayout_7)

        self.verticalSpacer_3 = QSpacerItem(20, 269, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.kurdish_page)
        self.ttsPage = QWidget()
        self.ttsPage.setObjectName(u"ttsPage")
        self.verticalLayout_13 = QVBoxLayout(self.ttsPage)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_3 = QLabel(self.ttsPage)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalSlider_volume = QSlider(self.ttsPage)
        self.horizontalSlider_volume.setObjectName(u"horizontalSlider_volume")
        self.horizontalSlider_volume.setMaximum(100)
        self.horizontalSlider_volume.setValue(100)
        self.horizontalSlider_volume.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.horizontalSlider_volume, 0, 1, 1, 1)

        self.label_4 = QLabel(self.ttsPage)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)

        self.horizontalSlider_rate = QSlider(self.ttsPage)
        self.horizontalSlider_rate.setObjectName(u"horizontalSlider_rate")
        self.horizontalSlider_rate.setMaximum(100)
        self.horizontalSlider_rate.setValue(100)
        self.horizontalSlider_rate.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.horizontalSlider_rate, 1, 1, 1, 1)

        self.label_5 = QLabel(self.ttsPage)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 2, 0, 1, 1)

        self.lineEdit_voiceID = QLineEdit(self.ttsPage)
        self.lineEdit_voiceID.setObjectName(u"lineEdit_voiceID")

        self.gridLayout_5.addWidget(self.lineEdit_voiceID, 2, 1, 1, 1)


        self.verticalLayout_13.addLayout(self.gridLayout_5)

        self.verticalSpacer_4 = QSpacerItem(20, 256, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_4)

        self.stackedWidget.addWidget(self.ttsPage)
        self.onnx_page = QWidget()
        self.onnx_page.setObjectName(u"onnx_page")
        self.verticalLayout_20 = QVBoxLayout(self.onnx_page)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.groupBox = QGroupBox(self.onnx_page)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(u"border")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_17 = QVBoxLayout(self.groupBox)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.onnx_listWidget = QListWidget(self.groupBox)
        self.onnx_listWidget.setObjectName(u"onnx_listWidget")

        self.verticalLayout_17.addWidget(self.onnx_listWidget)


        self.verticalLayout_20.addWidget(self.groupBox)

        self.stackedWidget.addWidget(self.onnx_page)

        self.verticalLayout_19.addWidget(self.stackedWidget)

        self.tabWidget.addTab(self.TextToSpeechSetting, "")
        self.TranslationSettings = QWidget()
        self.TranslationSettings.setObjectName(u"TranslationSettings")
        self.verticalLayout_15 = QVBoxLayout(self.TranslationSettings)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.checkBox_translate = QCheckBox(self.TranslationSettings)
        self.checkBox_translate.setObjectName(u"checkBox_translate")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkBox_translate.sizePolicy().hasHeightForWidth())
        self.checkBox_translate.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setBold(True)
        self.checkBox_translate.setFont(font1)
        self.checkBox_translate.setChecked(True)

        self.verticalLayout_15.addWidget(self.checkBox_translate)

        self.groupBox_translate = QGroupBox(self.TranslationSettings)
        self.groupBox_translate.setObjectName(u"groupBox_translate")
        sizePolicy3.setHeightForWidth(self.groupBox_translate.sizePolicy().hasHeightForWidth())
        self.groupBox_translate.setSizePolicy(sizePolicy3)
        self.groupBox_translate.setFont(font1)
        self.groupBox_translate.setAlignment(Qt.AlignCenter)
        self.groupBox_translate.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_translate)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.groupBox_translate)
        self.label_2.setObjectName(u"label_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setBold(False)
        self.label_2.setFont(font2)

        self.gridLayout_2.addWidget(self.label_2, 6, 0, 1, 1)

        self.comboBox_writeLang = QComboBox(self.groupBox_translate)
        self.comboBox_writeLang.setObjectName(u"comboBox_writeLang")
        self.comboBox_writeLang.setFont(font2)

        self.gridLayout_2.addWidget(self.comboBox_writeLang, 5, 1, 1, 1)

        self.stackedWidget_provider = QStackedWidget(self.groupBox_translate)
        self.stackedWidget_provider.setObjectName(u"stackedWidget_provider")
        self.stackedWidget_provider.setFont(font2)
        self.mymemory = QWidget()
        self.mymemory.setObjectName(u"mymemory")
        self.verticalLayout_2 = QVBoxLayout(self.mymemory)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.mymemory_secret_key = QLineEdit(self.mymemory)
        self.mymemory_secret_key.setObjectName(u"mymemory_secret_key")
        self.mymemory_secret_key.setAlignment(Qt.AlignCenter)
        self.mymemory_secret_key.setReadOnly(False)

        self.verticalLayout_2.addWidget(self.mymemory_secret_key)

        self.email_mymemory = QLineEdit(self.mymemory)
        self.email_mymemory.setObjectName(u"email_mymemory")
        self.email_mymemory.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.email_mymemory)

        self.stackedWidget_provider.addWidget(self.mymemory)
        self.deepl = QWidget()
        self.deepl.setObjectName(u"deepl")
        self.verticalLayout_5 = QVBoxLayout(self.deepl)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.deepl_secret_key = QLineEdit(self.deepl)
        self.deepl_secret_key.setObjectName(u"deepl_secret_key")
        self.deepl_secret_key.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.deepl_secret_key)

        self.checkBox_pro = QCheckBox(self.deepl)
        self.checkBox_pro.setObjectName(u"checkBox_pro")

        self.verticalLayout_5.addWidget(self.checkBox_pro)

        self.stackedWidget_provider.addWidget(self.deepl)
        self.microsoft = QWidget()
        self.microsoft.setObjectName(u"microsoft")
        self.verticalLayout_6 = QVBoxLayout(self.microsoft)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.microsoft_secret_key = QLineEdit(self.microsoft)
        self.microsoft_secret_key.setObjectName(u"microsoft_secret_key")
        self.microsoft_secret_key.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.microsoft_secret_key)

        self.microsoft_region = QLineEdit(self.microsoft)
        self.microsoft_region.setObjectName(u"microsoft_region")
        self.microsoft_region.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.microsoft_region)

        self.stackedWidget_provider.addWidget(self.microsoft)
        self.libretranslate = QWidget()
        self.libretranslate.setObjectName(u"libretranslate")
        self.verticalLayout_4 = QVBoxLayout(self.libretranslate)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.LibreTranslate_secret_key = QLineEdit(self.libretranslate)
        self.LibreTranslate_secret_key.setObjectName(u"LibreTranslate_secret_key")
        self.LibreTranslate_secret_key.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.LibreTranslate_secret_key)

        self.LibreTranslate_url = QLineEdit(self.libretranslate)
        self.LibreTranslate_url.setObjectName(u"LibreTranslate_url")
        self.LibreTranslate_url.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.LibreTranslate_url)

        self.stackedWidget_provider.addWidget(self.libretranslate)
        self.google = QWidget()
        self.google.setObjectName(u"google")
        self.verticalLayout = QVBoxLayout(self.google)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget_provider.addWidget(self.google)
        self.linguee = QWidget()
        self.linguee.setObjectName(u"linguee")
        self.formLayout = QFormLayout(self.linguee)
        self.formLayout.setObjectName(u"formLayout")
        self.stackedWidget_provider.addWidget(self.linguee)
        self.yandex = QWidget()
        self.yandex.setObjectName(u"yandex")
        self.verticalLayout_14 = QVBoxLayout(self.yandex)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.yandex_secret_key = QLineEdit(self.yandex)
        self.yandex_secret_key.setObjectName(u"yandex_secret_key")
        self.yandex_secret_key.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.yandex_secret_key)

        self.stackedWidget_provider.addWidget(self.yandex)
        self.pons = QWidget()
        self.pons.setObjectName(u"pons")
        self.stackedWidget_provider.addWidget(self.pons)
        self.papago = QWidget()
        self.papago.setObjectName(u"papago")
        self.verticalLayout_9 = QVBoxLayout(self.papago)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.papago_client_id = QLineEdit(self.papago)
        self.papago_client_id.setObjectName(u"papago_client_id")
        self.papago_client_id.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.papago_client_id)

        self.papago_secret_key = QLineEdit(self.papago)
        self.papago_secret_key.setObjectName(u"papago_secret_key")
        self.papago_secret_key.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.papago_secret_key)

        self.stackedWidget_provider.addWidget(self.papago)
        self.qcri = QWidget()
        self.qcri.setObjectName(u"qcri")
        self.verticalLayout_3 = QVBoxLayout(self.qcri)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.qcri_secret_key = QLineEdit(self.qcri)
        self.qcri_secret_key.setObjectName(u"qcri_secret_key")
        self.qcri_secret_key.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.qcri_secret_key)

        self.stackedWidget_provider.addWidget(self.qcri)
        self.baidu = QWidget()
        self.baidu.setObjectName(u"baidu")
        self.verticalLayout_16 = QVBoxLayout(self.baidu)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.baidu_appid = QLineEdit(self.baidu)
        self.baidu_appid.setObjectName(u"baidu_appid")
        self.baidu_appid.setAlignment(Qt.AlignCenter)

        self.verticalLayout_16.addWidget(self.baidu_appid)

        self.baidu_secret_key = QLineEdit(self.baidu)
        self.baidu_secret_key.setObjectName(u"baidu_secret_key")
        self.baidu_secret_key.setAlignment(Qt.AlignCenter)

        self.verticalLayout_16.addWidget(self.baidu_secret_key)

        self.stackedWidget_provider.addWidget(self.baidu)

        self.gridLayout_2.addWidget(self.stackedWidget_provider, 7, 0, 1, 2)

        self.comboBox_provider = QComboBox(self.groupBox_translate)
        self.comboBox_provider.setObjectName(u"comboBox_provider")
        self.comboBox_provider.setFont(font2)

        self.gridLayout_2.addWidget(self.comboBox_provider, 3, 1, 1, 1)

        self.label_14 = QLabel(self.groupBox_translate)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font2)

        self.gridLayout_2.addWidget(self.label_14, 3, 0, 1, 1)

        self.label = QLabel(self.groupBox_translate)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)

        self.gridLayout_2.addWidget(self.label, 5, 0, 1, 1)

        self.comboBox_targetLang = QComboBox(self.groupBox_translate)
        self.comboBox_targetLang.setObjectName(u"comboBox_targetLang")
        sizePolicy3.setHeightForWidth(self.comboBox_targetLang.sizePolicy().hasHeightForWidth())
        self.comboBox_targetLang.setSizePolicy(sizePolicy3)
        self.comboBox_targetLang.setFont(font2)

        self.gridLayout_2.addWidget(self.comboBox_targetLang, 6, 1, 1, 1)

        self.checkBox_overwritepb = QCheckBox(self.groupBox_translate)
        self.checkBox_overwritepb.setObjectName(u"checkBox_overwritepb")
        sizePolicy3.setHeightForWidth(self.checkBox_overwritepb.sizePolicy().hasHeightForWidth())
        self.checkBox_overwritepb.setSizePolicy(sizePolicy3)
        self.checkBox_overwritepb.setFont(font2)
        self.checkBox_overwritepb.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_overwritepb, 1, 0, 1, 1)

        self.bypass_tts_checkBox = QCheckBox(self.groupBox_translate)
        self.bypass_tts_checkBox.setObjectName(u"bypass_tts_checkBox")
        self.bypass_tts_checkBox.setFont(font2)

        self.gridLayout_2.addWidget(self.bypass_tts_checkBox, 2, 0, 1, 1)


        self.verticalLayout_15.addWidget(self.groupBox_translate)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer_6)

        self.tabWidget.addTab(self.TranslationSettings, "")
        self.ApplicationSettings = QWidget()
        self.ApplicationSettings.setObjectName(u"ApplicationSettings")
        self.gridLayout_9 = QGridLayout(self.ApplicationSettings)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_15 = QLabel(self.ApplicationSettings)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font2)

        self.gridLayout_9.addWidget(self.label_15, 1, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_5, 1, 4, 1, 1)

        self.spinBox_threshold = QSpinBox(self.ApplicationSettings)
        self.spinBox_threshold.setObjectName(u"spinBox_threshold")
        self.spinBox_threshold.setFont(font2)
        self.spinBox_threshold.setMinimum(1)
        self.spinBox_threshold.setStepType(QAbstractSpinBox.DefaultStepType)
        self.spinBox_threshold.setValue(7)

        self.gridLayout_9.addWidget(self.spinBox_threshold, 1, 1, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_5, 6, 1, 1, 1)

        self.frame = QFrame(self.ApplicationSettings)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clear_cache = QPushButton(self.frame)
        self.clear_cache.setObjectName(u"clear_cache")

        self.horizontalLayout.addWidget(self.clear_cache)

        self.open_cache = QPushButton(self.frame)
        self.open_cache.setObjectName(u"open_cache")

        self.horizontalLayout.addWidget(self.open_cache)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.gridLayout_9.addWidget(self.frame, 4, 0, 1, 2)

        self.checkBox_stats = QCheckBox(self.ApplicationSettings)
        self.checkBox_stats.setObjectName(u"checkBox_stats")
        self.checkBox_stats.setFont(font2)
        self.checkBox_stats.setChecked(True)

        self.gridLayout_9.addWidget(self.checkBox_stats, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(30, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_3, 3, 4, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_7, 1, 3, 1, 1)

        self.frame_2 = QFrame(self.ApplicationSettings)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy5)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_2.addWidget(self.label_11)

        self.appPath = QLineEdit(self.frame_2)
        self.appPath.setObjectName(u"appPath")
        sizePolicy2.setHeightForWidth(self.appPath.sizePolicy().hasHeightForWidth())
        self.appPath.setSizePolicy(sizePolicy2)
        self.appPath.setMinimumSize(QSize(300, 0))
        self.appPath.setMaximumSize(QSize(350, 16777215))

        self.horizontalLayout_2.addWidget(self.appPath)

        self.copyApp = QPushButton(self.frame_2)
        self.copyApp.setObjectName(u"copyApp")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.copyApp.sizePolicy().hasHeightForWidth())
        self.copyApp.setSizePolicy(sizePolicy6)

        self.horizontalLayout_2.addWidget(self.copyApp)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.gridLayout_9.addWidget(self.frame_2, 3, 0, 1, 4)

        self.tabWidget.addTab(self.ApplicationSettings, "")
        self.AdvancedSettings = QWidget()
        self.AdvancedSettings.setObjectName(u"AdvancedSettings")
        self.verticalLayout_21 = QVBoxLayout(self.AdvancedSettings)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.scrollArea = QScrollArea(self.AdvancedSettings)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 773, 503))
        self.verticalLayout_23 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 120))
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.onnx_cache = QLineEdit(self.groupBox_4)
        self.onnx_cache.setObjectName(u"onnx_cache")

        self.horizontalLayout_4.addWidget(self.onnx_cache)

        self.cache_pushButton = QPushButton(self.groupBox_4)
        self.cache_pushButton.setObjectName(u"cache_pushButton")

        self.horizontalLayout_4.addWidget(self.cache_pushButton)


        self.verticalLayout_22.addLayout(self.horizontalLayout_4)

        self.onnx_checkBox = QCheckBox(self.groupBox_4)
        self.onnx_checkBox.setObjectName(u"onnx_checkBox")

        self.verticalLayout_22.addWidget(self.onnx_checkBox)


        self.verticalLayout_23.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(16777215, 150))
        self.verticalLayout_24 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")
        font3 = QFont()
        font3.setPointSize(10)
        self.label_9.setFont(font3)

        self.horizontalLayout_5.addWidget(self.label_9)

        self.lineEdit_key = QLineEdit(self.groupBox_5)
        self.lineEdit_key.setObjectName(u"lineEdit_key")

        self.horizontalLayout_5.addWidget(self.lineEdit_key)


        self.verticalLayout_24.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font3)

        self.horizontalLayout_6.addWidget(self.label_10)

        self.lineEdit_region = QLineEdit(self.groupBox_5)
        self.lineEdit_region.setObjectName(u"lineEdit_region")

        self.horizontalLayout_6.addWidget(self.lineEdit_region)


        self.verticalLayout_24.addLayout(self.horizontalLayout_6)

        self.checkBox_saveAudio = QCheckBox(self.groupBox_5)
        self.checkBox_saveAudio.setObjectName(u"checkBox_saveAudio")
        self.checkBox_saveAudio.setFont(font3)
        self.checkBox_saveAudio.setChecked(True)

        self.verticalLayout_24.addWidget(self.checkBox_saveAudio)


        self.verticalLayout_23.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMaximumSize(QSize(16777215, 120))
        self.verticalLayout_25 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_6 = QLabel(self.groupBox_6)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font3)

        self.verticalLayout_25.addWidget(self.label_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.credsFilePathEdit = QLineEdit(self.groupBox_6)
        self.credsFilePathEdit.setObjectName(u"credsFilePathEdit")
        self.credsFilePathEdit.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"min-width: 10em;\n"
"padding: 6px;")

        self.horizontalLayout_8.addWidget(self.credsFilePathEdit)

        self.browseButton = QPushButton(self.groupBox_6)
        self.browseButton.setObjectName(u"browseButton")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.browseButton.sizePolicy().hasHeightForWidth())
        self.browseButton.setSizePolicy(sizePolicy7)

        self.horizontalLayout_8.addWidget(self.browseButton)


        self.verticalLayout_25.addLayout(self.horizontalLayout_8)

        self.checkBox_saveAudio_gTTS = QCheckBox(self.groupBox_6)
        self.checkBox_saveAudio_gTTS.setObjectName(u"checkBox_saveAudio_gTTS")
        self.checkBox_saveAudio_gTTS.setChecked(True)

        self.verticalLayout_25.addWidget(self.checkBox_saveAudio_gTTS)


        self.verticalLayout_23.addWidget(self.groupBox_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_21.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.AdvancedSettings, "")

        self.verticalLayout_18.addWidget(self.tabWidget)

        self.statusBar = QLabel(Widget)
        self.statusBar.setObjectName(u"statusBar")

        self.verticalLayout_18.addWidget(self.statusBar)

        self.buttonBox = QDialogButtonBox(Widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setInputMethodHints(Qt.ImhPreferUppercase)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_18.addWidget(self.buttonBox)


        self.retranslateUi(Widget)
        self.checkBox_translate.clicked["bool"].connect(self.groupBox_translate.setEnabled)

        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_provider.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Configure TranslateAndTTS", None))
        self.ttsEngineBox.setItemText(0, QCoreApplication.translate("Widget", u"Sherpa-ONNX", None))
        self.ttsEngineBox.setItemText(1, QCoreApplication.translate("Widget", u"Azure TTS", None))
        self.ttsEngineBox.setItemText(2, QCoreApplication.translate("Widget", u"Google TTS", None))
        self.ttsEngineBox.setItemText(3, QCoreApplication.translate("Widget", u"GSpeak", None))
        self.ttsEngineBox.setItemText(4, QCoreApplication.translate("Widget", u"Sapi5 (Windows)", None))
        self.ttsEngineBox.setItemText(5, QCoreApplication.translate("Widget", u"NSS (Mac Only)", None))
        self.ttsEngineBox.setItemText(6, QCoreApplication.translate("Widget", u"coqui_ai_tts (Unsupported)", None))
        self.ttsEngineBox.setItemText(7, QCoreApplication.translate("Widget", u"espeak (Unsupported)", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Voices Models", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"Voice Models", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Neue Montreal','Helvetica Neue','Helvetica','Arial','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'; font-size:10pt; color:#001e00; background-color:#f5f6f7;\">Note: </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Neue M"
                        "ontreal','Helvetica Neue','Helvetica','Arial','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'; font-size:10pt; color:#001e00; background-color:#f5f6f7;\">1. Not all voices available. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Neue Montreal','Helvetica Neue','Helvetica','Arial','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'; font-size:10pt; color:#001e00; background-color:#f5f6f7;\">2. Voice is chosen by default based on Target Lang</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"Rate:", None))
#if QT_CONFIG(tooltip)
        self.label_12.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">VoiceID. To find what this would be run the programme with --listvoices</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("Widget", u"Voice ID:", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"Volume:", None))
        self.checkBox_saveAudio_sapi.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.checkBox_saveAudio_kurdish.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.checkBox_latin.setText(QCoreApplication.translate("Widget", u"Latin", None))
        self.checkBox_punctuation.setText(QCoreApplication.translate("Widget", u"Punctuation", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Volume:", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Rate:", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">VoiceID. To find what this would be run the programme with --listvoices</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Widget", u"Voice ID:", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"Voices", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TextToSpeechSetting), QCoreApplication.translate("Widget", u"Tab 1", None))
#if QT_CONFIG(tooltip)
        self.checkBox_translate.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Uncheck this option If you just want it to speak in the text you are writing</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_translate.setText(QCoreApplication.translate("Widget", u"Translate", None))
        self.groupBox_translate.setTitle(QCoreApplication.translate("Widget", u"Translate Settings", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Widget", u"Target Language for Translattion", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Widget", u"Target Language", None))
        self.mymemory_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u"MyMemory's secret access key", None))
#if QT_CONFIG(tooltip)
        self.email_mymemory.setToolTip(QCoreApplication.translate("Widget", u"Valid email allows 50000 chars/day.", None))
#endif // QT_CONFIG(tooltip)
        self.email_mymemory.setPlaceholderText(QCoreApplication.translate("Widget", u"Optional Email Address", None))
        self.deepl_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u"DeepL's secret access key", None))
        self.checkBox_pro.setText(QCoreApplication.translate("Widget", u"DeepL Pro", None))
        self.microsoft_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u"Microsoft's secret access key", None))
        self.microsoft_region.setPlaceholderText(QCoreApplication.translate("Widget", u"Region", None))
        self.LibreTranslate_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u" LibreTranslate's secret access key", None))
#if QT_CONFIG(tooltip)
        self.LibreTranslate_url.setToolTip(QCoreApplication.translate("Widget", u"Leave it for default value", None))
#endif // QT_CONFIG(tooltip)
        self.LibreTranslate_url.setPlaceholderText(QCoreApplication.translate("Widget", u"Url: https://translate.argosopentech.com/", None))
        self.yandex_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u"Yandex's Secret Access Key", None))
        self.papago_client_id.setPlaceholderText(QCoreApplication.translate("Widget", u"Client ID", None))
        self.papago_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u"Papago's Secret Access Key", None))
        self.qcri_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u"QCRI's secret access key", None))
        self.baidu_appid.setPlaceholderText(QCoreApplication.translate("Widget", u"Baidu Cloud App ID", None))
        self.baidu_secret_key.setPlaceholderText(QCoreApplication.translate("Widget", u"QCRI's secret access key", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"Provider", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Writing Language </span></pre><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Widget", u"Writing Language", None))
#if QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Do you want to overwrite the pasteboard with the new translated string?</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setText(QCoreApplication.translate("Widget", u"Overwrite Pasteboard", None))
        self.bypass_tts_checkBox.setText(QCoreApplication.translate("Widget", u"Bypass TTS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TranslationSettings), QCoreApplication.translate("Widget", u"Tab 2", None))
        self.label_15.setText(QCoreApplication.translate("Widget", u"Application Cache Threshold: ", None))
        self.spinBox_threshold.setSuffix(QCoreApplication.translate("Widget", u" day(s)", None))
        self.clear_cache.setText(QCoreApplication.translate("Widget", u"Clear Cache", None))
        self.open_cache.setText(QCoreApplication.translate("Widget", u"Open Cache", None))
        self.checkBox_stats.setText(QCoreApplication.translate("Widget", u"Allow The Application to Collecting Stats", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"Application Path: ", None))
        self.appPath.setText("")
        self.copyApp.setText(QCoreApplication.translate("Widget", u"Copy Path of Main app", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ApplicationSettings), QCoreApplication.translate("Widget", u"Page", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Widget", u"Sherpa ONNX", None))
        self.cache_pushButton.setText(QCoreApplication.translate("Widget", u"Open Cache", None))
        self.onnx_checkBox.setText(QCoreApplication.translate("Widget", u"Save Audio", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Widget", u"Azure TTS", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"Key:", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"Region:", None))
        self.checkBox_saveAudio.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Widget", u"gTTS", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Credentials File:", None))
        self.browseButton.setText(QCoreApplication.translate("Widget", u"Browse", None))
        self.checkBox_saveAudio_gTTS.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AdvancedSettings), QCoreApplication.translate("Widget", u"Page", None))
        self.statusBar.setText("")
    # retranslateUi

