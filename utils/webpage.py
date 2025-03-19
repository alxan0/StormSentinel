def webpage(state, latitude, longitude, acu_temp, acu_condition, sensor_temp, sensor_humidity, sensor_co2,  gemini_insights):
    with open("static/home.html", "r") as file:
        html = file.read()

    # Replace placeholders with dynamic data
    html = html.replace("{{sensor_temp}}", str(sensor_temp))
    html = html.replace("{{sensor_humidity}}", str(sensor_humidity))
    html = html.replace("{{sensor_co2}}", str(sensor_co2))
    html = html.replace("{{acu_temp}}", str(acu_temp))
    html = html.replace("{{acu_condition}}", str(acu_condition))
    html = html.replace("{{gemini_insights}}", str(gemini_insights))
    html = html.replace("{{state}}", str(state))

    if latitude and longitude is not 0:
        html = html.replace("{{latitude}}", str(latitude))
        html = html.replace("{{longitude}}", str(longitude))
    else:
        html = html.replace("{{latitude}}", "latitude")
        html = html.replace("{{longitude}}", "longitude")

    return html