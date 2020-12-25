#! /usr/bin/env python3
import sys
import os
import argparse
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from bartender.bartender import Bartender

'''
Creates and runs the bartender gui
'''
parser = argparse.ArgumentParser()
parser.add_argument("--sim", dest="sim",help="Run bartender without GPIO", action="store_true")
args = parser.parse_args()
app = QApplication(sys.argv)
bartenderApp = Bartender(args)
bartenderApp.show()
sys.exit(app.exec_())