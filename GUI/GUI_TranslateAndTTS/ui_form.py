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
    QLineEdit, QListWidget, QListWidgetItem, QRadioButton,
    QSizePolicy, QSlider, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 487)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_ttsEngine = QGroupBox(Widget)
        self.groupBox_ttsEngine.setObjectName(u"groupBox_ttsEngine")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_ttsEngine.sizePolicy().hasHeightForWidth())
        self.groupBox_ttsEngine.setSizePolicy(sizePolicy)
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
        self.radioButton_azure.setChecked(True)

        self.verticalLayout.addWidget(self.radioButton_azure)

        self.radioButton_google = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_google.setObjectName(u"radioButton_google")
        sizePolicy1.setHeightForWidth(self.radioButton_google.sizePolicy().hasHeightForWidth())
        self.radioButton_google.setSizePolicy(sizePolicy1)
        self.radioButton_google.setChecked(False)

        self.verticalLayout.addWidget(self.radioButton_google)

        self.radioButton_sapi5 = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_sapi5.setObjectName(u"radioButton_sapi5")
        sizePolicy1.setHeightForWidth(self.radioButton_sapi5.sizePolicy().hasHeightForWidth())
        self.radioButton_sapi5.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.radioButton_sapi5)

        self.radioButton_coqui = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_coqui.setObjectName(u"radioButton_coqui")
        sizePolicy1.setHeightForWidth(self.radioButton_coqui.sizePolicy().hasHeightForWidth())
        self.radioButton_coqui.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.radioButton_coqui)

        self.radioButton_nsss = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_nsss.setObjectName(u"radioButton_nsss")
        sizePolicy1.setHeightForWidth(self.radioButton_nsss.sizePolicy().hasHeightForWidth())
        self.radioButton_nsss.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.radioButton_nsss)

        self.radioButton_espeak = QRadioButton(self.groupBox_ttsEngine)
        self.radioButton_espeak.setObjectName(u"radioButton_espeak")
        sizePolicy1.setHeightForWidth(self.radioButton_espeak.sizePolicy().hasHeightForWidth())
        self.radioButton_espeak.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.radioButton_espeak)


        self.gridLayout.addWidget(self.groupBox_ttsEngine, 0, 0, 1, 1)

        self.groupBox_translate = QGroupBox(Widget)
        self.groupBox_translate.setObjectName(u"groupBox_translate")
        sizePolicy.setHeightForWidth(self.groupBox_translate.sizePolicy().hasHeightForWidth())
        self.groupBox_translate.setSizePolicy(sizePolicy)
        self.groupBox_translate.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_translate)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox_overwritepb = QCheckBox(self.groupBox_translate)
        self.checkBox_overwritepb.setObjectName(u"checkBox_overwritepb")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.checkBox_overwritepb.sizePolicy().hasHeightForWidth())
        self.checkBox_overwritepb.setSizePolicy(sizePolicy2)
        self.checkBox_overwritepb.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_overwritepb, 1, 0, 1, 1)

        self.checkBox_translate = QCheckBox(self.groupBox_translate)
        self.checkBox_translate.setObjectName(u"checkBox_translate")
        sizePolicy2.setHeightForWidth(self.checkBox_translate.sizePolicy().hasHeightForWidth())
        self.checkBox_translate.setSizePolicy(sizePolicy2)
        self.checkBox_translate.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_translate, 0, 0, 1, 1)

        self.comboBox_writeLang = QComboBox(self.groupBox_translate)
        self.comboBox_writeLang.setObjectName(u"comboBox_writeLang")

        self.gridLayout_2.addWidget(self.comboBox_writeLang, 2, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_translate)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)

        self.label = QLabel(self.groupBox_translate)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.comboBox_targetLang = QComboBox(self.groupBox_translate)
        self.comboBox_targetLang.setObjectName(u"comboBox_targetLang")
        sizePolicy2.setHeightForWidth(self.comboBox_targetLang.sizePolicy().hasHeightForWidth())
        self.comboBox_targetLang.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboBox_targetLang, 3, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_translate, 1, 0, 1, 1)

        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy4)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.formLayoutWidget_4 = QWidget(self.page)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(0, 30, 441, 391))
        self.gridLayout_4 = QGridLayout(self.formLayoutWidget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.checkBox_saveToWav = QCheckBox(self.formLayoutWidget_4)
        self.checkBox_saveToWav.setObjectName(u"checkBox_saveToWav")
        self.checkBox_saveToWav.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_saveToWav, 2, 1, 1, 1)

        self.listWidget_voiceazure = QListWidget(self.formLayoutWidget_4)
        self.listWidget_voiceazure.setObjectName(u"listWidget_voiceazure")
        sizePolicy.setHeightForWidth(self.listWidget_voiceazure.sizePolicy().hasHeightForWidth())
        self.listWidget_voiceazure.setSizePolicy(sizePolicy)
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

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.formLayoutWidget = QWidget(self.page_2)
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

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 2, 1)

        self.buttonBox = QDialogButtonBox(Widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setInputMethodHints(Qt.ImhPreferUppercase)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        QWidget.setTabOrder(self.radioButton_azure, self.radioButton_google)
        QWidget.setTabOrder(self.radioButton_google, self.radioButton_sapi5)
        QWidget.setTabOrder(self.radioButton_sapi5, self.radioButton_coqui)
        QWidget.setTabOrder(self.radioButton_coqui, self.radioButton_nsss)
        QWidget.setTabOrder(self.radioButton_nsss, self.radioButton_espeak)
        QWidget.setTabOrder(self.radioButton_espeak, self.checkBox_translate)
        QWidget.setTabOrder(self.checkBox_translate, self.checkBox_overwritepb)
        QWidget.setTabOrder(self.checkBox_overwritepb, self.comboBox_writeLang)
        QWidget.setTabOrder(self.comboBox_writeLang, self.comboBox_targetLang)
        QWidget.setTabOrder(self.comboBox_targetLang, self.lineEdit_key)
        QWidget.setTabOrder(self.lineEdit_key, self.lineEdit_region)
        QWidget.setTabOrder(self.lineEdit_region, self.checkBox_saveToWav)
        QWidget.setTabOrder(self.checkBox_saveToWav, self.listWidget_voiceazure)
        QWidget.setTabOrder(self.listWidget_voiceazure, self.horizontalSlider_volume)
        QWidget.setTabOrder(self.horizontalSlider_volume, self.horizontalSlider_rate)
        QWidget.setTabOrder(self.horizontalSlider_rate, self.lineEdit_voiceID)

        self.retranslateUi(Widget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Configure TranslateAndTTS", None))
        self.groupBox_ttsEngine.setTitle(QCoreApplication.translate("Widget", u"TTS Engine", None))
        self.radioButton_azure.setText(QCoreApplication.translate("Widget", u"Azure TTS", None))
        self.radioButton_google.setText(QCoreApplication.translate("Widget", u"Google TTS", None))
        self.radioButton_sapi5.setText(QCoreApplication.translate("Widget", u"sapi5 (Windows)", None))
        self.radioButton_coqui.setText(QCoreApplication.translate("Widget", u"coqui_ai_tts (mac)", None))
        self.radioButton_nsss.setText(QCoreApplication.translate("Widget", u"nsss (mac)", None))
        self.radioButton_espeak.setText(QCoreApplication.translate("Widget", u"espeak (Linux)", None))
        self.groupBox_translate.setTitle(QCoreApplication.translate("Widget", u"Translate Settings", None))
#if QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Do you want to overwrite the pasteboard with the new translated string?</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_overwritepb.setText(QCoreApplication.translate("Widget", u"Overwrite Pasteboard", None))
#if QT_CONFIG(tooltip)
        self.checkBox_translate.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Uncheck this option If you just want it to speak in the text you are writing</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_translate.setText(QCoreApplication.translate("Widget", u"Translate", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Widget", u"Target Language for Translattion", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Widget", u"Target Language", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">Writing Language </span></pre><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Widget", u"Writing Language", None))
        self.checkBox_saveToWav.setText(QCoreApplication.translate("Widget", u"Save to Wav Files", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"Key:", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"Region:", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"Voice Model:", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Volume:", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Rate:", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:14px; color:#6a9955;\">VoiceID. To find what this would be run the programme with --listvoices</span></pre></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Widget", u"Voice ID:", None))
    # retranslateUi

