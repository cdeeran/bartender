from abc import ABC
from gpiozero.pins.pigpio import PiGPIOFactory as pgf
from gpiozero.pins.mock import MockFactory as mf
from gpiozero import LED
from hardware.pins import Pins
from hardware.gpio import Gpio
from time import sleep
'''
Need to view documentation:

https://gpiozero.readthedocs.io/en/stable/remote_gpio.html

This is just a simulation class to test the interface between the 
bartender gui and the GPIO interface on the Raspberry PI
'''
RASPBERRY_PI_IP = "192.168.1.35"
class GpioSim(Gpio):

    def __init__(self,sim = None) -> None:
        '''
        Initialize the simulation interface. If the raspberry pi is
        connected to a breadboard with LEDs and you are SSHing into the pi to run
        make sure the sim variable is False, so it will establish a remote connection to the pi
        using the constant ip address above. Otherwise, set sim to True and the code will be executed
        with console output.
        '''
        super().__init__(sim)
        self.sim = sim
        if self.sim == False:
            self.remote_factory = pgf(host=RASPBERRY_PI_IP)
        else:
            self.remote_factory = mf()
        self.gpio_dict = dict.fromkeys(Pins.GPIO_PINS_LIST,None)

    def setupPins(self,pumpConfig:dict):
        '''
        Initialize each pin an LED for simulation and store it in the dictonary
        '''
        for pump in pumpConfig.keys():
            led = LED(pumpConfig[pump]["pin"],pin_factory=self.remote_factory)
            self.gpio_dict[pumpConfig[pump]["pin"]] = led
        
        self.turnOffGPIO()
            
    def pourDrinkStart(self, pin):
        self.gpio_dict[pin].on()

        if self.sim == True:
            print("Turning Pin: {} on".format(pin))

    def pourDrinkFinish(self,pin):
        self.gpio_dict[pin].off()

        if self.sim == True:
            print("Turning Pin: {} off".format(pin))

    def turnOffGPIO(self):
        for key,item in self.gpio_dict.items():
            if item != None:
                item.off()

    def getPin(self,pin) -> LED:
        return self.gpio_dict[pin]