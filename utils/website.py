import asyncio
import socket
import ujson as json
from machine import Pin
from utils.webpage import webpage
from services.acuweather import get_weather
from services.geminiAsk import ask_gemini
from utils.location import save_coordinates, load_coordinates

# Create an LED output
led_control = Pin("LED", Pin.OUT)

# These get set by init_app_state()
app_state = {}
acu_data = {}
local_data = {}

def inject_state(app, acu, local):
    global app_state, acu_data, local_data
    app_state = app
    acu_data = acu
    local_data = local

async def init_app_state():
    app_state["latitude"], app_state["longitude"], _ = await load_coordinates()
    if app_state["latitude"] != 0 and app_state["longitude"] != 0:
        acu_data.update(await get_weather(app_state["latitude"], app_state["longitude"]))
    else:
        acu_data["acu_temp"] = "Invalid or missing coordinates"

async def handle_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)

    # Skip headers
    while await reader.readline() != b"\r\n":
        pass

    request = str(request_line, "utf-8").split()[1]
    print("Path:", request)

    # Serve CSS
    if request == "/home.css":
        try:
            with open("static/home.css", "r") as css_file:
                css_content = css_file.read()
            writer.write("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n".encode() + css_content.encode())
        except Exception as e:
            print("CSS load error:", e)
            writer.write("HTTP/1.1 404 Not Found\r\n\r\n".encode())

    # LED control
    elif request.startswith("/lighton"):
        led_control.value(1)
        app_state["led_state"] = "ON"
    elif request.startswith("/lightoff"):
        led_control.value(0)
        app_state["led_state"] = "OFF"

    # Air quality warning
    elif request.startswith("/disableairqualitywarnings"):
        app_state["air_quality_warning"] = "OFF"
    elif request.startswith("/enableairqualitywarnings"):
        app_state["air_quality_warning"] = "ON"    

    # Save coordinates
    elif request.startswith("/savecoordinates"):
        qs = request.split("?", 1)[1]
        coords = dict(param.split("=") for param in qs.split("&") if "=" in param)
        await save_coordinates(coords)
        app_state["latitude"], app_state["longitude"], _ = await load_coordinates()

    # Get weather
    elif request.startswith("/getweather"):
        if app_state["latitude"] and app_state["longitude"]:
            acu_data.update(await get_weather(app_state["latitude"], app_state["longitude"]))
        else:
            acu_data["acu_temp"] = "Invalid or missing coordinates"

    # Get Gemini insight
    elif request.startswith("/getinsight"):
        if acu_data.get("acu_temp") != 300:
            geminiResponse = await ask_gemini(acu_data)
        else:
            geminiResponse = "Va rog sa generati temperatura mai intai"
        app_state["gemini_insights"] = geminiResponse

    # Sensor-data JSON endpoint
    elif request.startswith("/sensor-data"):
        payload = {
            "temp":     local_data["sensor_temp"],
            "humidity": local_data["sensor_humidity"],
            "co2":      local_data["sensor_co2"],
            "dust":     local_data["sensor_dust"],
        }
        body = json.dumps(payload)
        writer.write(
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: application/json\r\n"
            b"Access-Control-Allow-Origin: *\r\n"
            b"\r\n" +
            body.encode()
        )
        await writer.drain()
        await writer.wait_closed()
        return  # stop here—don't render HTML

    # Finally, render the main HTML page
    response = webpage(
        app_state["led_state"],
        app_state["air_quality_warning"],
        app_state["latitude"], 
        app_state["longitude"],
        acu_data.get("acu_temp",""),
        acu_data.get("acu_condition",""),
        acu_data.get("acu_humidity",""),        
        acu_data.get("acu_wind_speed",""),         
        acu_data.get("acu_chance_of_rain",""),     
        acu_data.get("acu_precipitation_type",""),
        local_data.get("sensor_temp",""),
        local_data.get("sensor_humidity",""),
        local_data.get("sensor_co2",""),
        local_data.get("sensor_dust",""),
        app_state["gemini_insights"]
    )
    writer.write(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response}".encode())

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")
