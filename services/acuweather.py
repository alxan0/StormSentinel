import asyncio
import urequests
import json
from config.secrets import ACU_API_KEY as API_KEY

# Get the location key from coordinates
async def get_location_key(latitude, longitude):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_KEY}&q={latitude},{longitude}"
    try:
        await asyncio.sleep(0)
        response = urequests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data['Key']  # Location Key
        else:
            print(f"Error fetching location key: {data['Message']}")
            return None
    except Exception as e:
        print(f"Error connecting to AccuWeather API: {e}")
        return None

# Get the temperature using the location key
async def get_temperature(location_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true&metric=true"
    try:
        await asyncio.sleep(0)
        response = urequests.get(url)
        data = response.json()
        if response.status_code == 200:
            temperature = data[0]['Temperature']['Metric']['Value']
            print(f"Temperature is {temperature}C")
            return temperature
        else:
            print(f"Error fetching temperature data: {data['Message']}")
            return None
    except Exception as e:
        print(f"Error connecting to AccuWeather API: {e}")
        return None

# Combine the two functions
async def get_weather(latitude, longitude):
    location_key = await get_location_key(latitude, longitude)
    if location_key:
        return await get_temperature(location_key)
    else:
        print("Failed to retrieve location key.")
        return None
