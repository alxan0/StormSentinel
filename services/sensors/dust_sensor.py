from machine import Pin, ADC
import time

# Configurare pini
led_pin = Pin(15, Pin.OUT)       # controlul LED-ului intern al senzorului
adc_pin = ADC(26)                # ADC0 pe Raspberry Pi Pico (GPIO26)

def read_dust():
    led_pin.value(1)             # Aprinde LED-ul
    time.sleep_us(280)          # Așteaptă conform datasheet
    adc_val = adc_pin.read_u16()  # Citește valoarea ADC (16 biți)
    time.sleep_us(40)
    led_pin.value(0)             # Oprește LED-ul
    time.sleep_ms(10)           # Timp de repaus
    return adc_val

while True:
    raw = read_dust()
    voltage = (raw / 65535.0) * 3.3  # Conversie la tensiune (0-3.3V)
    dust_density = max((voltage - 0.6) / 0.5, 0)  # mg/m³, simplificat

    print("ADC:", raw, "Voltage: {:.2f} V".format(voltage),
          "Dust density: {:.2f} mg/m³".format(dust_density))
    time.sleep(1)
