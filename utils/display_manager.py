import asyncio
from services.display_service import show_readings, clear_screen

def inject_state(acu, local):
    global acu_data, local_data
    acu_data = acu
    local_data = local

async def display_loop(tft):
    while True:
        clear_screen(tft)
        show_readings(tft, "Storm Sentinel", 0, 0)

        # === AccuWeather Section ===
        show_readings(tft, "AccuWeather:", 0, 20)
        show_readings(tft, f"T: {acu_data.get('acu_temp', '--')}C", 10, 35)
        show_readings(tft, f"H: {acu_data.get('acu_humidity', '--')}%", 10, 50)

        # === Local Sensor Section ===
        show_readings(tft, "Local Sensors:", 0, 70)
        show_readings(tft, f"T: {local_data.get('sensor_temp', '--')}C", 10, 85)
        show_readings(tft, f"CO2: {local_data.get('sensor_co2', '--')}ppm", 10, 100)

        await asyncio.sleep(10)
