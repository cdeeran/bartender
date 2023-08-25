'''
This class handles all the functionality from the PremadeDrinksUi.py file
'''
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from ui.output_files.splashScreenUi import Ui_BartenderSplashScreen

class SplashScreenWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.view = Ui_BartenderSplashScreen()
        self.view.setupUi(self)