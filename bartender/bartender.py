import json
import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QLabel, QListWidgetItem, QMainWindow
from bartender.thread_manager import ThreadManager
from hardware.gpio_sim import GPIO_SIM
from hardware.pins import Pins
from PyQt5.QtCore import pyqtSignal

# import everything from the UIs
from ui.bartenderGui import *
class Bartender(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.gui.progressBar.hide()
        self.gui.progressStatus.setText("")
        self.gui.progressBar.setValue(0)
        self.pumpConfiguration = None
        self.gpioInterface = GPIO_SIM()
        self.premadeDrinks = {}
        self.setupBarKeep()
        self.show()
        
    
    def setupBarKeep(self) -> None:
        self.pumpConfiguration = self.readPumpConfiguration()
        self.createPremadeDrinks()
        
        self.gpioInterface.setupPins([  Pins.GPIO_PIN_14,
                                        Pins.GPIO_PIN_15,
                                        Pins.GPIO_PIN_18,
                                        Pins.GPIO_PIN_17,
                                        Pins.GPIO_PIN_22,
                                        Pins.GPIO_PIN_9,
                                        Pins.GPIO_PIN_10,
                                        Pins.GPIO_PIN_11 ])
        

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
        self.gpioInterface.pinOff(Pins.GPIO_PIN_11)
        self.gui.progressBar.show()
        self.gitlitThread = ThreadManager()
        self.gitlitThread.count.connect(self.updateDrinkProgress)
        self.gitlitThread.start()

    def updateDrinkProgress(self,value) -> None:
        self.gui.progressBar.setValue(value)

        if value <= 10:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Getting bartender's attention...")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_14)

        elif value > 10 and value <= 20:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Placing order with bartender...")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_15)

        elif value > 20 and value <= 50:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Getting ingredients together...")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_18)

        elif value > 50 and value <= 60:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Talking with other people instead of pouring your drink...")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_17)

        elif value > 60 and value <= 80:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Pouring your drink...")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_22)

        elif value > 80 and value <= 90:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Walking drink over to you...")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_9)

        elif value > 90 and value <= 99:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Checking you out ;) ...")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_10)

        else:
            self.updateDrinkProgressStatus(self.gui.progressStatus,"Order complete! Thank you!")
            self.gpioInterface.pinOn(Pins.GPIO_PIN_11)
            self.gpioInterface.pinsOff([Pins.GPIO_PIN_14,
                                        Pins.GPIO_PIN_15,
                                        Pins.GPIO_PIN_18,
                                        Pins.GPIO_PIN_17,
                                        Pins.GPIO_PIN_22,
                                        Pins.GPIO_PIN_9,
                                        Pins.GPIO_PIN_10])

    def updateDrinkProgressStatus(self, label:QLabel, value:str) -> None:
        label.setText(value)
        label.adjustSize()

if __name__ == "__main__":
    bartenderApp = QApplication(sys.argv)
    bartender = Bartender()
    bartender.show()
    sys.exit(bartenderApp.exec_())