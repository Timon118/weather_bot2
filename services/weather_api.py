# Работа с OpenWeatherMap API
import requests
from utils.config import OPENWEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_by_city(city_en: str) -> dict | None:
    """
    Получает погоду по названию города на английском.
    Возвращает словарь с данными или None в случае ошибки.
    """
    params = {
        "q": city_en,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # температура в °C
        "lang": "ru"        # описание погоды на русском (требуется для GPT)
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "City not found"}
        print(f"[OpenWeather Error] {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"[OpenWeather Exception] {e}")
        return {"error": str(e)}