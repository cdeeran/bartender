from abc import ABC, abstractmethod

'''
Need to view documentation:

https://gpiozero.readthedocs.io/en/stable/remote_gpio.html

This is just a simulation class to test the interface between the 
bartender gui and the GPIO interface on the Raspberry PI
'''
class Gpio(ABC):

    def __init__(self,sim = None) -> None:
        super().__init__()

    @abstractmethod
    def setupPins(self,pumpConfig):
        pass

    @abstractmethod
    def pourDrinkStart(self, pin):
        pass
    
    @abstractmethod
    def pourDrinkFinish(self,pin):
        pass

    @abstractmethod
    def turnOffGPIO(self):
        pass

    @abstractmethod
    def getPin(self,pin):
        pass
        