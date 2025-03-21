import network
import urequests
import ujson
import time

# 🔹 CONFIGURARE API GEMINI
API_KEY = "AIzaSyAjFhm82AlPAamAT2EAVcKedYYqo9tVrS4"  # 🛑 Nu împărtăși cheia API public!
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"


async def ask_gemini(degrees):
    prompt = "Afara sunt " + str(degrees) + " grade celsius. Spune-mi in maxim 30 de cuvinte cum sa ma imbrac."
    try:
        headers = {
            "Content-Type": "application/json"
        }

        # ✅ JSON FORMATAT CORECT
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
        print("📤 Trimit către API:", json_data)  # 🔍 Debugging

        # ✅ FACEM REQUEST CĂTRE API (LIPSEA ACEASTĂ LINIE)
        response = urequests.post(GEMINI_URL, headers=headers, data=json_data)

        # ✅ Verificăm răspunsul API
        print("📥 Răspuns brut API:", response.text)  # 🔍 Debugging

        result = response.json()
        response.close()

        # ✅ Extragem răspunsul AI
        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        #  print("🔹 Răspuns Gemini:", reply)
        else:
            print("⚠️ Eroare în răspunsul API:", result)
        return reply
    except Exception as e:
        print("⚠️ Eroare:", e)

# 🔹 Test API Gemini
# ask_gemini(3)

