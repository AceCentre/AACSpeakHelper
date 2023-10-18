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
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QStackedWidget, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(588, 400)
        icon = QIcon()
        icon.addFile(u":/images/images/configure.ico", QSize(), QIcon.Normal, QIcon.Off)
        Widget.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.buttonBox = QDialogButtonBox(Widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setInputMethodHints(Qt.ImhPreferUppercase)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)

        self.statusBar = QLabel(Widget)
        self.statusBar.setObjectName(u"statusBar")

        self.gridLayout.addWidget(self.statusBar, 4, 2, 1, 1)

        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.TextToSpeechSetting = QWidget()
        self.TextToSpeechSetting.setObjectName(u"TextToSpeechSetting")
        self.gridLayout_12 = QGridLayout(self.TextToSpeechSetting)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
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

        self.gridLayout_12.addWidget(self.ttsEngineBox, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer, 0, 1, 1, 1)

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
        self.label_9 = QLabel(self.formWidget_4)
        self.label_9.setObjectName(u"label_9")
        font = QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.checkBox_saveAudio = QCheckBox(self.formWidget_4)
        self.checkBox_saveAudio.setObjectName(u"checkBox_saveAudio")
        self.checkBox_saveAudio.setFont(font)
        self.checkBox_saveAudio.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_saveAudio, 2, 1, 1, 1)

        self.lineEdit_region = QLineEdit(self.formWidget_4)
        self.lineEdit_region.setObjectName(u"lineEdit_region")

        self.gridLayout_4.addWidget(self.lineEdit_region, 1, 1, 1, 1)

        self.label_10 = QLabel(self.formWidget_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)

        self.lineEdit_key = QLineEdit(self.formWidget_4)
        self.lineEdit_key.setObjectName(u"lineEdit_key")

        self.gridLayout_4.addWidget(self.lineEdit_key, 0, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.formWidget_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.groupBox_2.setFont(font1)
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


        self.gridLayout_4.addWidget(self.groupBox_2, 3, 0, 1, 2)


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
        self.label_6 = QLabel(self.gridWidget_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)

        self.browseButton = QPushButton(self.gridWidget_2)
        self.browseButton.setObjectName(u"browseButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.browseButton.sizePolicy().hasHeightForWidth())
        self.browseButton.setSizePolicy(sizePolicy2)

        self.gridLayout_6.addWidget(self.browseButton, 0, 2, 1, 1)

        self.credsFilePathEdit = QLineEdit(self.gridWidget_2)
        self.credsFilePathEdit.setObjectName(u"credsFilePathEdit")
        self.credsFilePathEdit.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"min-width: 10em;\n"
"padding: 6px;")

        self.gridLayout_6.addWidget(self.credsFilePathEdit, 0, 1, 1, 1)

        self.checkBox_saveAudio_gTTS = QCheckBox(self.gridWidget_2)
        self.checkBox_saveAudio_gTTS.setObjectName(u"checkBox_saveAudio_gTTS")
        self.checkBox_saveAudio_gTTS.setChecked(True)

        self.gridLayout_6.addWidget(self.checkBox_saveAudio_gTTS, 2, 1, 1, 2)

        self.groupBox_3 = QGroupBox(self.gridWidget_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)
        self.groupBox_3.setAlignment(Qt.AlignCenter)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.listWidget_voicegoogle = QListWidget(self.groupBox_3)
        self.listWidget_voicegoogle.setObjectName(u"listWidget_voicegoogle")
        self.listWidget_voicegoogle.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.listWidget_voicegoogle.setSortingEnabled(True)

        self.verticalLayout_8.addWidget(self.listWidget_voicegoogle)


        self.gridLayout_6.addWidget(self.groupBox_3, 3, 0, 1, 3)


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
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy3)
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

        self.gridLayout_12.addWidget(self.stackedWidget, 2, 0, 1, 2)

        self.tabWidget.addTab(self.TextToSpeechSetting, "")
        self.TranslationSettings = QWidget()
        self.TranslationSettings.setObjectName(u"TranslationSettings")
        self.verticalLayout_15 = QVBoxLayout(self.TranslationSettings)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.checkBox_translate = QCheckBox(self.TranslationSettings)
        self.checkBox_translate.setObjectName(u"checkBox_translate")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.checkBox_translate.sizePolicy().hasHeightForWidth())
        self.checkBox_translate.setSizePolicy(sizePolicy4)
        font2 = QFont()
        font2.setBold(True)
        self.checkBox_translate.setFont(font2)
        self.checkBox_translate.setChecked(True)

        self.verticalLayout_15.addWidget(self.checkBox_translate)

        self.groupBox_translate = QGroupBox(self.TranslationSettings)
        self.groupBox_translate.setObjectName(u"groupBox_translate")
        sizePolicy4.setHeightForWidth(self.groupBox_translate.sizePolicy().hasHeightForWidth())
        self.groupBox_translate.setSizePolicy(sizePolicy4)
        self.groupBox_translate.setFont(font2)
        self.groupBox_translate.setAlignment(Qt.AlignCenter)
        self.groupBox_translate.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_translate)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.groupBox_translate)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setBold(False)
        self.label.setFont(font3)

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_translate)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font3)

        self.gridLayout_2.addWidget(self.label_14, 2, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_translate)
        self.label_2.setObjectName(u"label_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)
        self.label_2.setFont(font3)

        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)

        self.comboBox_writeLang = QComboBox(self.groupBox_translate)
        self.comboBox_writeLang.setObjectName(u"comboBox_writeLang")
        self.comboBox_writeLang.setFont(font3)

        self.gridLayout_2.addWidget(self.comboBox_writeLang, 4, 1, 1, 1)

        self.comboBox_provider = QComboBox(self.groupBox_translate)
        self.comboBox_provider.setObjectName(u"comboBox_provider")
        self.comboBox_provider.setFont(font3)

        self.gridLayout_2.addWidget(self.comboBox_provider, 2, 1, 1, 1)

        self.comboBox_targetLang = QComboBox(self.groupBox_translate)
        self.comboBox_targetLang.setObjectName(u"comboBox_targetLang")
        sizePolicy4.setHeightForWidth(self.comboBox_targetLang.sizePolicy().hasHeightForWidth())
        self.comboBox_targetLang.setSizePolicy(sizePolicy4)
        self.comboBox_targetLang.setFont(font3)

        self.gridLayout_2.addWidget(self.comboBox_targetLang, 5, 1, 1, 1)

        self.checkBox_overwritepb = QCheckBox(self.groupBox_translate)
        self.checkBox_overwritepb.setObjectName(u"checkBox_overwritepb")
        sizePolicy4.setHeightForWidth(self.checkBox_overwritepb.sizePolicy().hasHeightForWidth())
        self.checkBox_overwritepb.setSizePolicy(sizePolicy4)
        self.checkBox_overwritepb.setFont(font3)
        self.checkBox_overwritepb.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_overwritepb, 1, 0, 1, 1)

        self.stackedWidget_provider = QStackedWidget(self.groupBox_translate)
        self.stackedWidget_provider.setObjectName(u"stackedWidget_provider")
        self.stackedWidget_provider.setFont(font3)
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

        self.gridLayout_2.addWidget(self.stackedWidget_provider, 6, 0, 1, 2)


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
        self.label_15.setFont(font3)

        self.gridLayout_9.addWidget(self.label_15, 1, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_5, 1, 4, 1, 1)

        self.spinBox_threshold = QSpinBox(self.ApplicationSettings)
        self.spinBox_threshold.setObjectName(u"spinBox_threshold")
        self.spinBox_threshold.setFont(font3)
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
        self.checkBox_stats.setFont(font3)
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
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy6)
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
        sizePolicy3.setHeightForWidth(self.appPath.sizePolicy().hasHeightForWidth())
        self.appPath.setSizePolicy(sizePolicy3)
        self.appPath.setMinimumSize(QSize(300, 0))
        self.appPath.setMaximumSize(QSize(350, 16777215))

        self.horizontalLayout_2.addWidget(self.appPath)

        self.copyApp = QPushButton(self.frame_2)
        self.copyApp.setObjectName(u"copyApp")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.copyApp.sizePolicy().hasHeightForWidth())
        self.copyApp.setSizePolicy(sizePolicy7)

        self.horizontalLayout_2.addWidget(self.copyApp)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.gridLayout_9.addWidget(self.frame_2, 3, 0, 1, 4)

        self.tabWidget.addTab(self.ApplicationSettings, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 3)


        self.retranslateUi(Widget)
        self.checkBox_translate.clicked["bool"].connect(self.groupBox_translate.setEnabled)

        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_provider.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Configure TranslateAndTTS", None))
        self.statusBar.setText("")
        self.ttsEngineBox.setItemText(0, QCoreApplication.translate("Widget", u"Azure TTS", None))
        self.ttsEngineBox.setItemText(1, QCoreApplication.translate("Widget", u"Google TTS", None))
        self.ttsEngineBox.setItemText(2, QCoreApplication.translate("Widget", u"GSpeak", None))
        self.ttsEngineBox.setItemText(3, QCoreApplication.translate("Widget", u"Sapi5 (Windows)", None))
        self.ttsEngineBox.setItemText(4, QCoreApplication.translate("Widget", u"NSS (Mac Only)", None))
        self.ttsEngineBox.setItemText(5, QCoreApplication.translate("Widget", u"coqui_ai_tts (Unsupported)", None))
        self.ttsEngineBox.setItemText(6, QCoreApplication.translate("Widget", u"espeak (Unsupported)", None))
        self.ttsEngineBox.setItemText(7, QCoreApplication.translate("Widget", u"Kurdish TTS", None))

        self.label_9.setText(QCoreApplication.translate("Widget", u"Key:", None))
        self.checkBox_saveAudio.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"Region:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Voices Models", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Credentials File:", None))
        self.browseButton.setText(QCoreApplication.translate("Widget", u"Browse", None))
        self.checkBox_saveAudio_gTTS.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"Voice Models", None))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TextToSpeechSetting), QCoreApplication.translate("Widget", u"Tab 1", None))
#if QT_CONFIG(tooltip)
        self.checkBox_translate.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Uncheck this option If you just want it to speak in the text you are writing</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_translate.setText(QCoreApplication.translate("Widget", u"Translate", None))
        self.groupBox_translate.setTitle(QCoreApplication.translate("Widget", u"Translate Settings", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Writing Language </span></pre><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Widget", u"Writing Language", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"Provider", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Widget", u"Target Language for Translattion", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Widget", u"Target Language", None))
#if QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Do you want to overwrite the pasteboard with the new translated string?</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setText(QCoreApplication.translate("Widget", u"Overwrite Pasteboard", None))
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
    # retranslateUi

