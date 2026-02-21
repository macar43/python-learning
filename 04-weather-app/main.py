# ============================================
# Wetter-App mit OpenWeatherMap API
# ============================================

import requests
import json
from datetime import datetime

class WeatherApp:
    """Wetter-App die aktuelle Wetterdaten abruft"""
    
    def __init__(self):
        """Initialisiert die App"""
        # API-Key von OpenWeatherMap (kostenlos!)
        # Registriere dich: https://openweathermap.org/api
        self.api_key = "77c8b3b1c9d5f8a01b2795136d1c40fd"  # Du musst diesen eintragen!
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.units = "metric"  # Celsius statt Fahrenheit
    
    def get_weather(self, city):
        """Holt Wetterdaten für eine Stadt"""
        
        try:
            # Parameter für die API
            params = {
                "q": city,
                "appid": self.api_key,
                "units": self.units,
                "lang": "de"  # Deutsche Beschreibungen
            }
            
            # HTTP-Request zur API
            response = requests.get(self.base_url, params=params)
            
            # Überprüfe ob Request erfolgreich war
            if response.status_code != 200:
                print(f"❌ Fehler: Stadt '{city}' nicht gefunden!")
                return None
            
            # Wandle JSON-Response in Python-Dictionary um
            data = response.json()
            return data
        
        except requests.exceptions.ConnectionError:
            print("❌ Keine Internetverbindung!")
            return None
        except Exception as e:
            print(f"❌ Fehler beim API-Aufruf: {str(e)}")
            return None
    
    def display_weather(self, data):
        """Zeigt Wetterdaten schön formatiert an"""
        
        if data is None:
            return
        
        # Extrahiere Daten aus dem JSON
        city = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"].capitalize()
        icon = data["weather"][0]["main"]
        
        # Emoji basierend auf Wetter-Icon
        emoji_map = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️"
        }
        emoji = emoji_map.get(icon, "🌍")
        
        # Formatierte Ausgabe
        print("\n" + "="*50)
        print(f"{emoji} WETTER IN {city.upper()}, {country}")
        print("="*50)
        print(f"🌡️  Temperatur:      {temperature}°C")
        print(f"🤔 Gefühlt wie:      {feels_like}°C")
        print(f"💧 Luftfeuchtigkeit: {humidity}%")
        print(f"🔽 Luftdruck:        {pressure} hPa")
        print(f"💨 Windgeschwindigkeit: {wind_speed} m/s")
        print(f"📝 Beschreibung:     {description}")
        print("="*50 + "\n")
    
    def get_forecast_simple(self, data):
        """Gibt einfache Vorhersage basierend auf Temperatur"""
        
        if data is None:
            return
        
        temp = data["main"]["temp"]
        
        print("📊 Einfache Vorhersage:")
        if temp < 0:
            print("❄️  Es ist sehr kalt - Warm anziehen!")
        elif temp < 10:
            print("🧥 Es ist kalt - Jacke mitnehmen!")
        elif temp < 20:
            print("🌤️  Angenehm mild - Normales Wetter")
        elif temp < 30:
            print("☀️  Warm - Leichte Kleidung reicht")
        else:
            print("🔥 Sehr heiß - Viel trinken und Sonnenschutz!")
        print()

def main():
    """Hauptprogramm"""
    
    app = WeatherApp()
    
    # Überprüfe ob API-Key eingegeben wurde
    if app.api_key == "DEIN_API_KEY_HIER":
        print("⚠️  WICHTIG: API-Key muss eingegeben werden!")
        print("1. Gehe zu: https://openweathermap.org/api")
        print("2. Registriere dich (kostenlos)")
        print("3. Kopiere deinen API-Key")
        print("4. Ersetze 'DEIN_API_KEY_HIER' in diesem Script\n")
        return
    
    print("🌍 Willkommen zur Wetter-App!")
    print("Gib eine Stadt ein um das Wetter zu sehen.\n")
    
    while True:
        city = input("Stadt eingeben (oder 'exit' zum Beenden): ").strip()
        
        if city.lower() in ["exit", "quit", "q"]:
            print("\n👋 Auf Wiedersehen!")
            break
        
        if city == "":
            print("❌ Bitte eine Stadt eingeben!\n")
            continue
        
        # Wetterdaten abrufen
        print(f"⏳ Laden für '{city}'...\n")
        weather_data = app.get_weather(city)
        
        # Daten anzeigen
        if weather_data:
            app.display_weather(weather_data)
            app.get_forecast_simple(weather_data)

# ============================================
# Programm starten
# ============================================
if __name__ == "__main__":
    main()