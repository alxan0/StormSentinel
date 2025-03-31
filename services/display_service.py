import time
import math
from lib.ST7735 import TFT
from lib.sysfont import sysfont

def show_boot_screen(tft):
    tft.fill(TFT.BLACK)
    tft.text((10, 20), "Weather Station", TFT.CYAN, sysfont, 2)
    tft.text((10, 50), "Starting up...", TFT.GREEN, sysfont, 1)

def clear_screen(tft):
    tft.fill(TFT.BLACK)

def show_readings(tft, text, x, y, color=TFT.WHITE, font=sysfont, size=1):
    tft.text((x, y), text, color, font, size)