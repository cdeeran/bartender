'''
This class handles all the functionality from the PremadeDrinksUi.py file
'''
import json
import pprint
from PyQt5 import QtCore, QtWidgets
from ui.output_files.settingsUi import Ui_SettingsWidget
from utils import constants

class SettingsWidget(QtWidgets.QWidget):

    def __init__(self, updateSignal:QtCore.pyqtSignal):
        super().__init__()
        self.view = Ui_SettingsWidget()
        self.view.setupUi(self)
        self.pumpConfiguration = self.readPumpConfiguration(constants.PUMP_CONFIG_PATH)
        self.updateSignal = updateSignal

        '''
        Setup the buttons in the QDialogButtonBox 
        index 0 is the Save Button 
        index 1 is the Discard Button
        '''
        self.view.saveCancelSettingsBox.buttons()[0].clicked.connect(self.saveChanges) # Save button
        self.view.saveCancelSettingsBox.buttons()[1].clicked.connect(self.discardChanges) # Discard button

        '''
        Update the text fields to the last known saved configuration
        '''
        self.displayConfiguration()

    def dumpPumpConfiguration(self) -> None:
        '''
        Debug function
        '''
        print("Current Pump Configuration")
        pprint.pprint(self.pumpConfiguration)
        return None

    def readPumpConfiguration(self, path) -> json:
        '''
        Read in the pump configurations from the json file
        '''
        return json.load(open(path))

    def displayConfiguration(self):
        '''
        Update the text fields to the last known saved configuration
        '''
        self.view.pump1ConfigurationField.setText(self.pumpConfiguration['pump1']['value'])
        self.view.pump2ConfigurationField.setText(self.pumpConfiguration['pump2']['value'])
        self.view.pump3ConfigurationField.setText(self.pumpConfiguration['pump3']['value'])
        self.view.pump4ConfigurationField.setText(self.pumpConfiguration['pump4']['value'])
        self.view.pump5ConfigurationField.setText(self.pumpConfiguration['pump5']['value'])
        self.view.pump6ConfigurationField.setText(self.pumpConfiguration['pump6']['value'])

    def discardChanges(self):
        '''
        Confirm the user wants to discard their changes
        '''
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Are you sure you want to discard?")
        msgBox.setWindowTitle("Discard Changes")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        returnValue = msgBox.exec()
        '''
        If yes, display the last known saved configuration, else do nothing
        '''
        if returnValue == QtWidgets.QMessageBox.Yes:
            self.displayConfiguration()

    def saveChanges(self):
        '''
        Confirm the user wants to save their changes and overwrite the settings
        '''
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Are you sure you want to save these changes?")
        msgBox.setWindowTitle("Save Changes")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Yes:
            '''
            If user says yes, update the current pump configuration with the current text in the line
            edits
            '''
            self.pumpConfiguration['pump1']['value'] = self.view.pump1ConfigurationField.text()
            self.pumpConfiguration['pump2']['value'] = self.view.pump2ConfigurationField.text()
            self.pumpConfiguration['pump3']['value'] = self.view.pump3ConfigurationField.text()
            self.pumpConfiguration['pump4']['value'] = self.view.pump4ConfigurationField.text()
            self.pumpConfiguration['pump5']['value'] = self.view.pump5ConfigurationField.text()
            self.pumpConfiguration['pump6']['value'] = self.view.pump6ConfigurationField.text()

            '''
            Overwrite the current pump configuration
            '''            
            with open(constants.PUMP_CONFIG_PATH, "w") as configuration:
                '''
                Sort_keys=True, indent=4 adds formatting to the json file
                otherwise it will be written on a single line.
                '''
                json.dump(self.pumpConfiguration, configuration, sort_keys=True, indent=4)

                # Signal that there has been a configuration update
                self.updateSignal.emit()

        else:
            '''
            If user says no, refresh the UI with the last known saved configuration
            '''
            self.displayConfiguration()

    def getPumpConfiguration(self):
        return self.pumpConfiguration