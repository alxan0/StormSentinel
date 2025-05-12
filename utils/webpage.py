def webpage(
    led_state,
    air_quality_warning, 
    latitude, 
    longitude, 
    accu_temp, 
    accu_condition, 
    accu_humidity,            
    accu_wind_speed,          
    accu_chance_of_rain,      
    accu_precipitation_type,  
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
    html = html.replace("{{accu_temp}}", str(accu_temp))
    html = html.replace("{{accu_condition}}", str(accu_condition))
    html = html.replace("{{accu_humidity}}", str(accu_humidity))        
    html = html.replace("{{accu_wind_speed}}", str(accu_wind_speed))      
    html = html.replace("{{accu_chance_of_rain}}", str(accu_chance_of_rain))
    html = html.replace("{{accu_precipitation_type}}", str(accu_precipitation_type)) 
    html = html.replace("{{gemini_insights}}", str(gemini_insights))
    html = html.replace("{{led_state}}", str(led_state))
    html = html.replace("{{air_quality_warning}}", str(air_quality_warning))


    if latitude and longitude is not 0:
        html = html.replace("{{latitude}}", str(latitude))
        html = html.replace("{{longitude}}", str(longitude))
    else:
        html = html.replace("{{latitude}}", "latitude")
        html = html.replace("{{longitude}}", "longitude")

    return html