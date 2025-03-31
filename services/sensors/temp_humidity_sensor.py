import dht
from machine import Pin

# Configure the DHT22 pin (update to your pin)
DHT_PIN = 2  # Example: GPIO15
dht_sensor = dht.DHT22(Pin(DHT_PIN))

def read_temp_humidity():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except OSError as e:
        print("Failed to read DHT22 sensor:", e)
        return 0, 0  # fallback values
