from machine import UART, Pin
from lib.mh_z19 import MH_Z19
import utime

# UART Pins 
UART_TX_PIN = 16  # Pico TX --> Sensor RX
UART_RX_PIN = 17  # Pico RX <-- Sensor TX

def read_co2():
    sensor_co2 = MH_Z19(Pin(UART_TX_PIN), Pin(UART_RX_PIN))
    return sensor_co2.read_co2()