import asyncio
import socket
from machine import Pin
from utils.webpage import webpage
from services.acuweather import get_weather
from utils.location import save_coordinates, load_coordinates

# Create several LEDs
led_control = Pin("LED", Pin.OUT)

# Centralized data dictionary
app_state = {
    "state": "OFF",
    "latitude": 0,
    "longitude": 0,
    "acu_temp": 300,
    "sensor_temp": 300,
    "sensor_humidity": 2,
    "sensor_co2": 1,
    "acu_condition": "S",
    "gemini_insights": "a"
}

# Fetch first set of data
async def init_app_state():
    app_state["latitude"], app_state["longitude"] = load_coordinates()
    if app_state["latitude"] and app_state["longitude"] is not 0:
        app_state["acu_temp"] = await get_weather(app_state["latitude"], app_state["longitude"])
    else:
        app_state["acu_temp"] = "Invalid or missing coordinates"

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
            save_coordinates(coordinates)
        except IndexError:
            print("No value provided.")

        app_state["latitude"], app_state["longitude"] = load_coordinates()

        if app_state["latitude"] and app_state["longitude"] is 0:
            app_state["acu_temp"] = "Invalid or missing coordinates"
    
    # Get weather from the AcuWeather API
    elif request.startswith('/getweather?'):
        try:
            if app_state["latitude"] and app_state["longitude"] is not 0:
                app_state["acu_temp"] = await get_weather(app_state["latitude"], app_state["longitude"]) # TODO check if the coord. exists
            else:
                app_state["acu_temp"] = "Invalid or missing coordinates"
        except IndexError:
            print("No value provided.")
    
    # Logic for serving the main website
    response = webpage(
            app_state["state"],
            app_state["latitude"], 
            app_state["longitude"],
            app_state["acu_temp"],
            app_state["acu_condition"],
            app_state["sensor_temp"],
            app_state["sensor_humidity"],
            app_state["sensor_co2"],
            app_state["gemini_insights"]
        )
    writer.write(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response}".encode())

    #Close the connection
    await writer.drain()
    await writer.wait_closed()
    print("Client Disconnected")