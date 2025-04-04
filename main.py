import asyncio
from utime import sleep
from core.wifi import init_wifi
from core.display import init_display
from services.display_service import show_boot_screen
import services.sensors.sensors_manager as sensors_manager
import services.display_manager as display_manager
import utils.website as website
import config.secrets as secrets

# AcuWeather Data
acu_data = {
    "acu_temp": 300,
    "acu_condition": "S",
    "acu_humidity": -1,
    "acu_wind_speed": 40,
    "acu_chance_of_rain": -10,
    "acu_precipitation_type": "None"
}

# Local Sensor Data
local_data = {
    "sensor_temp": 300,
    "sensor_humidity": 2,
    "sensor_co2": 1,
    "sensor_dust": -1
}

async def main():    
    if not init_wifi(secrets.ssid, secrets.password):
        print('Exiting program.')
        return
    
    tft = init_display()
    
    sensors_manager.inject_state(local_data)
    asyncio.create_task(sensors_manager.read_all_loop())

    # Later update readings
    # Get a first set of data
    website.inject_state(acu_data, local_data)
    await website.init_app_state() # TODO add error check

    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(website.handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    
    show_boot_screen(tft)
    display_manager.inject_state(acu_data, local_data)
    asyncio.create_task(display_manager.display_loop(tft))


# Create an Event Loop
loop = asyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')
