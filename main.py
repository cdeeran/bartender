import sys
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from bartender.bartender import Bartender

'''
Creates and runs the bartender gui
'''
app = QApplication(sys.argv)
bartenderApp = Bartender()
bartenderApp.show()
sys.exit(app.exec_())