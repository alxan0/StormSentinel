import ujson

COORDINATES_FILE = "location.json"

def save_coordinates(coordinates):
    try:
        with open(COORDINATES_FILE, "w") as file:
            ujson.dump(coordinates, file)
        print(f"Coordinates saved: {coordinates.get('latitude')}, {coordinates.get('longitude')}")
    except Exception as e:
        print(f"Error saving coordinates: {e}")

def load_coordinates():
    try:
        with open(COORDINATES_FILE, "r") as file:
            data = ujson.load(file)
            return data.get("latitude"), data.get("longitude")
    except (OSError, ValueError):
        print("No valid coordinates found.")
        return 0, 0
