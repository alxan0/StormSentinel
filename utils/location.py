import ujson

COORDINATES_FILE = "location.json"

async def save_coordinates(coordinates):
    try:
        from services.acuweather import get_location_key
        print(">>>>>>>>>test")
        coordinates["location_key"] = await get_location_key(coordinates.get("latitude"), coordinates.get("longitude"))
        with open(COORDINATES_FILE, "w") as file:
            ujson.dump(coordinates, file)
        print(f"Coordinates saved: {coordinates.get('latitude')}, {coordinates.get('longitude')}, {coordinates.get("location_key")}")
    except Exception as e:
        print(f"Error saving coordinates: {e}")

async def load_coordinates():
    try:
        with open(COORDINATES_FILE, "r") as file:
            data = ujson.load(file)
            return data.get("latitude"), data.get("longitude"), data.get("location_key")
    except (OSError, ValueError):
        print("No valid coordinates found.")
        return 0, 0, 0
    

