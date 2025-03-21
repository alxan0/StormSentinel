import asyncio
import urequests
import json
from config.secrets import ACU_API_KEY as API_KEY
from utils.location import load_coordinates

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

# Get multiple weather details using the location key
async def get_weather_details(location_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true&metric=true"
    try:
        await asyncio.sleep(0)
        response = urequests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                "acu_temp": data[0].get('Temperature', {}).get('Metric', {}).get('Value', 'Unknown'),
                "acu_condition": data[0].get('WeatherText', 'Unknown'),
                "acu_humidity": data[0].get('RelativeHumidity', -1),  # Default to -1 for invalid data
                "acu_wind_speed": data[0]['Wind']['Speed']['Metric'].get('Value', -1),
                "acu_chance_of_rain": 100 if data[0].get('HasPrecipitation', False) else 0,
                "acu_precipitation_type": data[0].get('PrecipitationType', 'None')
            }

            print(weather_data)  # For debugging purposes
            return weather_data
        else:
            print(f"Error fetching weather data: {data.get('Message', 'Unknown error')}")
            return {
                "acu_temp": "Unknown",
                "acu_condition": "Error",
                "acu_humidity": -1,
                "acu_wind_speed": -1,
                "acu_chance_of_rain": -1,
                "acu_precipitation_type": "Error"
            }
    except Exception as e:
        print(f"Error connecting to AccuWeather API: {e}")
        return {
            "acu_temp": "Unknown",
            "acu_condition": "Unknown",
            "acu_humidity": -1,
            "acu_wind_speed": -1,
            "acu_chance_of_rain": -1,
            "acu_precipitation_type": "Unknown"
        }


# Combine the two functions
async def get_weather(latitude, longitude):
    
    _, _,  saved_location_key = await load_coordinates()
    
    if(saved_location_key):
        location_key = saved_location_key
        print(">>>>Location_key loaded")
    else:
        location_key = await get_location_key(latitude, longitude)

    if location_key:
        return await get_weather_details(location_key)
    else:
        print("Failed to retrieve location key.")
        return dict()
