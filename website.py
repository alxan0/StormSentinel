import asyncio
import socket
from machine import Pin
from webpage import webpage
from acuweather import get_weather

# Create several LEDs
led_control = Pin("LED", Pin.OUT)

# Initialize variables
state = "OFF"
random_value = 0
weather = 0

# Asynchronous functio to handle client's requests
async def handle_client(reader, writer):
    global state
    global weather

    print("Client connected")
    request_line = await reader.readline()
    print('Request:', request_line)
    
    # Skip HTTP request headers
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, 'utf-8').split()[1]
    print('Request:', request)
    
    # Process the request and update variables
    if request == '/lighton?':
        print('LED on')
        led_control.value(1)
        state = 'ON'
    elif request == '/lightoff?':
        print('LED off')
        led_control.value(0)
        state = 'OFF'
    elif request.startswith('/coordinates?'):
        print("Let's see...")
        try:
            query_string = request.split('?')[1]
            params = dict(param.split('=') for param in query_string.split('&') if '=' in param)

            latitude = params.get('latitude')
            longitude = params.get('longitude')

            if latitude and longitude:
                temp = await get_weather(latitude, longitude)
                weather = f"Temperature at {latitude}, {longitude} is {temp}C"
            else:
                weather = "Invalid or missing coordinates."

        except IndexError:
            print("No value provided.")

    # Generate HTML response
    response = webpage(random_value, state, weather)  

    # Send the HTTP response and close the connection
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')