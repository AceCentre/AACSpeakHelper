# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_item(object):
    def setupUi(self, item):
        if not item.objectName():
            item.setObjectName(u"item")
        item.resize(333, 53)
        self.verticalLayout = QVBoxLayout(item)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(item)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QFrame.Raised)
        self.stackedWidgetPage1 = QWidget()
        self.stackedWidgetPage1.setObjectName(u"stackedWidgetPage1")
        self.gridLayout = QGridLayout(self.stackedWidgetPage1)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.line = QFrame(self.stackedWidgetPage1)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setLineWidth(0)
        self.line.setFrameShape(QFrame.VLine)

        self.gridLayout.addWidget(self.line, 0, 1, 3, 1)

        self.play = QPushButton(self.stackedWidgetPage1)
        self.play.setObjectName(u"play")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.play.sizePolicy().hasHeightForWidth())
        self.play.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/images/images/play-round-icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.play.setIcon(icon)
        self.play.setIconSize(QSize(25, 25))
        self.play.setFlat(True)

        self.gridLayout.addWidget(self.play, 0, 3, 3, 1)

        self.gender = QLabel(self.stackedWidgetPage1)
        self.gender.setObjectName(u"gender")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gender.sizePolicy().hasHeightForWidth())
        self.gender.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(8)
        self.gender.setFont(font)

        self.gridLayout.addWidget(self.gender, 2, 2, 1, 1)

        self.name = QLabel(self.stackedWidgetPage1)
        self.name.setObjectName(u"name")
        sizePolicy1.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        self.name.setFont(font1)

        self.gridLayout.addWidget(self.name, 0, 2, 2, 1)

        self.photo = QLabel(self.stackedWidgetPage1)
        self.photo.setObjectName(u"photo")
        sizePolicy.setHeightForWidth(self.photo.sizePolicy().hasHeightForWidth())
        self.photo.setSizePolicy(sizePolicy)
        self.photo.setMaximumSize(QSize(25, 25))
        self.photo.setPixmap(QPixmap(u":/images/images/person.png"))
        self.photo.setScaledContents(True)

        self.gridLayout.addWidget(self.photo, 0, 0, 3, 1)

        self.stackedWidget.addWidget(self.stackedWidgetPage1)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.data = QLabel(self.page)
        self.data.setObjectName(u"data")
        self.data.setGeometry(QRect(9, 9, 261, 31))
        self.stackedWidget.addWidget(self.page)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(item)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(item)
    # setupUi

    def retranslateUi(self, item):
        item.setWindowTitle(QCoreApplication.translate("item", u"Form", None))
        self.play.setText("")
        self.gender.setText(QCoreApplication.translate("item", u"Gender", None))
        self.name.setText(QCoreApplication.translate("item", u"Name", None))
        self.photo.setText("")
        self.data.setText("")
    # retranslateUi

