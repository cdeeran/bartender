import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal

class ThreadManager(QThread):
    
    count = pyqtSignal(int)

    def __init__(self, parent = None) -> None:
        super(ThreadManager, self).__init__(parent)   

    def run(self):
        count = 0
        while count < 100:
            count += 5
            time.sleep(0.5)
            self.count.emit(count)
