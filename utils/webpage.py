def webpage(
    state, 
    latitude, 
    longitude, 
    acu_temp, 
    acu_condition, 
    acu_humidity,            
    acu_wind_speed,          
    acu_chance_of_rain,      
    acu_precipitation_type,  
    sensor_temp, 
    sensor_humidity, 
    sensor_co2,
    sensor_dust,
    gemini_insights
):
    with open("static/home.html", "r") as file:
        html = file.read()

    # Replace placeholders with dynamic data
    html = html.replace("{{sensor_temp}}", str(sensor_temp))
    html = html.replace("{{sensor_humidity}}", str(sensor_humidity))
    html = html.replace("{{sensor_co2}}", str(sensor_co2))
    html = html.replace("{{sensor_dust}}", str(sensor_dust))
    html = html.replace("{{acu_temp}}", str(acu_temp))
    html = html.replace("{{acu_condition}}", str(acu_condition))
    html = html.replace("{{acu_humidity}}", str(acu_humidity))        
    html = html.replace("{{acu_wind_speed}}", str(acu_wind_speed))      
    html = html.replace("{{acu_chance_of_rain}}", str(acu_chance_of_rain))
    html = html.replace("{{acu_precipitation_type}}", str(acu_precipitation_type)) 
    html = html.replace("{{gemini_insights}}", str(gemini_insights))
    html = html.replace("{{state}}", str(state))

    if latitude and longitude is not 0:
        html = html.replace("{{latitude}}", str(latitude))
        html = html.replace("{{longitude}}", str(longitude))
    else:
        html = html.replace("{{latitude}}", "latitude")
        html = html.replace("{{longitude}}", "longitude")

    return html