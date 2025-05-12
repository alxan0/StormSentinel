import asyncio
from services.sensors.temp_humidity_sensor import read_temp_humidity
from services.sensors.co2_sensor import read_co2
from services.display_manager import (
    set_display_error,
    clear_display_error,
    error_state
)
#from services.sensors.dust_sensor import read_dust

def inject_state(local):
    global acu_data, local_data
    local_data = local

TH_CO2_ALERT = 2000     # ppm – trigger when ≥ this value

def update_avg(buf, new_val, size=5):
    buf.append(new_val)
    if len(buf) > size:
        buf.pop(0)
    return sum(buf) / len(buf)

async def read_all_loop():
    temp_buf = []     
    hum_buf  = []
    co2_buf  = []
    #dust_buf = []

    while True:
        temp_raw, hum_raw = read_temp_humidity()
        co2_raw = read_co2()
        #dust_raw = await read_dust()

        temp_avg = update_avg(temp_buf, temp_raw)
        hum_avg  = update_avg(hum_buf,  hum_raw)
        co2_avg  = update_avg(co2_buf,  co2_raw)
        #dust_avg = update_avg(dust_buf,  dust_raw)

        
        local_data["sensor_temp"]     = round(temp_avg, 2)
        local_data["sensor_humidity"] = round(hum_avg, 2)
        local_data["sensor_co2"]      = int(co2_avg)
        #local_data["sensor_dust"]     = int(dust_avg)
        
        alert_active = error_state["type"] == "High CO2"

        if co2_avg >= TH_CO2_ALERT:
            if not alert_active:
                set_display_error(f"{int(co2_avg)} ppm, Dangerous", "High CO2")
        else:
            if alert_active:
                clear_display_error()
        
        await asyncio.sleep(5)
