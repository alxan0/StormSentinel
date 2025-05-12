import asyncio
from services.display_service import (
    clear_screen,
    show_error_screen,
    show_accuweather_screen,
    show_local_sensor_screen,
    show_summary_screen
)

def inject_state(acu, local):
    global app_state, acu_data, local_data
    acu_data = acu
    local_data = local

error_active = 0

error_state = {
    "msg": "None",
    "type": ""
} 

def set_display_error(msg, type):
    error_state["msg"] = msg
    error_state["type"] = type

def clear_display_error():
    error_state["msg"] = "None"
    error_state["type"] = ""


async def display_loop(tft):

    screen_index = 0
    screens = [
        show_summary_screen,
        show_accuweather_screen,
        show_local_sensor_screen
    ]

    while True:
        if error_state["msg"] is not "None":
            if not error_active:
                error_active = 1
                clear_screen(tft)
                show_error_screen(tft, error_state["msg"], error_state["type"])
        else:
            clear_screen(tft)
            error_active = 0
            current_screen = screens[screen_index]
            current_screen(tft, acu_data, local_data)
            
            screen_index = (screen_index + 1) % len(screens)

        await asyncio.sleep(6)
