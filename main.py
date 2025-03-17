from utime import sleep
from blink import ToggleOnBoardLed

def main():
    while True:
        try:
            ToggleOnBoardLed()
            sleep(1) # sleep 1sec
        except KeyboardInterrupt:
            print("Finished.")
            break

main()
