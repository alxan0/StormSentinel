from lib.ST7735 import TFT,TFTColor
from lib.sysfont import sysfont

def clear_screen(tft):
    tft.fill(TFT.BLACK)

def show_readings(tft, text, x, y, color=TFT.WHITE, font=sysfont, size=1):
    tft.text((x, y), text, color, font, size)

def format_val(value, unit="", invalid_values=(300, -1, "None", None)):
    if value in invalid_values:
        return "--"
    return f"{value}{unit}"

def center_text(tft, text, y, color=TFT.WHITE, size=1):
        char_width = 5 * size
        text_width = len(text) * char_width
        x = (128 - text_width) // 2
        tft.text((x, y), text, color, sysfont, size)

def show_image(tft, filename, mode="top", y=0, max_width=128, max_height=128):
    """
    Display a 24-bit uncompressed BMP from the /assets folder.
    mode: 'top' or 'full'
        - 'top': center image horizontally, aligned to top
        - 'full': draw image from (0,0) and crop to fit screen
    """
    try:
        with open(f"assets/{filename}", 'rb') as f:
            if f.read(2) != b'BM':
                print("Not a valid BMP file.")
                return

            f.read(8)  # Skip file size & reserved
            offset = int.from_bytes(f.read(4), 'little')
            f.read(4)  # DIB header size
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            f.read(2)  # Planes
            depth = int.from_bytes(f.read(2), 'little')
            compression = int.from_bytes(f.read(4), 'little')

            if depth != 24 or compression != 0:
                print("Unsupported BMP format. Must be 24-bit uncompressed.")
                return

            rowsize = (width * 3 + 3) & ~3
            flip = height > 0
            height = abs(height)

            w = min(width, max_width)
            h = min(height, max_height)

            # Position logic
            if mode == "full":
                x, y = 0, y
            else:  # mode == "top"
                x = (max_width - w) // 2
                y = y

            tft._setwindowloc((x, y), (x + w - 1, y + h - 1))

            for row in range(h):
                pos = offset + (height - 1 - row if flip else row) * rowsize
                if f.tell() != pos:
                    f.seek(pos)
                for col in range(w):
                    bgr = f.read(3)
                    color = TFTColor(bgr[2], bgr[1], bgr[0])
                    tft._pushcolor(color)

    except Exception as e:
        print("Error loading image:", e)


def show_boot_screen(tft):
    tft.fill(TFT.BLACK)
    image_name = "boot_screen.bmp"
    show_image(tft, image_name, mode="full")

def show_error_screen(tft, message, error_type="Error"):
    tft.fill(TFT.BLACK)

    image_name = f"{error_type.lower().replace(' ', '_')}.bmp"

    try:
        show_image(tft, image_name, mode="top", y=10)
    except Exception as e:
        print("Image load failed:", e)

    # Draw error text below the image
    title_color = TFT.RED
    if error_type == "Wifi Error":
        title_color = TFT.BLUE
    elif error_type == "Sensor Error":
        title_color = TFT.GREEN
    elif error_type == "API Error":
        title_color = TFT.PURPLE

    tft.text((10, 80), f"{error_type}", title_color, sysfont, 2)
    tft.text((10, 105), message, TFT.YELLOW, sysfont, 1)



def show_summary_screen(tft, acu_data, local_data):
    show_readings(tft, "Storm Sentinel", 0, 0, color=TFT.YELLOW)

    # === AccuWeather Section ===
    show_readings(tft, "AccuWeather:", 0, 20)
    show_readings(tft, f"T: {format_val(acu_data.get('acu_temp'), 'C')}", 10, 35)
    show_readings(tft, f"H: {format_val(acu_data.get('acu_humidity'), '%')}", 10, 50)

    # === Local Sensor Section ===
    show_readings(tft, "Local Sensors:", 0, 70)
    show_readings(tft, f"T: {format_val(local_data.get('sensor_temp'), 'C')}", 10, 85)
    show_readings(tft, f"CO2: {format_val(local_data.get('sensor_co2'), 'ppm')}", 10, 100)


def show_accuweather_screen(tft, acu_data, _):
    show_readings(tft, "AccuWeather", 0, 0, color=TFT.CYAN)
    show_readings(tft, f"Temp: {format_val(acu_data.get('acu_temp'), 'C')}", 10, 30)
    show_readings(tft, f"Humidity: {format_val(acu_data.get('acu_humidity'), '%')}", 10, 45)
    show_readings(tft, f"Wind: {format_val(acu_data.get('acu_wind_speed'), ' km/h')}", 10, 60)
    show_readings(tft, f"Rain: {format_val(acu_data.get('acu_chance_of_rain'), '%')}", 10, 75)
    show_readings(tft, f"Cond: {acu_data.get('acu_condition', '--')}", 10, 90)
    show_readings(tft, f"Precip: {acu_data.get('acu_precipitation_type', '--')}", 10, 105)

def show_local_sensor_screen(tft, _, local_data):
    show_readings(tft, "Local Sensors", 0, 0, color=TFT.GREEN)
    show_readings(tft, f"Temp: {format_val(local_data.get('sensor_temp'), 'C')}", 10, 30)
    show_readings(tft, f"Humidity: {format_val(local_data.get('sensor_humidity'), '%')}", 10, 45)
    show_readings(tft, f"CO2: {format_val(local_data.get('sensor_co2'), 'ppm')}", 10, 60)
    show_readings(tft, f"Dust: {format_val(local_data.get('sensor_dust'), ' µg/m³')}", 10, 75)