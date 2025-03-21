import network
import urequests
import ujson
import time
from config.secrets import AI_API_KEY as API_KEY

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"


async def ask_gemini(acu_data):
    prompt = (
        f"Afara sunt {acu_data['acu_temp']} grade Celsius cu "
        f"{acu_data['acu_condition'].lower()}."
        f" Umiditate de {acu_data['acu_humidity']}% si vant de "
        f"{acu_data['acu_wind_speed']} km/h. "
        f"Sanse de ploaie {acu_data['acu_chance_of_rain']}%."
        f" Spune-mi in maxim 30 de cuvinte cum sa ma imbrac."
    )
    try:
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        json_data = ujson.dumps(data).encode('utf-8')  # Convertim corect JSON-ul
        print("Trimit către API:", json_data)  # Debugging

        # Facem REQUEST CĂTRE API (LIPSEA ACEASTĂ LINIE)
        response = urequests.post(GEMINI_URL, headers=headers, data=json_data)

        # Verificăm răspunsul API
        print("Răspuns brut API:", response.text)  # Debugging

        result = response.json()
        response.close()

        # Extragem răspunsul AI
        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        #  print("🔹 Răspuns Gemini:", reply)
        else:
            print("Eroare în răspunsul API:", result)
        return reply
    except Exception as e:
        print("Eroare:", e)

