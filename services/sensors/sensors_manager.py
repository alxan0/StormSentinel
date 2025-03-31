import asyncio
from services.sensors.temp_humidity_sensor import read_temp_humidity
#from sensors.co2_sensor import read_co2
#from sensors.dust_sensor import read_dust

def inject_state(local):
    global acu_data, local_data
    local_data = local

async def read_all_loop():
    while True:
        temp, humidity = read_temp_humidity()
        #co2 = read_co2()
        #dust = read_dust()
        
        local_data["sensor_temp"] = temp
        local_data["sensor_humidity"] = humidity
        #local_data["sensor_co2"] = co2
        #local_data["sensor_dust"] = dust
        await asyncio.sleep(5)
