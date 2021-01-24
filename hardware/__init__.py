import os
from hardware.pins import Pins
from hardware.gpio_sim import GpioSim
from hardware.gpio import Gpio

if os.name != 'nt':
    from hardware.gpio_interface import GpioInterface