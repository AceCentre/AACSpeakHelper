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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialogButtonBox, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QStackedWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(854, 553)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.azure_page = QWidget()
        self.azure_page.setObjectName(u"azure_page")
        self.formLayoutWidget_4 = QWidget(self.azure_page)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(0, 30, 441, 391))
        self.gridLayout_4 = QGridLayout(self.formLayoutWidget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.checkBox_saveAudio = QCheckBox(self.formLayoutWidget_4)
        self.checkBox_saveAudio.setObjectName(u"checkBox_saveAudio")
        self.checkBox_saveAudio.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_saveAudio, 2, 1, 1, 1)

        self.listWidget_voiceazure = QListWidget(self.formLayoutWidget_4)
        self.listWidget_voiceazure.setObjectName(u"listWidget_voiceazure")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget_voiceazure.sizePolicy().hasHeightForWidth())
        self.listWidget_voiceazure.setSizePolicy(sizePolicy1)
        self.listWidget_voiceazure.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.listWidget_voiceazure.setSortingEnabled(True)

        self.gridLayout_4.addWidget(self.listWidget_voiceazure, 3, 1, 1, 1)

        self.label_9 = QLabel(self.formLayoutWidget_4)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_10 = QLabel(self.formLayoutWidget_4)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)

        self.lineEdit_region = QLineEdit(self.formLayoutWidget_4)
        self.lineEdit_region.setObjectName(u"lineEdit_region")

        self.gridLayout_4.addWidget(self.lineEdit_region, 1, 1, 1, 1)

        self.label_11 = QLabel(self.formLayoutWidget_4)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 3, 0, 1, 1)

        self.lineEdit_key = QLineEdit(self.formLayoutWidget_4)
        self.lineEdit_key.setObjectName(u"lineEdit_key")

        self.gridLayout_4.addWidget(self.lineEdit_key, 0, 1, 1, 1)

        self.stackedWidget.addWidget(self.azure_page)
        self.gTTS_page = QWidget()
        self.gTTS_page.setObjectName(u"gTTS_page")
        self.gridLayoutWidget_2 = QWidget(self.gTTS_page)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(4, 29, 471, 411))
        self.gridLayout_6 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.credsFilePathEdit = QLineEdit(self.gridLayoutWidget_2)
        self.credsFilePathEdit.setObjectName(u"credsFilePathEdit")

        self.gridLayout_6.addWidget(self.credsFilePathEdit, 0, 1, 1, 1)

        self.browseButton = QPushButton(self.gridLayoutWidget_2)
        self.browseButton.setObjectName(u"browseButton")

        self.gridLayout_6.addWidget(self.browseButton, 0, 2, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_6.addWidget(self.label_13, 3, 0, 1, 1)

        self.listWidget_voicegoogle = QListWidget(self.gridLayoutWidget_2)
        self.listWidget_voicegoogle.setObjectName(u"listWidget_voicegoogle")

        self.gridLayout_6.addWidget(self.listWidget_voicegoogle, 3, 1, 1, 2)

        self.checkBox_saveAudio_gTTS = QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_saveAudio_gTTS.setObjectName(u"checkBox_saveAudio_gTTS")
        self.checkBox_saveAudio_gTTS.setChecked(True)

        self.gridLayout_6.addWidget(self.checkBox_saveAudio_gTTS, 2, 1, 1, 2)

        self.stackedWidget.addWidget(self.gTTS_page)
        self.gspeak_page = QWidget()
        self.gspeak_page.setObjectName(u"gspeak_page")
        self.gridLayoutWidget = QWidget(self.gspeak_page)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(-1, 29, 471, 87))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.gridLayoutWidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setAutoFillBackground(True)

        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.gspeak_page)
        self.sapi_page = QWidget()
        self.sapi_page.setObjectName(u"sapi_page")
        self.formLayoutWidget_2 = QWidget(self.sapi_page)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(0, 33, 471, 411))
        self.gridLayout_8 = QGridLayout(self.formLayoutWidget_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_8.addWidget(self.label_8, 1, 0, 1, 1)

        self.listWidget_sapi = QListWidget(self.formLayoutWidget_2)
        self.listWidget_sapi.setObjectName(u"listWidget_sapi")

        self.gridLayout_8.addWidget(self.listWidget_sapi, 3, 1, 1, 1)

        self.horizontalSlider_rate_sapi = QSlider(self.formLayoutWidget_2)
        self.horizontalSlider_rate_sapi.setObjectName(u"horizontalSlider_rate_sapi")
        self.horizontalSlider_rate_sapi.setMaximum(100)
        self.horizontalSlider_rate_sapi.setValue(100)
        self.horizontalSlider_rate_sapi.setOrientation(Qt.Horizontal)

        self.gridLayout_8.addWidget(self.horizontalSlider_rate_sapi, 1, 1, 1, 1)

        self.label_12 = QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_8.addWidget(self.label_12, 3, 0, 1, 1)

        self.horizontalSlider_volume_sapi = QSlider(self.formLayoutWidget_2)
        self.horizontalSlider_volume_sapi.setObjectName(u"horizontalSlider_volume_sapi")
        self.horizontalSlider_volume_sapi.setMaximum(100)
        self.horizontalSlider_volume_sapi.setValue(100)
        self.horizontalSlider_volume_sapi.setOrientation(Qt.Horizontal)

        self.gridLayout_8.addWidget(self.horizontalSlider_volume_sapi, 0, 1, 1, 1)

        self.label_7 = QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_8.addWidget(self.label_7, 0, 0, 1, 1)

        self.checkBox_saveAudio_sapi = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_saveAudio_sapi.setObjectName(u"checkBox_saveAudio_sapi")
        self.checkBox_saveAudio_sapi.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_saveAudio_sapi, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.sapi_page)
        self.kurdish_page = QWidget()
        self.kurdish_page.setObjectName(u"kurdish_page")
        self.gridLayoutWidget_3 = QWidget(self.kurdish_page)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(9, 29, 461, 94))
        self.gridLayout_7 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.checkBox_saveAudio_kurdish = QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_saveAudio_kurdish.setObjectName(u"checkBox_saveAudio_kurdish")
        self.checkBox_saveAudio_kurdish.setChecked(True)

        self.gridLayout_7.addWidget(self.checkBox_saveAudio_kurdish, 0, 0, 1, 1)

        self.checkBox_latin = QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_latin.setObjectName(u"checkBox_latin")
        self.checkBox_latin.setChecked(True)

        self.gridLayout_7.addWidget(self.checkBox_latin, 1, 0, 1, 1)

        self.checkBox_punctuation = QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_punctuation.setObjectName(u"checkBox_punctuation")
        self.checkBox_punctuation.setChecked(False)

        self.gridLayout_7.addWidget(self.checkBox_punctuation, 2, 0, 1, 1)

        self.stackedWidget.addWidget(self.kurdish_page)
        self.ttsPage = QWidget()
        self.ttsPage.setObjectName(u"ttsPage")
        self.formLayoutWidget = QWidget(self.ttsPage)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(0, 30, 441, 84))
        self.gridLayout_5 = QGridLayout(self.formLayoutWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalSlider_volume = QSlider(self.formLayoutWidget)
        self.horizontalSlider_volume.setObjectName(u"horizontalSlider_volume")
        self.horizontalSlider_volume.setMaximum(100)
        self.horizontalSlider_volume.setValue(100)
        self.horizontalSlider_volume.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.horizontalSlider_volume, 0, 1, 1, 1)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)

        self.horizontalSlider_rate = QSlider(self.formLayoutWidget)
        self.horizontalSlider_rate.setObjectName(u"horizontalSlider_rate")
        self.horizontalSlider_rate.setMaximum(100)
        self.horizontalSlider_rate.setValue(100)
        self.horizontalSlider_rate.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.horizontalSlider_rate, 1, 1, 1, 1)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 2, 0, 1, 1)

        self.lineEdit_voiceID = QLineEdit(self.formLayoutWidget)
        self.lineEdit_voiceID.setObjectName(u"lineEdit_voiceID")

        self.gridLayout_5.addWidget(self.lineEdit_voiceID, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.ttsPage)

        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 3, 1)

        self.groupBox_translate = QGroupBox(Widget)
        self.groupBox_translate.setObjectName(u"groupBox_translate")
        sizePolicy1.setHeightForWidth(self.groupBox_translate.sizePolicy().hasHeightForWidth())
        self.groupBox_translate.setSizePolicy(sizePolicy1)
        self.groupBox_translate.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_translate)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox_translate = QCheckBox(self.groupBox_translate)
        self.checkBox_translate.setObjectName(u"checkBox_translate")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.checkBox_translate.sizePolicy().hasHeightForWidth())
        self.checkBox_translate.setSizePolicy(sizePolicy2)
        self.checkBox_translate.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_translate, 0, 0, 1, 1)

        self.checkBox_overwritepb = QCheckBox(self.groupBox_translate)
        self.checkBox_overwritepb.setObjectName(u"checkBox_overwritepb")
        sizePolicy2.setHeightForWidth(self.checkBox_overwritepb.sizePolicy().hasHeightForWidth())
        self.checkBox_overwritepb.setSizePolicy(sizePolicy2)
        self.checkBox_overwritepb.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_overwritepb, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox_translate)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_translate)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 2, 0, 1, 1)

        self.comboBox_targetLang = QComboBox(self.groupBox_translate)
        self.comboBox_targetLang.setObjectName(u"comboBox_targetLang")
        sizePolicy2.setHeightForWidth(self.comboBox_targetLang.sizePolicy().hasHeightForWidth())
        self.comboBox_targetLang.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboBox_targetLang, 5, 1, 1, 1)

        self.comboBox_writeLang = QComboBox(self.groupBox_translate)
        self.comboBox_writeLang.setObjectName(u"comboBox_writeLang")

        self.gridLayout_2.addWidget(self.comboBox_writeLang, 4, 1, 1, 1)

        self.stackedWidget_provider = QStackedWidget(self.groupBox_translate)
        self.stackedWidget_provider.setObjectName(u"stackedWidget_provider")
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

        self.gridLayout_2.addWidget(self.stackedWidget_provider, 3, 0, 1, 2)

        self.label_2 = QLabel(self.groupBox_translate)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)

        self.comboBox_provider = QComboBox(self.groupBox_translate)
        self.comboBox_provider.setObjectName(u"comboBox_provider")

        self.gridLayout_2.addWidget(self.comboBox_provider, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_translate, 2, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setInputMethodHints(Qt.ImhPreferUppercase)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)

        self.groupBox_ttsEngine = QGroupBox(Widget)
        self.groupBox_ttsEngine.setObjectName(u"groupBox_ttsEngine")
        sizePolicy1.setHeightForWidth(self.groupBox_ttsEngine.sizePolicy().hasHeightForWidth())
        self.groupBox_ttsEngine.setSizePolicy(sizePolicy1)
        self.groupBox_ttsEngine.setFlat(False)
        self.groupBox_ttsEngine.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.groupBox_ttsEngine)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioButton_azure = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_azure.setObjectName(u"radioButton_azure")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.radioButton_azure.sizePolicy().hasHeightForWidth())
        self.radioButton_azure.setSizePolicy(sizePolicy4)
        self.radioButton_azure.setChecked(True)

        self.verticalLayout.addWidget(self.radioButton_azure)

        self.radioButton_google = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_google.setObjectName(u"radioButton_google")
        sizePolicy4.setHeightForWidth(self.radioButton_google.sizePolicy().hasHeightForWidth())
        self.radioButton_google.setSizePolicy(sizePolicy4)
        self.radioButton_google.setChecked(False)

        self.verticalLayout.addWidget(self.radioButton_google)

        self.radioButton_gspeak = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_gspeak.setObjectName(u"radioButton_gspeak")

        self.verticalLayout.addWidget(self.radioButton_gspeak)

        self.radioButton_sapi5 = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_sapi5.setObjectName(u"radioButton_sapi5")
        sizePolicy4.setHeightForWidth(self.radioButton_sapi5.sizePolicy().hasHeightForWidth())
        self.radioButton_sapi5.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.radioButton_sapi5)

        self.radioButton_nsss = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_nsss.setObjectName(u"radioButton_nsss")
        sizePolicy4.setHeightForWidth(self.radioButton_nsss.sizePolicy().hasHeightForWidth())
        self.radioButton_nsss.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.radioButton_nsss)

        self.radioButton_coqui = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_coqui.setObjectName(u"radioButton_coqui")
        self.radioButton_coqui.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.radioButton_coqui.sizePolicy().hasHeightForWidth())
        self.radioButton_coqui.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.radioButton_coqui)

        self.radioButton_espeak = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_espeak.setObjectName(u"radioButton_espeak")
        self.radioButton_espeak.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.radioButton_espeak.sizePolicy().hasHeightForWidth())
        self.radioButton_espeak.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.radioButton_espeak)

        self.radioButton_kurdish = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_kurdish.setObjectName(u"radioButton_kurdish")

        self.verticalLayout.addWidget(self.radioButton_kurdish)


        self.gridLayout.addWidget(self.groupBox_ttsEngine, 0, 0, 1, 1)

        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox_stats = QCheckBox(self.groupBox)
        self.checkBox_stats.setObjectName(u"checkBox_stats")
        self.checkBox_stats.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_stats)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        QWidget.setTabOrder(self.radioButton_azure, self.radioButton_google)
        QWidget.setTabOrder(self.radioButton_google, self.radioButton_sapi5)
        QWidget.setTabOrder(self.radioButton_sapi5, self.radioButton_nsss)
        QWidget.setTabOrder(self.radioButton_nsss, self.radioButton_espeak)
        QWidget.setTabOrder(self.radioButton_espeak, self.checkBox_translate)
        QWidget.setTabOrder(self.checkBox_translate, self.checkBox_overwritepb)
        QWidget.setTabOrder(self.checkBox_overwritepb, self.comboBox_writeLang)
        QWidget.setTabOrder(self.comboBox_writeLang, self.comboBox_targetLang)
        QWidget.setTabOrder(self.comboBox_targetLang, self.lineEdit_key)
        QWidget.setTabOrder(self.lineEdit_key, self.lineEdit_region)
        QWidget.setTabOrder(self.lineEdit_region, self.checkBox_saveAudio)
        QWidget.setTabOrder(self.checkBox_saveAudio, self.listWidget_voiceazure)
        QWidget.setTabOrder(self.listWidget_voiceazure, self.horizontalSlider_volume)
        QWidget.setTabOrder(self.horizontalSlider_volume, self.horizontalSlider_rate)
        QWidget.setTabOrder(self.horizontalSlider_rate, self.lineEdit_voiceID)

        self.retranslateUi(Widget)

        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_provider.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Configure TranslateAndTTS", None))
        self.checkBox_saveAudio.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"Key:", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"Region:", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"Voice Model:", None))
        self.browseButton.setText(QCoreApplication.translate("Widget", u"Browse", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Credentials File:", None))
        self.label_13.setText(QCoreApplication.translate("Widget", u"Voice Model:", None))
        self.checkBox_saveAudio_gTTS.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Neue Montreal','Helvetica Neue','Helvetica','Arial','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'; font-size:10pt; color:#001e00; background-color:#f5f6f7;\">Note: </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Neue Montreal','Helvetica Neue','Helvetica','Arial','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'; font-size:10pt; color:"
                        "#001e00; background-color:#f5f6f7;\">1. Not all voices available. </span></p>\n"
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
        self.groupBox_translate.setTitle(QCoreApplication.translate("Widget", u"Translate Settings", None))
#if QT_CONFIG(tooltip)
        self.checkBox_translate.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Uncheck this option If you just want it to speak in the text you are writing</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_translate.setText(QCoreApplication.translate("Widget", u"Translate", None))
#if QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Do you want to overwrite the pasteboard with the new translated string?</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setText(QCoreApplication.translate("Widget", u"Overwrite Pasteboard", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Writing Language </span></pre><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Widget", u"Writing Language", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"Provider", None))
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
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Widget", u"Target Language for Translattion", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Widget", u"Target Language", None))
        self.groupBox_ttsEngine.setTitle(QCoreApplication.translate("Widget", u"TTS Engine", None))
        self.radioButton_azure.setText(QCoreApplication.translate("Widget", u"Azure TTS", None))
        self.radioButton_google.setText(QCoreApplication.translate("Widget", u"Google TTS", None))
        self.radioButton_gspeak.setText(QCoreApplication.translate("Widget", u"GSpeak", None))
        self.radioButton_sapi5.setText(QCoreApplication.translate("Widget", u"Sapi5 (Windows)", None))
        self.radioButton_nsss.setText(QCoreApplication.translate("Widget", u"NSSS (Mac Only)", None))
        self.radioButton_coqui.setText(QCoreApplication.translate("Widget", u"coqui_ai_tts (Unsupported)", None))
        self.radioButton_espeak.setText(QCoreApplication.translate("Widget", u"espeak (Unsupported)", None))
        self.radioButton_kurdish.setText(QCoreApplication.translate("Widget", u"Kurdish TTS", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"App", None))
        self.checkBox_stats.setText(QCoreApplication.translate("Widget", u"Allow Collecting Stats", None))
    # retranslateUi

