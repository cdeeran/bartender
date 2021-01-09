import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal

class ProgressThread(QThread):
    
    count = pyqtSignal(int)

    def __init__(self, waitTime = 0, parent = None) -> None:
        super(ProgressThread, self).__init__(parent)
        self.waitTime = waitTime 

    def run(self):
        count = 0
        sleepInterval = self.waitTime / 100.0
        while count < self.waitTime:
            count += sleepInterval * 10
            time.sleep(2)
            self.count.emit(count)

class PourDrinkThread(QThread):

    gpioStart = pyqtSignal(int)
    gpioFinished = pyqtSignal(int)

    def __init__(self, pin, waitTime = 0, parent = None) -> None:
        super(PourDrinkThread, self).__init__(parent)
        self.pin = pin
        self.waitTime = waitTime

    def run(self):
        self.gpioStart.emit(self.pin)
        time.sleep(self.waitTime)
        self.gpioFinished.emit(self.pin)
        