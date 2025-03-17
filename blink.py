from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

def ToggleOnBoardLed():
    pin.toggle()
    print("LED toggled...")


