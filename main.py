import asyncio
from utime import sleep
from wifi import init_wifi
import website
import secrets

async def main():    
    if not init_wifi(secrets.ssid, secrets.password):
        print('Exiting program.')
        return
    
    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(website.handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    
    while True:
        # Add other tasks that you might need to do in the loop
        await asyncio.sleep(5)
        print('This message will be printed every 5 seconds')
        

# Create an Event Loop
loop = asyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')
