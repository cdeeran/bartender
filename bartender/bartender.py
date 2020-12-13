
import hardware
import bartender
import json
import sys
import os
from PyQt5.QtWidgets import QApplication, QCheckBox, QListWidgetItem, QMainWindow

# import everything from the UI
from ui.bartenderGui import *

class Bartender(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.pumpConfiguration = None
        self.premadeDrinks = {}
        self.setupBarKeep()
        self.show()
        
    
    def setupBarKeep(self) -> None:
        self.pumpConfiguration = self.readPumpConfiguration()
        self.createPremadeDrinks()
        
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

        self.gui.gitlit_button.clicked


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
        tempDictionary = {}
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
        for key,val in self.premadeDrinks.items():
            self.gui.listWidget.addItem(QListWidgetItem(key))

if __name__ == "__main__":
    bartenderApp = QApplication(sys.argv)
    bartender = Bartender()
    bartender.show()
    sys.exit(bartenderApp.exec_())