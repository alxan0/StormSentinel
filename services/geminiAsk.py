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
        f" Spune-mi in maxim 50 de cuvinte cum sa ma imbrac."
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

        json_data = ujson.dumps(data).encode('utf-8')
        # print("Send to API:", json_data)  # Debugging

        response = urequests.post(GEMINI_URL, headers=headers, data=json_data)
        print("GeminiAPI:", response.text)  # Debugging

        result = response.json()
        response.close()

        # Extract the reply
        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        #  print("Gemini's reply:", reply)
        else:
            print("Gemini API error:", result)
        return reply
    except Exception as e:
        print("Error in geminiAsk:", e)

