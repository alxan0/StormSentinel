from machine import UART, Pin
import time

# Setează UART (verifică pinii tăi pentru placa ta)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

def read_co2():
    cmd = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'  # comandă standard de citire CO₂
    uart.write(cmd)
    time.sleep(0.1)
    if uart.any():
        response = uart.read(9)
        if response and response[0] == 0xFF and response[1] == 0x86:
            co2 = response[2] * 256 + response[3]
            return co2
    return None

# Buclă de citire CO₂
while True:
    co2 = read_co2()
    if co2:
        print("CO₂:", co2, "ppm")
    else:
        print("Eroare la citire sau senzor inactiv.")
    time.sleep(2)
