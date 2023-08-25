'''
This class handles all the functionality from the PremadeDrinksUi.py file
'''
import json
import time
from PyQt5 import QtWidgets, QtCore
from ui.output_files.customDrinkUi import Ui_CustomDrinkWidget
from utils import constants
from utils.bartenderExceptions import BartenderException
from bartender.thread_manager import ProgressThread, PourDrinkThread
from hardware.gpio_sim import GpioSim
class CustomDrinkWidget(QtWidgets.QWidget):

    def __init__(self, pumpConfiguration, updateKnownDrinksSignal:QtCore.pyqtSignal, gpioInterface, sim=True) -> None:
        super().__init__()
        self.view = Ui_CustomDrinkWidget()
        self.view.setupUi(self)
        self.pumpConfiguration = pumpConfiguration
        self.knownDrinks = None 
        self.updateKnownDrinksSignal = updateKnownDrinksSignal
        if sim == False:
            from hardware.gpio_interface import GpioInterface
        self.gpioInterface = gpioInterface

        self.setupWidget()
        return None

    def setupWidget(self) -> None:
        '''
        Set the values of the liquor and mixer options based
        upon the pump configuration
        '''
        self.setCustomDrinkBoxes()
        self.view.customDrinkProgressBar.setValue(0)
        self.view.customDrinkProgressBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.view.customDrinkProgressBar.hide()
        self.view.makeCustomDrinkButton.clicked.connect(self.makeDrink)
        self.view.clearCustomDrinkButton.clicked.connect(self.resetGui)
        self.view.saveCustomDrinkButton.clicked.connect(self.save)
        self.knownDrinks = self.readKnownDrinks(constants.PREMADE_DRINKS_PATH)
        return None

    def setCustomDrinkBoxes(self) -> None:
        '''
        Set the text of the check boxes with the pump configuration
        '''
        self.view.drinkOption1.setText(self.pumpConfiguration["pump1"]["value"])
        self.view.drinkOption2.setText(self.pumpConfiguration["pump2"]["value"])
        self.view.drinkOption3.setText(self.pumpConfiguration["pump3"]["value"])
        self.view.drinkOption4.setText(self.pumpConfiguration["pump4"]["value"])
        self.view.drinkOption5.setText(self.pumpConfiguration["pump5"]["value"])
        self.view.drinkOption6.setText(self.pumpConfiguration["pump6"]["value"])
        self.view.drinkOption1.adjustSize()
        self.view.drinkOption2.adjustSize()
        self.view.drinkOption3.adjustSize()
        self.view.drinkOption4.adjustSize()
        self.view.drinkOption5.adjustSize()
        self.view.drinkOption6.adjustSize()
        self.view.drinkOption1.toggled.connect(self.view.drinkOption1.adjustSize)
        self.view.drinkOption2.toggled.connect(self.view.drinkOption2.adjustSize)
        self.view.drinkOption3.toggled.connect(self.view.drinkOption3.adjustSize)
        self.view.drinkOption4.toggled.connect(self.view.drinkOption4.adjustSize)
        self.view.drinkOption5.toggled.connect(self.view.drinkOption5.adjustSize)
        self.view.drinkOption6.toggled.connect(self.view.drinkOption6.adjustSize)
        
        return None


    def readKnownDrinks(self, path) -> json:
        '''
        Read in the pump configurations from the json file
        '''
        return json.load(open(path))


    def updatePumpConfiguration(self, newConfiguration) -> None:
        '''
        Update the pump configuration 
        '''
        self.pumpConfiguration = newConfiguration
        self.setCustomDrinkBoxes()
        return None


    def makeDrink(self) -> None:
        self.threads = []

        '''
        Hide the current interface
        '''
        self.view.makeCustomDrinkButton.hide()
        self.view.mixItLabel.hide()
        self.view.saveCustomDrinkButton.hide()
        self.view.saveLabel.hide()
        self.view.clearCustomDrinkButton.hide()
        self.view.clearLabel.hide() 

        '''
        Attempt to pour the drink the user selected. Otherwise, handle the error.
        '''
        try:
            '''
            Get the drink selected and determine the ingredients that need to be poured
            '''
            selectedDrinkOptions = self.getDrinkOptions()
            strengthLevel = self.getDrinkStrengthLevel()
            ingredient = ""
            for pump in self.pumpConfiguration.keys():
                ingredient = self.pumpConfiguration[pump]["value"]
                ingredientType = self.pumpConfiguration[pump]["type"]
                if  ingredient in selectedDrinkOptions:
                    print("PUMP: {} SELECTED OPTION: {}".format(pump, ingredient))

                    pin = self.pumpConfiguration[pump]["pin"]
                    
                    '''
                    StrengthLevel is based on Alcohol. To prevent overflow and accurate drink measurement
                    we need to use the type variable in the configuration.
                    '''
                    if ingredientType == constants.LiquidType.MIXER.value:
                        self.waitTime = constants.FLOW_RATE * constants.StrengthLevel.MIXER_LEVEL.value
                    elif ingredientType == constants.LiquidType.ALCOHOL.value:
                        self.waitTime = constants.FLOW_RATE * strengthLevel
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
            makeDrinkThread = ProgressThread(waitTime=self.waitTime)
            makeDrinkThread.count.connect(self.updateDrinkProgress)
            self.threads.append(makeDrinkThread)
            
            '''
            Show the progress bar now that we know the order will go through
            '''
            self.view.customDrinkProgressBar.show()
            self.view.customDrinkProgressBar.setFormat("Submitting custom drink order...")

            '''
            Start the threads for the progress bar and Hardware interface
            '''
            for thread in self.threads:
                thread.start()

        except KeyError:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("The ingredient {} is not currently in the known pump configuration.".format(ingredient) + \
                            "If this is incorrect, go to settings and update the pump configuration and try again.")
            msgBox.setWindowTitle("Ingredient Not In Configuration")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
            self.resetGui()

        except BartenderException as e:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText(e.getMessage())
            msgBox.setWindowTitle(e.getError())
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

    def getDrinkOptions(self) -> list() or BartenderException:
        '''
        Get all of the drink options checked
        '''
        checkedBoxes = []

        if self.view.drinkOption1.isChecked():
            checkedBoxes.append(self.view.drinkOption1.text())
        if self.view.drinkOption2.isChecked():
            checkedBoxes.append(self.view.drinkOption2.text())
        if self.view.drinkOption3.isChecked():
            checkedBoxes.append(self.view.drinkOption3.text())
        if self.view.drinkOption4.isChecked():
            checkedBoxes.append(self.view.drinkOption4.text())
        if self.view.drinkOption5.isChecked():
            checkedBoxes.append(self.view.drinkOption5.text())
        if self.view.drinkOption6.isChecked():
            checkedBoxes.append(self.view.drinkOption6.text())
        
        print(checkedBoxes)
        if len(checkedBoxes) == 0:
            raise BartenderException("No drink options selected", "DrinkOptionError")
        else:
            return checkedBoxes

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
            raise BartenderException("Strength Level was not selected", "StrengthLevelError") 

    def updateDrinkProgress(self, value) -> None:
        '''
        Numbers are definitely hacked... but whatever it's a nice progress bar
        '''
        self.view.customDrinkProgressBar.setValue(int(value))

        if value <= 15:
            self.view.customDrinkProgressBar.setFormat("Getting bartender's attention...")

        elif value > 15 and value <= 35:
            self.view.customDrinkProgressBar.setFormat("Placing order with bartender...")

        elif value > 35 and value <= 55:
            self.view.customDrinkProgressBar.setFormat("Getting ingredients together...")

        elif value > 55 and value <= 75:
            self.view.customDrinkProgressBar.setFormat("Hittin' on the cuties ;)")

        elif value > 75 and value <= 85:
            self.view.customDrinkProgressBar.setFormat("Pouring your drink...")

        elif value > 85 and value <= 90:
            self.view.customDrinkProgressBar.setFormat("Checking you out ;)")

        if value >= 100:
            self.view.customDrinkProgressBar.setFormat("Order complete! Cheers!")
            self.view.customDrinkProgressBar.setValue(100)
            time.sleep(2) # Let the ui show the drink is finished and let the hardware settle and reset
            self.resetGui()
        return None

    def resetGui(self) -> None:
        '''
        Reset the Gui to it's nominal state
        '''
        self.view.makeCustomDrinkButton.show()
        self.view.mixItLabel.show()
        self.view.saveCustomDrinkButton.show()
        self.view.saveLabel.show()
        self.view.clearCustomDrinkButton.show()
        self.view.clearLabel.show() 
        self.view.customDrinkProgressBar.hide()
        self.view.customDrinkProgressBar.setValue(0)

        '''
        Clear checkboxes
        '''
        self.view.drinkOption1.setChecked(False)
        self.view.drinkOption2.setChecked(False)
        self.view.drinkOption3.setChecked(False)
        self.view.drinkOption4.setChecked(False)
        self.view.drinkOption5.setChecked(False)
        self.view.drinkOption6.setChecked(False)   


        return None

    def save(self) -> None:
        '''
        Confirm the user wants to save their drink
        '''
        drinkName, returnValue = QtWidgets.QInputDialog.getText(self, "Save Drink", "Enter Drink Name:")

        if returnValue:
            try:
                if drinkName in self.knownDrinks.keys():
                    raise BartenderException("Drink already exists!", "DrinkExistsError")
                else:
                    self.knownDrinks[drinkName] = {"ingredients":[]}
                    for ingredient in self.getDrinkOptions():
                        self.knownDrinks[drinkName]['ingredients'].append(ingredient)

                    with open(constants.PREMADE_DRINKS_PATH, "w") as premadeDrinks:
                        '''
                        Sort_keys=True, indent=4 adds formatting to the json file
                        otherwise it will be written on a single line.
                        '''
                        json.dump(self.knownDrinks, premadeDrinks, sort_keys=True, indent=4)
                        
                    # Signal that there has been a new drink added
                    self.updateKnownDrinksSignal.emit()

            except BartenderException as e:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                msgBox.setText(e.getMessage())
                msgBox.setWindowTitle(e.getError())
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.exec()