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
    QComboBox, QDialogButtonBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QSpinBox, QStackedWidget, QTextBrowser, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(854, 594)
        icon = QIcon()
        icon.addFile(u":/images/images/configure.ico", QSize(), QIcon.Normal, QIcon.Off)
        Widget.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_appCache = QGroupBox(Widget)
        self.groupBox_appCache.setObjectName(u"groupBox_appCache")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_appCache.sizePolicy().hasHeightForWidth())
        self.groupBox_appCache.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        self.groupBox_appCache.setFont(font)
        self.groupBox_appCache.setAlignment(Qt.AlignCenter)
        self.gridLayout_9 = QGridLayout(self.groupBox_appCache)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_15 = QLabel(self.groupBox_appCache)
        self.label_15.setObjectName(u"label_15")
        font1 = QFont()
        font1.setBold(False)
        self.label_15.setFont(font1)

        self.gridLayout_9.addWidget(self.label_15, 0, 0, 1, 1)

        self.spinBox_threshold = QSpinBox(self.groupBox_appCache)
        self.spinBox_threshold.setObjectName(u"spinBox_threshold")
        self.spinBox_threshold.setFont(font1)
        self.spinBox_threshold.setMinimum(1)
        self.spinBox_threshold.setStepType(QAbstractSpinBox.DefaultStepType)
        self.spinBox_threshold.setValue(7)

        self.gridLayout_9.addWidget(self.spinBox_threshold, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_appCache, 4, 0, 1, 1)

        self.groupBox_ttsEngine = QGroupBox(Widget)
        self.groupBox_ttsEngine.setObjectName(u"groupBox_ttsEngine")
        sizePolicy.setHeightForWidth(self.groupBox_ttsEngine.sizePolicy().hasHeightForWidth())
        self.groupBox_ttsEngine.setSizePolicy(sizePolicy)
        self.groupBox_ttsEngine.setFont(font)
        self.groupBox_ttsEngine.setAlignment(Qt.AlignCenter)
        self.groupBox_ttsEngine.setFlat(False)
        self.groupBox_ttsEngine.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.groupBox_ttsEngine)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioButton_azure = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_azure.setObjectName(u"radioButton_azure")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.radioButton_azure.sizePolicy().hasHeightForWidth())
        self.radioButton_azure.setSizePolicy(sizePolicy1)
        self.radioButton_azure.setFont(font1)
        self.radioButton_azure.setChecked(True)

        self.verticalLayout.addWidget(self.radioButton_azure)

        self.radioButton_google = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_google.setObjectName(u"radioButton_google")
        sizePolicy1.setHeightForWidth(self.radioButton_google.sizePolicy().hasHeightForWidth())
        self.radioButton_google.setSizePolicy(sizePolicy1)
        self.radioButton_google.setFont(font1)
        self.radioButton_google.setChecked(False)

        self.verticalLayout.addWidget(self.radioButton_google)

        self.radioButton_gspeak = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_gspeak.setObjectName(u"radioButton_gspeak")
        self.radioButton_gspeak.setFont(font1)

        self.verticalLayout.addWidget(self.radioButton_gspeak)

        self.radioButton_sapi5 = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_sapi5.setObjectName(u"radioButton_sapi5")
        sizePolicy1.setHeightForWidth(self.radioButton_sapi5.sizePolicy().hasHeightForWidth())
        self.radioButton_sapi5.setSizePolicy(sizePolicy1)
        self.radioButton_sapi5.setFont(font1)

        self.verticalLayout.addWidget(self.radioButton_sapi5)

        self.radioButton_nsss = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_nsss.setObjectName(u"radioButton_nsss")
        sizePolicy1.setHeightForWidth(self.radioButton_nsss.sizePolicy().hasHeightForWidth())
        self.radioButton_nsss.setSizePolicy(sizePolicy1)
        self.radioButton_nsss.setFont(font1)

        self.verticalLayout.addWidget(self.radioButton_nsss)

        self.radioButton_coqui = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_coqui.setObjectName(u"radioButton_coqui")
        self.radioButton_coqui.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.radioButton_coqui.sizePolicy().hasHeightForWidth())
        self.radioButton_coqui.setSizePolicy(sizePolicy1)
        self.radioButton_coqui.setFont(font1)

        self.verticalLayout.addWidget(self.radioButton_coqui)

        self.radioButton_espeak = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_espeak.setObjectName(u"radioButton_espeak")
        self.radioButton_espeak.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.radioButton_espeak.sizePolicy().hasHeightForWidth())
        self.radioButton_espeak.setSizePolicy(sizePolicy1)
        self.radioButton_espeak.setFont(font1)

        self.verticalLayout.addWidget(self.radioButton_espeak)

        self.radioButton_kurdish = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_kurdish.setObjectName(u"radioButton_kurdish")
        self.radioButton_kurdish.setFont(font1)

        self.verticalLayout.addWidget(self.radioButton_kurdish)


        self.gridLayout.addWidget(self.groupBox_ttsEngine, 0, 0, 1, 1)

        self.groupBox_translate = QGroupBox(Widget)
        self.groupBox_translate.setObjectName(u"groupBox_translate")
        sizePolicy.setHeightForWidth(self.groupBox_translate.sizePolicy().hasHeightForWidth())
        self.groupBox_translate.setSizePolicy(sizePolicy)
        self.groupBox_translate.setFont(font)
        self.groupBox_translate.setAlignment(Qt.AlignCenter)
        self.groupBox_translate.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_translate)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox_overwritepb = QCheckBox(self.groupBox_translate)
        self.checkBox_overwritepb.setObjectName(u"checkBox_overwritepb")
        sizePolicy.setHeightForWidth(self.checkBox_overwritepb.sizePolicy().hasHeightForWidth())
        self.checkBox_overwritepb.setSizePolicy(sizePolicy)
        self.checkBox_overwritepb.setFont(font1)
        self.checkBox_overwritepb.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_overwritepb, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox_translate)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_translate)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)

        self.gridLayout_2.addWidget(self.label_14, 2, 0, 1, 1)

        self.comboBox_targetLang = QComboBox(self.groupBox_translate)
        self.comboBox_targetLang.setObjectName(u"comboBox_targetLang")
        sizePolicy.setHeightForWidth(self.comboBox_targetLang.sizePolicy().hasHeightForWidth())
        self.comboBox_targetLang.setSizePolicy(sizePolicy)
        self.comboBox_targetLang.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_targetLang, 5, 1, 1, 1)

        self.comboBox_writeLang = QComboBox(self.groupBox_translate)
        self.comboBox_writeLang.setObjectName(u"comboBox_writeLang")
        self.comboBox_writeLang.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_writeLang, 4, 1, 1, 1)

        self.stackedWidget_provider = QStackedWidget(self.groupBox_translate)
        self.stackedWidget_provider.setObjectName(u"stackedWidget_provider")
        self.stackedWidget_provider.setFont(font1)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setFont(font1)

        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)

        self.comboBox_provider = QComboBox(self.groupBox_translate)
        self.comboBox_provider.setObjectName(u"comboBox_provider")
        self.comboBox_provider.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_provider, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_translate, 3, 0, 1, 1)

        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox_stats = QCheckBox(self.groupBox)
        self.checkBox_stats.setObjectName(u"checkBox_stats")
        self.checkBox_stats.setFont(font1)
        self.checkBox_stats.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_stats)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setInputMethodHints(Qt.ImhPreferUppercase)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)

        self.checkBox_translate = QCheckBox(Widget)
        self.checkBox_translate.setObjectName(u"checkBox_translate")
        sizePolicy.setHeightForWidth(self.checkBox_translate.sizePolicy().hasHeightForWidth())
        self.checkBox_translate.setSizePolicy(sizePolicy)
        self.checkBox_translate.setFont(font)
        self.checkBox_translate.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_translate, 2, 0, 1, 1)

        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy3)
        self.azure_page = QWidget()
        self.azure_page.setObjectName(u"azure_page")
        self.gridLayout_10 = QGridLayout(self.azure_page)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.formWidget_4 = QWidget(self.azure_page)
        self.formWidget_4.setObjectName(u"formWidget_4")
        self.gridLayout_4 = QGridLayout(self.formWidget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_9 = QLabel(self.formWidget_4)
        self.label_9.setObjectName(u"label_9")
        font2 = QFont()
        font2.setPointSize(10)
        self.label_9.setFont(font2)

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.checkBox_saveAudio = QCheckBox(self.formWidget_4)
        self.checkBox_saveAudio.setObjectName(u"checkBox_saveAudio")
        self.checkBox_saveAudio.setFont(font2)
        self.checkBox_saveAudio.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_saveAudio, 2, 1, 1, 1)

        self.lineEdit_region = QLineEdit(self.formWidget_4)
        self.lineEdit_region.setObjectName(u"lineEdit_region")
        self.lineEdit_region.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"min-width: 10em;\n"
"padding: 6px;")

        self.gridLayout_4.addWidget(self.lineEdit_region, 1, 1, 1, 1)

        self.label_10 = QLabel(self.formWidget_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font2)

        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)

        self.lineEdit_key = QLineEdit(self.formWidget_4)
        self.lineEdit_key.setObjectName(u"lineEdit_key")
        self.lineEdit_key.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"min-width: 10em;\n"
"padding: 6px;")

        self.gridLayout_4.addWidget(self.lineEdit_key, 0, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.formWidget_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.groupBox_2.setFont(font3)
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.search_azure = QLineEdit(self.groupBox_2)
        self.search_azure.setObjectName(u"search_azure")
        self.search_azure.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"min-width: 10em;\n"
"padding: 6px;")
        self.search_azure.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.search_azure)

        self.listWidget_voiceazure = QListWidget(self.groupBox_2)
        self.listWidget_voiceazure.setObjectName(u"listWidget_voiceazure")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.listWidget_voiceazure.sizePolicy().hasHeightForWidth())
        self.listWidget_voiceazure.setSizePolicy(sizePolicy4)
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
        self.gridWidget_2 = QWidget(self.gTTS_page)
        self.gridWidget_2.setObjectName(u"gridWidget_2")
        self.gridLayout_6 = QGridLayout(self.gridWidget_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_6 = QLabel(self.gridWidget_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)

        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)

        self.browseButton = QPushButton(self.gridWidget_2)
        self.browseButton.setObjectName(u"browseButton")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.browseButton.sizePolicy().hasHeightForWidth())
        self.browseButton.setSizePolicy(sizePolicy5)

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
        self.groupBox_3.setFont(font3)
        self.groupBox_3.setAlignment(Qt.AlignCenter)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.search_goggle = QLineEdit(self.groupBox_3)
        self.search_goggle.setObjectName(u"search_goggle")
        self.search_goggle.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"min-width: 10em;\n"
"padding: 6px;")

        self.verticalLayout_8.addWidget(self.search_goggle)

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

        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 5, 1)

        QWidget.setTabOrder(self.radioButton_azure, self.radioButton_google)
        QWidget.setTabOrder(self.radioButton_google, self.radioButton_sapi5)
        QWidget.setTabOrder(self.radioButton_sapi5, self.radioButton_nsss)
        QWidget.setTabOrder(self.radioButton_nsss, self.radioButton_espeak)
        QWidget.setTabOrder(self.radioButton_espeak, self.checkBox_overwritepb)
        QWidget.setTabOrder(self.checkBox_overwritepb, self.comboBox_writeLang)
        QWidget.setTabOrder(self.comboBox_writeLang, self.comboBox_targetLang)
        QWidget.setTabOrder(self.comboBox_targetLang, self.lineEdit_key)
        QWidget.setTabOrder(self.lineEdit_key, self.lineEdit_region)
        QWidget.setTabOrder(self.lineEdit_region, self.checkBox_saveAudio)
        QWidget.setTabOrder(self.checkBox_saveAudio, self.horizontalSlider_volume)
        QWidget.setTabOrder(self.horizontalSlider_volume, self.horizontalSlider_rate)
        QWidget.setTabOrder(self.horizontalSlider_rate, self.lineEdit_voiceID)

        self.retranslateUi(Widget)
        self.checkBox_translate.clicked["bool"].connect(self.groupBox_translate.setVisible)

        self.stackedWidget_provider.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Configure TranslateAndTTS", None))
        self.groupBox_appCache.setTitle(QCoreApplication.translate("Widget", u"App Cache", None))
        self.label_15.setText(QCoreApplication.translate("Widget", u"Threshold", None))
        self.spinBox_threshold.setSuffix(QCoreApplication.translate("Widget", u" day(s)", None))
        self.groupBox_ttsEngine.setTitle(QCoreApplication.translate("Widget", u"TTS Engine", None))
        self.radioButton_azure.setText(QCoreApplication.translate("Widget", u"Azure TTS", None))
#if QT_CONFIG(tooltip)
        self.radioButton_google.setToolTip(QCoreApplication.translate("Widget", u"Google Cloud TTS", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_google.setText(QCoreApplication.translate("Widget", u"Google TTS", None))
#if QT_CONFIG(tooltip)
        self.radioButton_gspeak.setToolTip(QCoreApplication.translate("Widget", u"based on Google Translate speech functionality", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_gspeak.setText(QCoreApplication.translate("Widget", u"GSpeak", None))
        self.radioButton_sapi5.setText(QCoreApplication.translate("Widget", u"Sapi5 (Windows)", None))
        self.radioButton_nsss.setText(QCoreApplication.translate("Widget", u"NSSS (Mac Only)", None))
        self.radioButton_coqui.setText(QCoreApplication.translate("Widget", u"coqui_ai_tts (Unsupported)", None))
        self.radioButton_espeak.setText(QCoreApplication.translate("Widget", u"espeak (Unsupported)", None))
        self.radioButton_kurdish.setText(QCoreApplication.translate("Widget", u"Kurdish TTS", None))
        self.groupBox_translate.setTitle(QCoreApplication.translate("Widget", u"Translate Settings", None))
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
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"App", None))
        self.checkBox_stats.setText(QCoreApplication.translate("Widget", u"Allow Collecting Stats", None))
#if QT_CONFIG(tooltip)
        self.checkBox_translate.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Uncheck this option If you just want it to speak in the text you are writing</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_translate.setText(QCoreApplication.translate("Widget", u"Translate", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"Key:", None))
        self.checkBox_saveAudio.setText(QCoreApplication.translate("Widget", u"Save Audio File", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"Region:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Voices Models", None))
        self.search_azure.setPlaceholderText(QCoreApplication.translate("Widget", u"Search", None))
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
    # retranslateUi

