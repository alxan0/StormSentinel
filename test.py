import time
from machine import Pin
import dht

sensor = dht.DHT22(Pin(2))  # GPIO2 = GP2

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("Temp: {:.1f}°C, Humidity: {:.1f}%".format(temp, hum))
    except OSError as e:
        print("Sensor error:", e)
    
    time.sleep(4)
