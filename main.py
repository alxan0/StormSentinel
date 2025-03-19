import asyncio
from utime import sleep
from core.wifi import init_wifi
import utils.website as website
import config.secrets as secrets

async def main():    
    if not init_wifi(secrets.ssid, secrets.password):
        print('Exiting program.')
        return
    
    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(website.handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    
    while True:
        await asyncio.sleep(5)


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
