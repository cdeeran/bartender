import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal

class ProgressThread(QThread):
    
    count = pyqtSignal(int)

    def __init__(self, waitTime = 0, parent = None) -> None:
        super(ProgressThread, self).__init__(parent)
        self.waitTime = waitTime 

    def run(self):
        count = 0.0
        sleepInterval = 100.0/self.waitTime
        while count < 100:
            count += sleepInterval
            time.sleep(1)
            self.count.emit(count)

class PourDrinkThread(QThread):
    '''
    Thread dedicated to the pouring the drink
    '''
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
        