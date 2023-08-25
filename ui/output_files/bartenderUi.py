# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/ui_files/bartender.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BartenderUI(object):
    def setupUi(self, BartenderUI):
        BartenderUI.setObjectName("BartenderUI")
        BartenderUI.resize(790, 413)
        BartenderUI.setMinimumSize(QtCore.QSize(790, 413))
        BartenderUI.setMaximumSize(QtCore.QSize(790, 413))
        BartenderUI.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"QStatusBar{\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(BartenderUI)
        self.centralwidget.setObjectName("centralwidget")
        self.premadeDrinksButton = QtWidgets.QPushButton(self.centralwidget)
        self.premadeDrinksButton.setGeometry(QtCore.QRect(20, 10, 50, 50))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.premadeDrinksButton.setFont(font)
        self.premadeDrinksButton.setToolTipDuration(2)
        self.premadeDrinksButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: solid;\n"
"    border-radius: 10px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    max-width:50px;\n"
"  max-height:50px;\n"
"  min-width:50px;\n"
"  min-height:50px;\n"
"    background-image: url(:/images/images/premadeDrink.svg);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    }")
        self.premadeDrinksButton.setText("")
        self.premadeDrinksButton.setObjectName("premadeDrinksButton")
        self.customDrinkButton = QtWidgets.QPushButton(self.centralwidget)
        self.customDrinkButton.setGeometry(QtCore.QRect(20, 80, 50, 50))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.customDrinkButton.setFont(font)
        self.customDrinkButton.setToolTipDuration(2)
        self.customDrinkButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: solid;\n"
"    border-radius: 10px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    max-width:50px;\n"
"  max-height:50px;\n"
"  min-width:50px;\n"
"  min-height:50px;\n"
"    background-image: url(:/images/images/customDrink.svg);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    }")
        self.customDrinkButton.setText("")
        self.customDrinkButton.setObjectName("customDrinkButton")
        self.mainDisplayWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.mainDisplayWidget.setGeometry(QtCore.QRect(140, 10, 641, 381))
        self.mainDisplayWidget.setObjectName("mainDisplayWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.mainDisplayWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.mainDisplayWidget.addWidget(self.page_2)
        self.spotifyButton = QtWidgets.QPushButton(self.centralwidget)
        self.spotifyButton.setGeometry(QtCore.QRect(20, 160, 50, 50))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.spotifyButton.setFont(font)
        self.spotifyButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: solid;\n"
"    border-radius: 10px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    max-width:50px;\n"
"  max-height:50px;\n"
"  min-width:50px;\n"
"  min-height:50px;\n"
"    background-image: url(:/images/images/spotify-logo.svg);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    }")
        self.spotifyButton.setText("")
        self.spotifyButton.setObjectName("spotifyButton")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(20, 320, 50, 50))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.settingsButton.setFont(font)
        self.settingsButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: solid;\n"
"    border-radius: 10px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    max-width:50px;\n"
"  max-height:50px;\n"
"  min-width:50px;\n"
"  min-height:50px;\n"
"    background-image: url(:/images/images/settings.svg);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    }")
        self.settingsButton.setText("")
        self.settingsButton.setObjectName("settingsButton")
        self.homeButton = QtWidgets.QPushButton(self.centralwidget)
        self.homeButton.setGeometry(QtCore.QRect(20, 240, 50, 50))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.homeButton.setFont(font)
        self.homeButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: solid;\n"
"    border-radius: 10px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    max-width:50px;\n"
"  max-height:50px;\n"
"  min-width:50px;\n"
"  min-height:50px;\n"
"    \n"
"    background-image: url(:/images/images/home.svg);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0, stop: 1\n"
"        );\n"
"    }")
        self.homeButton.setText("")
        self.homeButton.setObjectName("homeButton")
        BartenderUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BartenderUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 21))
        self.menubar.setObjectName("menubar")
        BartenderUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BartenderUI)
        self.statusbar.setObjectName("statusbar")
        BartenderUI.setStatusBar(self.statusbar)

        self.retranslateUi(BartenderUI)
        self.mainDisplayWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(BartenderUI)

    def retranslateUi(self, BartenderUI):
        _translate = QtCore.QCoreApplication.translate
        BartenderUI.setWindowTitle(_translate("BartenderUI", "Bartender"))
        self.premadeDrinksButton.setToolTip(_translate("BartenderUI", "Search for premade drinks"))
        self.premadeDrinksButton.setStatusTip(_translate("BartenderUI", "Search for premade drinks"))
        self.customDrinkButton.setToolTip(_translate("BartenderUI", "Make a custom drink"))
        self.customDrinkButton.setStatusTip(_translate("BartenderUI", "Make a custom drink"))
from . import bartenderMainWindowResource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BartenderUI = QtWidgets.QMainWindow()
    ui = Ui_BartenderUI()
    ui.setupUi(BartenderUI)
    BartenderUI.show()
    sys.exit(app.exec_())
