# 🌩️ Storm Sentinel — Smart Indoor/Outdoor Weather Station

### Description

Storm Sentinel is a smart indoor/outdoor weather station powered by a Raspberry Pi Pico 2W.  
It displays real-time indoor sensor data and live outdoor weather from AccuWeather, both on a web interface and an onboard TFT display.  
It also monitors air quality and alerts you if CO₂ levels become unsafe.

---

### Features

📡 Wi-Fi-enabled with Raspberry Pi Pico 2W  
🌡️ Indoor sensor readings:
- Temperature
- Humidity
- CO₂ levels (with alerts)
- Dust/air quality (optional)
☁️ Outdoor weather from AccuWeather API

📺 Onboard TFT display shows all readings  
🌍 Web interface to monitor readings and control the onboard LED   
💾 Persistent storage for coordinates and location info  

### Technologies & Components

**Hardware:** Raspberry Pi Pico 2W, DHT22 (temperature and humidity), MH-Z19B (CO₂ sensor), GP2Y1010AU0F (dust sensor), ST7735 TFT display  
**Languages:** MicroPython (with asyncio)  
**Frontend:** HTML/CSS served directly from the Pico  
**APIs:**
- AccuWeather (outdoor weather)
- Gemini (Google AI, optional: weather-based recommendations)

### 📸 Screenshots (TODO)

![Web UI]()
![TFT Display]()

### Setup

Clone this repository:
```
git clone https://github.com/your-username/storm-sentinel.git
```
Configure Wi-Fi and API in config/secrets.py:
```py
# Wifi credentials
ssid = "your_wifi_name"
password = "your_wifi_password"

# API keys
ACU_API_KEY = "your_accuweather_api_key"
AI_API_KEY = "your_google_gemini_api_key"
```
Flash main.py to your Pico 2W and reboot.

### Dependencies
- [boochow/MicroPython-ST7735](https://github.com/boochow/MicroPython-ST7735) - ST7735 TFT display driver

