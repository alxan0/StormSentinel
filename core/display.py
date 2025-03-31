from lib.ST7735 import TFT
from machine import SPI,Pin

def init_display():
    dc = 8
    rst = 12
    cs = 9

    spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
            sck=Pin(10), mosi=Pin(11))
    tft=TFT(spi, aDC=dc, aReset=rst, aCS=cs)
    tft.initr()
    tft.rgb(True)

    return tft

    