import platform
from hardware.pins import Pins
from hardware.gpio_sim import GpioSim
from hardware.gpio import Gpio

if platform.system() == 'Linux':
    from hardware.gpio_interface import GpioInterface