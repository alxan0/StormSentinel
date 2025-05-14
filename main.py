import asyncio
from core.wifi import init_wifi
from core.display import init_display
from services.display_service import show_boot_screen
import services.sensors.sensors_manager as sensors_manager
import services.display_manager as display_manager
import utils.website as website
import config.secrets as secrets

# Application state
app_state = {
    "led_state": "OFF",
    "air_quality_warning": "ON",
    "latitude": 0,
    "longitude": 0,
    "gemini_insights": ""
}

# AccuWeather Data
accu_data = {
    "accu_temp": 300,
    "accu_condition": "None",
    "accu_humidity": 300,
    "accu_wind_speed": 300,
    "accu_chance_of_rain": 300,
    "accu_precipitation_type": "None"
}

# Local Sensor Data
local_data = {
    "sensor_temp": 300,
    "sensor_humidity": 300,
    "sensor_co2": -1,
    "sensor_dust": -1
}

async def main():  

    tft = init_display() # TODO add error check
    show_boot_screen(tft)
    display_manager.inject_state(accu_data, local_data)
    asyncio.create_task(display_manager.display_loop(tft))

    if not init_wifi(secrets.ssid, secrets.password):
        display_manager.set_display_error("No network found", "Wifi Error")
        print('Exiting program.')
        return
    
    sensors_manager.inject_state(app_state, local_data)
    asyncio.create_task(sensors_manager.read_all_loop())

    # Later update readings
    # Get a first set of data
    website.inject_state(app_state, accu_data, local_data)
    await website.init_app_state() # TODO add error check

    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(website.handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    
    


# Create an Event Loop
loop = asyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occurred: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')
