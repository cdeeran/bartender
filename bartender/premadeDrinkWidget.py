'''
This class handles all the functionality from the PremadeDrinksUi.py file
'''
import json
import pprint
import time
from PyQt5 import QtCore, QtWidgets, QtGui
from ui.output_files.premadeDrinkUi import Ui_PremadeDrinksWidget
from utils import constants
from utils.bartenderExceptions import BartenderException
from bartender.thread_manager import ProgressThread, PourDrinkThread
from hardware.gpio_sim import GpioSim
class PremadeDrinkWidget(QtWidgets.QWidget):

    def __init__(self, pumpConfiguration, gpioInterface, sim=True) -> None:
        '''
        Initialize the widget
        '''
        super().__init__()

        self.view = Ui_PremadeDrinksWidget()
        self.view.setupUi(self)
        self.pumpConfiguration = pumpConfiguration
        self.knownDrinks       = None
        self.premadeDrinks     = {}
        if sim == False:
            from hardware.gpio_interface import GpioInterface

        self.gpioInterface     = gpioInterface

        self.setupWidget()
        self.createPremadeDrinks()
        return None
    
    def setupWidget(self) -> None:
        '''
        Change the settings of some view components
        '''
        self.view.premadeDrinkDetailsLabel.adjustSize()
        self.view.premadeDrinkListLabel.adjustSize()
        self.view.premadeDrinkProgressBar.setValue(0)
        self.view.premadeDrinkProgressBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.view.premadeDrinkProgressBar.hide()
        self.view.premadeDrinksList.setSpacing(7)
        self.view.premadeDrinksList.itemClicked.connect(self.displayDrinkDetails)
        self.view.premadeDrinkDetailsTextBrowser.setReadOnly(True)
        self.view.makePremadeDrinkButton.clicked.connect(self.makeDrink)
        self.knownDrinks = self.readKnownDrinks(constants.PREMADE_DRINKS_PATH)
        return None


    def dumpConfiguration(self) -> None:
        '''
        Debug function
        '''
        print("Current Pump Configuration")
        pprint.pprint(self.pumpConfiguration)
        print("Known Premade Drinks")
        pprint.pprint(self.knownDrinks)
        print("Drinks Eligible To Make")
        pprint.pprint(self.premadeDrinks)
        return None

    def updatePumpConfiguration(self, newConfiguration) -> None:
        '''
        Update the current pump configuration with a new one
        '''
        self.pumpConfiguration = newConfiguration
        self.createPremadeDrinks()
        return None

    def updateKnownDrinks(self) -> None:
        '''
        Update the dictonary of known drinks
        '''
        self.knownDrinks = self.readKnownDrinks(constants.PREMADE_DRINKS_PATH)
        self.createPremadeDrinks()
        return None

    def readKnownDrinks(self, path) -> json:
        '''
        Read in the pump configurations from the json file
        '''
        return json.load(open(path))

    def createPremadeDrinks(self) -> None:
        '''
        Determine what premade drinks we can server based upon
        the pump configuration.
        '''
        self.premadeDrinks.clear() # Purge the dictonary before updating
        for drink, ingredient in self.knownDrinks.items():
            ingredientCount = 0
            for _, value in self.pumpConfiguration.items():
                if value["value"] in ingredient["ingredients"]:
                    ingredientCount += 1
                if ingredientCount == len(ingredient["ingredients"]):
                    self.premadeDrinks[drink] = ingredient["ingredients"]

        self.updatePremadeDrinksList()
        return None

    def updatePremadeDrinksList(self) -> None:
        '''
        Update the premade drinks list with the drinks that can be made
        with the current pump configuration
        '''
        self.view.premadeDrinksList.clear() # Purge the list widget before updating
        for key in self.premadeDrinks.keys():
            self.view.premadeDrinksList.addItem(QtWidgets.QListWidgetItem(key))
        return None

    def displayDrinkDetails(self, item) -> None:
        '''
        Display what is in the premade drink in the Drink Details browser
        '''
        itemDetails = item.text()
        drinkDetails = "Ingredients:\n\n"
        for ingredient in self.premadeDrinks[itemDetails]:
            drinkDetails += "{}\n\n".format(ingredient)
        self.view.premadeDrinkDetailsTextBrowser.setText(drinkDetails.strip())
        return None

    def makeDrink(self) -> None:
        self.threads = []

        '''
        Hide the current interface
        '''
        self.view.makePremadeDrinkButton.hide()
        
        '''
        Attempt to pour the drink the user selected. Otherwise, handle the error.
        '''
        try:
            '''
            Get the drink selected and determine the ingredients that need to be poured
            '''
            currentDrinkSelected = self.view.premadeDrinksList.selectedItems()
            ingredients = self.premadeDrinks[currentDrinkSelected[0].text()]
            strengthLevel = self.getDrinkStrengthLevel()

            '''
            Iterate over the configuration to create the drink
            Throw and error if there is an incorrect drink type
            '''
            for pump in self.pumpConfiguration.keys():
                pumpValue = self.pumpConfiguration[pump]['value']
                valueType = self.pumpConfiguration[pump]['type']
                if pumpValue in ingredients:
                    pin = self.pumpConfiguration[pump]["pin"]
                    
                    '''
                    StrengthLevel is based on Alcohol. To prevent overflow and accurate drink measurement
                    we need to use the type variable in the configuration.
                    '''
                    if valueType == constants.LiquidType.MIXER.value:
                        self.waitTime = constants.FLOW_RATE * constants.StrengthLevel.MIXER_LEVEL.value
                    elif valueType == constants.LiquidType.ALCOHOL.value:
                        self.waitTime = constants.FLOW_RATE * self.getDrinkStrengthLevel()
                    else:
                        raise BartenderException("Invalid drink type in configuration. Please update configuration to Alcohol or Mixer.", "InvalidDrinkType")

                    '''
                    Create. Connect. Append the dispense drink thread for each pump in this drink order
                    '''
                    print("Wait Time: {}".format(self.waitTime))
                    dispenseDrinkThread = PourDrinkThread(pin, waitTime=self.waitTime)
                    dispenseDrinkThread.gpioStart.connect(self.gpioInterface.pourDrinkStart)
                    dispenseDrinkThread.gpioFinished.connect(self.gpioInterface.pourDrinkFinish)
                    self.threads.append(dispenseDrinkThread)
                
            '''
            Initialize the make drink thread
            '''
            progressBarThread = ProgressThread(waitTime=self.waitTime)
            progressBarThread.count.connect(self.updateDrinkProgress)
            self.threads.append(progressBarThread)
            
            '''
            Show the progress bar now that we know the order will go through
            '''
            self.view.premadeDrinkProgressBar.show()
            self.view.premadeDrinkProgressBar.setFormat("Submitting order {}".format(currentDrinkSelected[0].text()))

            '''
            Start the threads for the progress bar and Hardware interface
            '''
            for thread in self.threads:
                thread.start()

        except KeyError:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("The ingredient {} is not currently in the known pump configuration.".format(ingredients) + \
                            "If this is incorrect, go to settings and update the pump configuration and try again.")
            msgBox.setWindowTitle("Ingredient Not In Configuration")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
            self.resetGui()
        except IndexError:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("Please select a drink for the list!")
            msgBox.setWindowTitle("Drink Not Selected")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
            self.resetGui()
        except BartenderException:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText(BartenderException.getMessage())
            msgBox.setWindowTitle(BartenderException.getError())
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
            self.resetGui()
        except:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("An unknown error has occured! Please restart the application and try again.")
            msgBox.setWindowTitle("Unknown Error")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
        return None

    def getDrinkStrengthLevel(self) -> constants.StrengthLevel or BartenderException:
        '''
        Return the strength level select or raise a BartenderException
        '''
        if self.view.easyTigerStrengthLevel.isChecked():
            return constants.StrengthLevel.EASY_TIGER.value
            
        elif self.view.fiftyFiftyStrengthLevel.isChecked():
            return constants.StrengthLevel.FIFTY_FIFTY.value
        
        elif self.view.littyTittyStrengthLevel.isChecked():
            return constants.StrengthLevel.LITTY_TITTY.value
        
        elif self.view.adioMfStrengthLevel.isChecked():
            return constants.StrengthLevel.ADIOS_MF.value
        else:
            raise BartenderException("Strength Level was not selected. Return Code: {}".format(constants.StrengthLevel.LITTY_TITTY.value), "StrengthLevelError")
        

    def updateDrinkProgress(self, value) -> None:
        '''
        Numbers are definitely hacked... but whatever it's a nice progress bar
        '''
        self.view.premadeDrinkProgressBar.setValue(int(value))

        if value <= 15:
            self.view.premadeDrinkProgressBar.setFormat("Getting bartender's attention...")

        elif value > 15 and value <= 35:
            self.view.premadeDrinkProgressBar.setFormat("Placing order with bartender...")

        elif value > 35 and value <= 55:
            self.view.premadeDrinkProgressBar.setFormat("Getting ingredients together...")

        elif value > 55 and value <= 75:
            self.view.premadeDrinkProgressBar.setFormat("Hittin' on the cuties ;)..")

        elif value > 75 and value <= 85:
            self.view.premadeDrinkProgressBar.setFormat("Pouring your drink...")

        elif value > 85 and value <= 90:
            self.view.premadeDrinkProgressBar.setFormat("Checking you out ;) ...")

        if value >= 100:
            self.view.premadeDrinkProgressBar.setFormat("Order complete! Enjoy!")
            self.view.premadeDrinkProgressBar.setValue(100)
            time.sleep(2) # Let the ui show the drink is finished and let the hardware settle and reset
            self.resetGui()
        return None

    def resetGui(self) -> None:
        self.view.makePremadeDrinkButton.show()   
        self.view.premadeDrinkProgressBar.hide()
        return None