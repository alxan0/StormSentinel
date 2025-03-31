import asyncio
import socket
from machine import Pin
from utils.webpage import webpage
from services.acuweather import get_weather
from services.geminiAsk import ask_gemini
from utils.location import save_coordinates, load_coordinates

# Create several LEDs
led_control = Pin("LED", Pin.OUT)

# Application State Data
app_state = {
    "state": "OFF",
    "latitude": 0,
    "longitude": 0,
    "gemini_insights": "a"
}

def inject_state(acu, local):
    global acu_data, local_data
    acu_data = acu
    local_data = local

# Fetch first set of data
async def init_app_state():
    app_state["latitude"], app_state["longitude"], _ = await load_coordinates()
    if app_state["latitude"] != 0 and app_state["longitude"] != 0:
        acu_data.update(await get_weather(app_state["latitude"], app_state["longitude"]))
    else:
        acu_data["acu_temp"] = "Invalid or missing coordinates"


# Asynchronous function to handle client's requests
async def handle_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    
    # Skip HTTP request headers
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, "utf-8").split()[1]
    print("Request:", request)
    
    # Process the request and update variables
    # Logic for serving CSS
    if "GET /home.css" in request_line:
        try:
            with open("static/home.css", "r") as css_file:
                css_content = css_file.read()
            writer.write(f"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n{css_content}".encode())
        except Exception as e:
            print(f"Error loading CSS file: {e}")
            writer.write("HTTP/1.1 404 Not Found\r\n\r\n".encode())

    # LED control
    elif request == "/lighton?":
        print("LED on")
        led_control.value(1)
        app_state["state"] = "ON"
    elif request == "/lightoff?":
        print("LED off")
        led_control.value(0)
        app_state["state"] = "OFF"

    # Save coordinates to a local file
    elif request.startswith("/savecoordinates?"):
        try:
            query_string = request.split("?")[1]
            coordinates = dict(param.split("=") for param in query_string.split("&") if "=" in param)
            await save_coordinates(coordinates)
        except IndexError:
            print("No value provided.")

        app_state["latitude"], app_state["longitude"], _ = await load_coordinates()

        if app_state["latitude"] and app_state["longitude"] is 0:
            acu_data["acu_temp"] = "Invalid or missing coordinates"
    
    # Get weather from the AcuWeather API
    elif request.startswith('/getweather?'):
        try:
            if app_state["latitude"] and app_state["longitude"] is not 0:
                acu_data.update(await get_weather(app_state["latitude"], app_state["longitude"]))
            else:
                acu_data["acu_temp"] = "Invalid or missing coordinates"
        except IndexError:
            print("No value provided.")
    
     # Ask Gemini about the weather
    elif request.startswith('/getinsight?'):
        if acu_data["acu_temp"] != 300:
            geminiResponse = await ask_gemini(acu_data)
        else:
            geminiResponse = "Va rog sa generati temperatura mai intai"
            print(geminiResponse)
        app_state["gemini_insights"] = geminiResponse
        print(geminiResponse)

    # Logic for serving the main website
    response = webpage(
        app_state["state"],
        app_state["latitude"], 
        app_state["longitude"],
        acu_data["acu_temp"],
        acu_data["acu_condition"],
        acu_data["acu_humidity"],        
        acu_data["acu_wind_speed"],         
        acu_data["acu_chance_of_rain"],     
        acu_data["acu_precipitation_type"],
        local_data["sensor_temp"],
        local_data["sensor_humidity"],
        local_data["sensor_co2"],
        app_state["gemini_insights"]
    )

    writer.write(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response}".encode())

    # Close the connection
    await writer.drain()
    await writer.wait_closed()
    print("Client Disconnected")