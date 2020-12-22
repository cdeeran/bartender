from gpiozero.pins.pigpio import PiGPIOFactory as pgf
from gpiozero import Device, Button, LED
from time import sleep
from hardware.pins import Pins

'''
Need to view documentation:

https://gpiozero.readthedocs.io/en/stable/remote_gpio.html

This is just a simulation class to test the interface between the 
bartender gui and the GPIO interface on the Raspberry PI
'''
class GPIO_SIM:

    def __init__(self) -> None:
        super().__init__()
        self.remote_factory = pgf(host="192.168.1.34")
        self.gpio_dict = dict.fromkeys(Pins.GPIO_PINS_LIST,None)
            
    def setupPins(self,pins:list):
        for pin in pins:
            led = LED(pin,pin_factory=self.remote_factory)
            self.gpio_dict[pin] = led

    def pinOn(self, pin):
        self.gpio_dict[pin].on()

    def pinOff(self,pin):
        self.gpio_dict[pin].off()

    def pinsOff(self,pins:list):
        for pin in pins:
            self.gpio_dict[pin].off()

    def turnOffGPIO(self):
        for key,item in self.gpio_dict.items():
            if item != None:
                item.off()

    def getPin(self,pin) -> LED:
        return self.gpio_dict[pin]