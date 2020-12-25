from gpiozero.pins.pigpio import PiGPIOFactory as pgf
from gpiozero.pins.mock import MockFactory as mf
from gpiozero import LED
from hardware.pins import Pins

'''
Need to view documentation:

https://gpiozero.readthedocs.io/en/stable/remote_gpio.html

This is just a simulation class to test the interface between the 
bartender gui and the GPIO interface on the Raspberry PI
'''
RASPBERRY_PI_IP = "192.168.1.35"
class GPIO_SIM:

    def __init__(self,sim) -> None:
        super().__init__()
        self.sim = sim
        if self.sim == False:
            self.remote_factory = pgf(host=RASPBERRY_PI_IP)
        else:
            self.remote_factory = mf()
        self.gpio_dict = dict.fromkeys(Pins.GPIO_PINS_LIST,None)
            
    def setupPins(self,pins:list):
        for pin in pins:
            led = LED(pin,pin_factory=self.remote_factory)
            self.gpio_dict[pin] = led

    def pinOn(self, pin):
        self.gpio_dict[pin].on()

        if self.sim == True:
            print("Turning Pin: {} on".format(pin))

    def pinOff(self,pin):
        self.gpio_dict[pin].off()

        if self.sim == True:
            print("Turning Pin: {} off".format(pin))

    def pinsOff(self,pins:list):
        for pin in pins:
            self.gpio_dict[pin].off()
        
            if self.sim == True:
                print("Turning Pin: {} off".format(pin))

    def turnOffGPIO(self):
        for key,item in self.gpio_dict.items():
            if item != None:
                item.off()

    def getPin(self,pin) -> LED:
        return self.gpio_dict[pin]