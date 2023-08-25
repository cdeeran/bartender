import platform
from time import time

if platform.system() != 'Linux':
    '''
    Module RPi.GPIO is not available for windows.
    Thus this python code cannot be compiled.
    '''
    pass
else:
    from abc import ABC

    from hardware.pins import Pins
    from hardware.gpio import Gpio
    import RPi.GPIO as GPIO
    from time import sleep


    '''
    Need to view documentation:

    https://gpiozero.readthedocs.io/en/stable/api_pins.html#module-gpiozero.pins.native

    This is the hardware interface to execute pump control. Each pump is wired to an input on the 
    power relay, which is connected to a native pin the raspberry pi.
    '''
    class GpioInterface(Gpio):
        '''
        Initialize the GPIO interface with the Native Factory, this will allow for use to 
        drive pins high and low directly on the PI.
        '''
        def __init__(self,sim = None) -> None:
            super().__init__()
            GPIO.setmode(GPIO.BCM)
            self.gpio_dict = dict.fromkeys(Pins.GPIO_PINS_LIST, None)

        def setupPins(self,pumpConfig:dict):
            '''
            Initialize each pin as a native pin and store it in the dictonary
            '''
            for pin in Pins.GPIO_PINS_LIST:
                print("Initializing Pin {}:".format(pin))
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
 

        def pourDrinkStart(self, pin):
            GPIO.output(pin, GPIO.LOW)
        
        def pourDrinkFinish(self,pin):
            GPIO.output(pin, GPIO.HIGH)

        def turnOffGPIO(self):
            GPIO.cleanup()

        def getPin(self,pin):
            pass
        