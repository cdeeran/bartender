import json
import sys
import os
import platform
from threading import Thread
import time
from PyQt5.QtWidgets import QApplication, QCheckBox, QLabel, QListWidgetItem, QMainWindow
from bartender.thread_manager import ProgressThread, PourDrinkThread
from hardware.gpio_sim import GpioSim
from utils import constants

# import everything from the UIs
from ui.bartenderGui import *

if platform.system() == 'Linux':
    from hardware.gpio_interface import GpioInterface


class Bartender(QMainWindow):

    def __init__(self, args) -> None:
        super().__init__()
        self.args = args
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.gui.progressBar.hide()
        self.gui.progressStatus.hide()
        self.gui.progressStatus.setText("")
        self.gui.progressBar.setValue(0)
        self.pumpConfiguration = None
        if self.args.sim == True:
            self.gpioInterface = GpioSim(sim=self.args.sim)
        else:
            if os.name != 'nt':
                self.gpioInterface = GpioInterface()
        self.premadeDrinks = {}
        self.order = "Current Order: "

        self.drinkCheckBoxes = [self.gui.checkBox,
                                self.gui.checkBox_2,
                                self.gui.checkBox_3,
                                self.gui.checkBox_4,
                                self.gui.checkBox_5,
                                self.gui.checkBox_6]

        self.setupBarKeep()

    def setupBarKeep(self) -> None:
        self.pumpConfiguration = self.readPumpConfiguration(constants.PUMP_CONFIG_PATH)
        self.createPremadeDrinks(constants.PREMADE_DRINKS_PATH)

        self.gpioInterface.setupPins(self.pumpConfiguration)

        '''
        Set the values of the liquor and mixer options based
        upon the pump configuration
        '''
        self.updateCustomDrinkBoxes(
            self.gui.checkBox, self.pumpConfiguration["pump1"]["value"])
        self.updateCustomDrinkBoxes(
            self.gui.checkBox_2, self.pumpConfiguration["pump2"]["value"])
        self.updateCustomDrinkBoxes(
            self.gui.checkBox_3, self.pumpConfiguration["pump3"]["value"])
        self.updateCustomDrinkBoxes(
            self.gui.checkBox_4, self.pumpConfiguration["pump4"]["value"])
        self.updateCustomDrinkBoxes(
            self.gui.checkBox_5, self.pumpConfiguration["pump5"]["value"])
        self.updateCustomDrinkBoxes(
            self.gui.checkBox_6, self.pumpConfiguration["pump6"]["value"])

        '''
        Set the values of the premade drink list
        '''
        self.updatePremadeDrinkList()

        self.gui.gitlit_button.clicked.connect(self.gitLitClicked)

    def dumpPumpConfiguration(self) -> None:
        print(self.pumpConfiguration)

    @staticmethod
    def readPumpConfiguration(path) -> json:
        return json.load(open(path))

    def createPremadeDrinks(self, path) -> None:
        '''
        Determine what premade drinks we can server based upon
        the pump configuration.
        '''
        tempjson = json.load(open(path))
        for drink, ingredient in tempjson.items():
            ingredientCount = 0
            for _, value in self.pumpConfiguration.items():
                if value["value"] in ingredient["ingredients"]:
                    ingredientCount += 1
                if ingredientCount == len(ingredient["ingredients"]):
                    self.premadeDrinks[drink] = ingredient["ingredients"]

    def updateCustomDrinkBoxes(self, checkbox: QCheckBox, value: str) -> None:
        checkbox.setText(value)
        checkbox.adjustSize()

    def updatePremadeDrinkList(self):
        for key in self.premadeDrinks.keys():
            self.gui.listWidget.addItem(QListWidgetItem(key))

    def gitLitClicked(self):
        self.waitTime = 0
        self.threads = []
        for checkBox in self.drinkCheckBoxes:
            if checkBox.isChecked():
                for pump in self.pumpConfiguration.keys():
                    print("Selection: {0} Pump Found: {1}".format(
                        checkBox.text(), self.pumpConfiguration[pump]["value"]))
                    if checkBox.text() == self.pumpConfiguration[pump]["value"]:
                        '''
                        Wait time is pour time
                        '''
                        self.waitTime = constants.SHOT_TIME * constants.FLOW_RATE
                        if self.gui.radioShotButton_2.isChecked():
                            self.waitTime *= 2
                        elif self.gui.radioShotButton_3.isChecked():
                            self.waitTime *= 3
                        elif self.gui.radioShotButton_4.isChecked():
                            self.waitTime *= 4

                        pin = self.pumpConfiguration[pump]["pin"]
                        pourThread = PourDrinkThread(
                            pin, waitTime=self.waitTime)
                        pourThread.gpioStart.connect(
                            self.gpioInterface.pourDrinkStart)
                        pourThread.gpioFinished.connect(
                            self.gpioInterface.pourDrinkFinish)
                        self.threads.append(pourThread)
                        break

        self.gui.gitlit_button.hide()
        self.gui.progressBar.show()
        self.gui.progressStatus.show()
        gitlitThread = ProgressThread(waitTime=self.waitTime)
        gitlitThread.count.connect(self.updateDrinkProgress)
        self.threads.append(gitlitThread)

        self.startTime = time.time()
        for thread in self.threads:
            thread.start()

    def updateDrinkProgress(self, value) -> None:
        '''
        Number are definitely hacked... but whatever it's a nice progress bar
        '''
        self.gui.progressBar.setValue(int(value))
        print(int(value))

        if value <= 15:
            self.updateDrinkProgressStatus(
                self.gui.progressStatus, "Getting bartender's attention...")

        elif value > 15 and value <= 35:
            self.updateDrinkProgressStatus(
                self.gui.progressStatus, "Placing order with bartender...")

        elif value > 35 and value <= 55:
            self.updateDrinkProgressStatus(
                self.gui.progressStatus, "Getting ingredients together...")

        elif value > 55 and value <= 75:
            self.updateDrinkProgressStatus(
                self.gui.progressStatus, "Hittin' on the bitches ;)..")

        elif value > 75 and value <= 85:
            self.updateDrinkProgressStatus(
                self.gui.progressStatus, "Pouring your drink...")

        elif value > 85 and value <= 90:
            self.updateDrinkProgressStatus(
                self.gui.progressStatus, "Checking you out ;) ...")

        if value >= 100:
            self.updateDrinkProgressStatus(
                self.gui.progressStatus, "Order complete! Thank you!")
            self.gui.progressBar.setValue(100)
            time.sleep(2)
            print("Process Time: {} seconds".format(
                time.time() - self.startTime))
            self.resetGui()

    def updateDrinkProgressStatus(self, label: QLabel, value: str) -> None:
        label.setText(value)
        label.adjustSize()

    def resetGui(self):
        self.gui.progressBar.hide()
        self.gui.progressStatus.hide()
        self.gui.progressStatus.setText("")
        self.gui.progressBar.setValue(0)
        self.gui.gitlit_button.show()


if __name__ == "__main__":
    bartenderApp = QApplication(sys.argv)
    bartender = Bartender()
    bartender.show()
    sys.exit(bartenderApp.exec_())
