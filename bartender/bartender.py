# PyQt Imports
from PyQt5 import Qt, QtCore, QtWidgets

# import everything from the UIs
from ui.output_files.bartenderUi import Ui_BartenderUI
from bartender.premadeDrinkWidget import PremadeDrinkWidget
from bartender.customDrinkWidget import CustomDrinkWidget
from bartender.settingsWidget import SettingsWidget
from bartender.spotifyWidget import SpotifyWidget
from bartender.splashScreenWidget import SplashScreenWidget
from hardware.gpio_sim import GpioSim
class Bartender(QtWidgets.QMainWindow):

    updatedConfigurationSignal = QtCore.pyqtSignal()
    updatedKnownDrinksSignal   = QtCore.pyqtSignal()

    def __init__(self, args):
        super().__init__()
        self.args = args
        '''
        Instantiate the main bartender window
        Call .setupUi(self) to create the new window form the QT Designer
        '''
        self.bartenderMainWindow = Ui_BartenderUI()
        self.bartenderMainWindow.setupUi(self) # Initialize the Bartender UI 
        
        '''
        Determine which gpio interface to use. The mainwindow has to initialize the gpio because once they are initialize
        they cannot updated.
        '''
        if self.args.sim == True:
            self.gpioInterface = GpioSim(sim=True)
        else:
            from hardware.gpio_interface import GpioInterface
            self.gpioInterface = GpioInterface()

        '''
        Initialize the widgets
        '''
        self.splashScreenWidget      = SplashScreenWidget()
        self.settingsWidget          = SettingsWidget(self.updatedConfigurationSignal)
        self.spotifyWidget           = SpotifyWidget(self.args.nospotify)
        self.updatedConfigurationSignal.connect(self.sendUpdateConfigurationSignal)
        self.updatedKnownDrinksSignal.connect(self.sendKnownDrinksUpdateSignal)
        self.gpioInterface.setupPins(self.settingsWidget.getPumpConfiguration())
        self.premadeDrinksWidget      = PremadeDrinkWidget(self.settingsWidget.getPumpConfiguration(), self.gpioInterface, sim=self.args.sim)
        self.customDrinkWidget        = CustomDrinkWidget(self.settingsWidget.getPumpConfiguration(), self.updatedKnownDrinksSignal, self.gpioInterface, sim=self.args.sim)
        self.setupMainWindow()
        

    def setupMainWindow(self):
        '''
        Setup the stacked widget to display the other widgets based on which button is pressed
        '''
        self.bartenderMainWindow.mainDisplayWidget.insertWidget(0,self.splashScreenWidget)
        self.bartenderMainWindow.homeButton.clicked.connect(self.displaySplashScreenWidget)
        self.displaySplashScreenWidget()
        
        self.bartenderMainWindow.mainDisplayWidget.insertWidget(1,self.premadeDrinksWidget)
        self.bartenderMainWindow.premadeDrinksButton.clicked.connect(self.displayPremadeDrinksWidget)
    
        self.bartenderMainWindow.mainDisplayWidget.insertWidget(2,self.customDrinkWidget)
        self.bartenderMainWindow.customDrinkButton.clicked.connect(self.displayCustomDrinkWidget)

        self.bartenderMainWindow.mainDisplayWidget.insertWidget(3,self.spotifyWidget)
        self.bartenderMainWindow.spotifyButton.clicked.connect(self.displaySpotifyWidget)

        self.bartenderMainWindow.mainDisplayWidget.insertWidget(4,self.settingsWidget)
        self.bartenderMainWindow.settingsButton.clicked.connect(self.displaySettingsWidget)

    def displaySplashScreenWidget(self):
        '''
        Display the splash screen aka landing page
        '''
        self.bartenderMainWindow.mainDisplayWidget.setCurrentIndex(0)

    def displayPremadeDrinksWidget(self):
        '''
        Display the premade drinks widget
        '''
        self.bartenderMainWindow.mainDisplayWidget.setCurrentIndex(1)

    def displayCustomDrinkWidget(self):
        '''
        Display the custom drink widget
        '''
        self.bartenderMainWindow.mainDisplayWidget.setCurrentIndex(2)

    def displaySpotifyWidget(self):
        '''
        Display the spotify widget
        '''
        self.bartenderMainWindow.mainDisplayWidget.setCurrentIndex(3)

    def displaySettingsWidget(self):
        '''
        Display the spotify widget
        '''
        self.bartenderMainWindow.mainDisplayWidget.setCurrentIndex(4)

    def sendUpdateConfigurationSignal(self):
        '''
        Pump Configuration has changed from settings being saved.
        Update the widgets that need to know about the new configuration.
        '''
        self.premadeDrinksWidget.updatePumpConfiguration(self.settingsWidget.getPumpConfiguration())
        self.customDrinkWidget.updatePumpConfiguration(self.settingsWidget.getPumpConfiguration())

    def sendKnownDrinksUpdateSignal(self):
        '''
        Signal that there is a new drink
        '''
        self.premadeDrinksWidget.updateKnownDrinks()

    def closeEvent(self, event) -> None:
        print("Exiting application...")
        if not self.args.sim:
            print("Cleaning up gpio...")
            self.gpioInterface.turnOffGPIO()
        
        event.accept()