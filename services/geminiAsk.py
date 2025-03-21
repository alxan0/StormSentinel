import network
import urequests
import ujson
import time

# 🔹 CONFIGURARE WiFi
#SSID = "DIGI-xM66"  # 🟢 Înlocuiește cu numele rețelei
#PASSWORD = "NR4zCwzS3s"  # 🟢 Înlocuiește cu parola

SSID = "Vand tuica"  # 🟢 Înlocuiește cu numele rețelei
PASSWORD = "marianul"  # 🟢 Înlocuiește cu parola

# Conectare la WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Conectare la WiFi...")
    time.sleep(1)

print("✅ Conectat la rețea:", wlan.ifconfig())

# 🔹 CONFIGURARE API GEMINI
API_KEY = "AIzaSyAjFhm82AlPAamAT2EAVcKedYYqo9tVrS4"  # 🛑 Nu împărtăși cheia API public!
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def ask_gemini(prompt):
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
            print("🔹 Răspuns Gemini:", reply)
        else:
            print("⚠️ Eroare în răspunsul API:", result)

    except Exception as e:
        print("⚠️ Eroare:", e)

# 🔹 Test API Gemini
ask_gemini("Scrie decat o cifra/doua cifre care sa semnifice cate grade sunt acum in Timisoara. Niciun alt caracter sau cuvant sau propozitie. De exemplu daca acum sunt 13 grade tu o sa scrii \"13\", iar daca sunt -3 o sa scrii \"-3\" ")
