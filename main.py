#! /usr/bin/env python3
import sys
import argparse
from PyQt5.QtWidgets import QApplication
from bartender.bartender import Bartender

'''
Creates and runs the bartender gui
'''
assert sys.version_info >= (3,6) # Must be running Python 3.6 or greater
parser = argparse.ArgumentParser()
parser.add_argument("--sim", dest="sim",help="Run bartender without GPIO", action="store_true")
parser.add_argument("--nospotify", dest="nospotify", help="Run bartender with or without spotify", action="store_true")
args = parser.parse_args()
app = QApplication(sys.argv)
bartenderApp = Bartender(args)
bartenderApp.show()
sys.exit(app.exec_())