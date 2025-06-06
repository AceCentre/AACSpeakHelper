# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
    QSize, Qt)
from PySide6.QtGui import (QFont, QIcon,
    QPixmap)
from PySide6.QtWidgets import (QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_item(object):
    def setupUi(self, item):
        if not item.objectName():
            item.setObjectName(u"item")
        item.resize(325, 91)
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
        self.stackedWidgetPage1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.gridLayout = QGridLayout(self.stackedWidgetPage1)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.photo = QLabel(self.stackedWidgetPage1)
        self.photo.setObjectName(u"photo")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.photo.sizePolicy().hasHeightForWidth())
        self.photo.setSizePolicy(sizePolicy)
        self.photo.setMaximumSize(QSize(40, 40))
        self.photo.setPixmap(QPixmap(u":/images/images/person.png"))
        self.photo.setScaledContents(True)

        self.gridLayout.addWidget(self.photo, 0, 0, 3, 1)

        self.name = QLabel(self.stackedWidgetPage1)
        self.name.setObjectName(u"name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.name.setFont(font)

        self.gridLayout.addWidget(self.name, 0, 2, 2, 1)

        self.line = QFrame(self.stackedWidgetPage1)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setLineWidth(0)
        self.line.setFrameShape(QFrame.VLine)

        self.gridLayout.addWidget(self.line, 0, 1, 3, 1)

        self.play = QPushButton(self.stackedWidgetPage1)
        self.play.setObjectName(u"play")
        sizePolicy.setHeightForWidth(self.play.sizePolicy().hasHeightForWidth())
        self.play.setSizePolicy(sizePolicy)
        self.play.setMaximumSize(QSize(30, 30))
        icon = QIcon()
        icon.addFile(u":/images/images/play-round-icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.play.setIcon(icon)
        self.play.setIconSize(QSize(30, 30))
        self.play.setFlat(True)

        self.gridLayout.addWidget(self.play, 0, 4, 3, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.gender = QLabel(self.stackedWidgetPage1)
        self.gender.setObjectName(u"gender")
        sizePolicy1.setHeightForWidth(self.gender.sizePolicy().hasHeightForWidth())
        self.gender.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(12)
        self.gender.setFont(font1)
        self.gender.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.gender, 2, 2, 1, 2)

        self.stackedWidget.addWidget(self.stackedWidgetPage1)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.data = QLabel(self.page)
        self.data.setObjectName(u"data")
        self.data.setGeometry(QRect(9, 9, 261, 31))
        self.stackedWidget.addWidget(self.page)

        self.verticalLayout.addWidget(self.stackedWidget)

        # Set button styling
        button_style = """
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 6px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #dee2e6;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """
        self.play.setStyleSheet(button_style)

        self.retranslateUi(item)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(item)
    # setupUi

    def retranslateUi(self, item):
        item.setWindowTitle(QCoreApplication.translate("item", u"Form", None))
        self.photo.setText("")
        self.name.setText(QCoreApplication.translate("item", u"Name", None))
        self.play.setText("")
        self.gender.setText(QCoreApplication.translate("item", u"Gender", None))
        self.data.setText("")
    # retranslateUi
