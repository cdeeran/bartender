import json
import sys
import os
from threading import Thread
import time
from PyQt5.QtWidgets import QApplication, QCheckBox, QLabel, QListWidgetItem, QMainWindow
from bartender.thread_manager import ProgressThread, PourDrinkThread
from hardware.gpio_sim import GpioSim
from hardware.pins import Pins

# import everything from the UIs
from ui.bartenderGui import *

if os.name != 'nt':
    from hardware.gpio_interface import GpioInterface

FLOW_RATE = 60.0/100.0

SHOT_TIME = 50
class Bartender(QMainWindow):

    def __init__(self,args) -> None:
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
            self.gpioInterface = GpioSim(sim = self.args.sim)
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
        self.show()
          
    def setupBarKeep(self) -> None:
        self.pumpConfiguration = self.readPumpConfiguration()
        self.createPremadeDrinks()
        
        self.gpioInterface.setupPins(self.pumpConfiguration)
        

        '''
        Set the values of the liquor and mixer options based
        upon the pump configuration
        '''
        self.updateCustomDrinkBoxes(self.gui.checkBox,self.pumpConfiguration["pump1"]["value"])
        self.updateCustomDrinkBoxes(self.gui.checkBox_2,self.pumpConfiguration["pump2"]["value"])
        self.updateCustomDrinkBoxes(self.gui.checkBox_3,self.pumpConfiguration["pump3"]["value"])
        self.updateCustomDrinkBoxes(self.gui.checkBox_4,self.pumpConfiguration["pump4"]["value"])
        self.updateCustomDrinkBoxes(self.gui.checkBox_5,self.pumpConfiguration["pump5"]["value"])
        self.updateCustomDrinkBoxes(self.gui.checkBox_6,self.pumpConfiguration["pump6"]["value"])

        '''
        Set the values of the premade drink list
        '''
        self.updatePremadeDrinkList()

        self.gui.gitlit_button.clicked.connect(self.gitLitClicked)

    def dumpPumpConfiguration(self) -> None:
        print(self.pumpConfiguration)

    @staticmethod
    def readPumpConfiguration() -> json:
        return json.load(open("./hardware/pump_config.json"))

    def createPremadeDrinks(self) -> None:
        '''
        Determine what premade drinks we can server based upon
        the pump configuration.
        '''
        tempjson = json.load(open("./bartender/premade_drinks.json"))
        for drink, ingredient in tempjson.items():
            ingredientCount = 0
            for pump, value in self.pumpConfiguration.items():
                if value["value"] in ingredient["ingredients"]:
                    ingredientCount += 1
                if ingredientCount == len(ingredient["ingredients"]):
                    self.premadeDrinks[drink] = ingredient["ingredients"]

    def updateCustomDrinkBoxes(self,checkbox:QCheckBox, value:str) -> None:
        checkbox.setText(value)
        checkbox.adjustSize()

    def updatePremadeDrinkList(self):
        for key in self.premadeDrinks.keys():
            self.gui.listWidget.addItem(QListWidgetItem(key))

    def gitLitClicked(self):
        self.waitTime = 0
        threads = []
        for checkBox in self.drinkCheckBoxes:
            if checkBox.isChecked():
                for pump in self.pumpConfiguration.keys():
                    print("Selection: {0} Pump Found: {1}".format(checkBox.text(),self.pumpConfiguration[pump]["value"]))
                    if checkBox.text() == self.pumpConfiguration[pump]["value"]:
                        self.waitTime = SHOT_TIME * FLOW_RATE
                        pin = self.pumpConfiguration[pump]["pin"]
                        #self.pourThread = Thread(target=self.gpioInterface.pourDrink, args=(pin,self.waitTime))
                        pourThread = PourDrinkThread(pin,waitTime=self.waitTime)
                        pourThread.gpioStart.connect(self.gpioInterface.pourDrinkStart)
                        pourThread.gpioFinished.connect(self.gpioInterface.pourDrinkFinish)
                        threads.append(pourThread)
                        break
                    

        # TODO: Create a good way to do multiple selections
        self.gui.gitlit_button.hide()
        self.gui.progressBar.show()
        self.gui.progressStatus.show()
        gitlitThread = ProgressThread(waitTime=self.waitTime)
        gitlitThread.count.connect(self.updateDrinkProgress)
        threads.append(gitlitThread)


        for thread in threads:
            thread.start()

    def updateDrinkProgress(self,value) -> None:
        '''
        Number are definitely hacked... but whatever it's a nice progress bar
        '''
        self.gui.progressBar.setValue(value * 5)
        
        if value <= 6:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Getting bartender's attention...")

        elif value > 6 and value <= 12:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Placing order with bartender...")

        elif value > 12 and value <= 18:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Getting ingredients together...")

        elif value > 18 and value <= 21:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Hittin' on the bitches ;)..")

        elif value > 21 and value <= 24:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Pouring your drink...")

        elif value > 24 and value <= 27:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Checking you out ;) ...")

        if value == self.waitTime:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Order complete! Thank you!")
            self.gui.progressBar.setValue(100)
            time.sleep(3)
            self.resetGui()

    def updateDrinkProgressStatus(self, label:QLabel, value:str) -> None:
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