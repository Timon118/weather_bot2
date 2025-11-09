# Работа с Yandex GPT: извлечение города и рекомендации по погоде
import requests
import json
from utils.config import YANDEX_API_KEY, YANDEX_CATALOG_ID

YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {YANDEX_API_KEY}",
    "x-folder-id": YANDEX_CATALOG_ID,
}

def extract_and_translate_city(user_input: str) -> str | None:
    """
    Использует Yandex GPT для извлечения названия города из текста и перевода на английский.
    Возвращает строку с названием города на английском (например, "Moscow").
    """
    prompt = f"""
    Извлеки из следующего сообщения пользователя только название города и переведи его на английский язык.
    Верни ТОЛЬКО название города на английском языке, ничего больше. Если город не найден, вернуть "None".
    Сообщение пользователя: "{user_input}"
    """

    payload = {
        "modelUri": f"gpt://{YANDEX_CATALOG_ID}/yandexgpt/rc",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "256"
        },
        "messages": [
            {"role": "system", "text": "Ты — ассистент, который извлекает и переводит названия городов."},
            {"role": "user", "text": prompt}
        ]
    }

    try:
        response = requests.post(YANDEX_GPT_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        city = result["result"]["alternatives"][0]["message"]["text"].strip()
        return city if city.lower() != "none" else None
    except Exception as e:
        print(f"[YandexGPT Error] extract_and_translate_city: {e}")
        return None


def generate_clothing_recommendation(city: str, weather_desc: str, temp_celsius: float) -> str:
    """
    Генерирует рекомендацию по одежде на основе описания погоды и температуры.
    """
    prompt = f"""
    Ты — эксперт по погоде и стилю. Посоветуй, какую одежду надеть сегодня в {city}.
    Погодные условия: {weather_desc}, температура: {temp_celsius:.1f}°C.
    Сделай рекомендацию кратко (1-3 предложения), дружелюбно, и практично.
    """

    payload = {
        "modelUri": f"gpt://{YANDEX_CATALOG_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.4,
            "maxTokens": "200"
        },
        "messages": [
            {"role": "system", "text": "Ты даёшь практические советы по выбору одежды с учётом погоды."},
            {"role": "user", "text": prompt}
        ]
    }

    try:
        response = requests.post(YANDEX_GPT_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["result"]["alternatives"][0]["message"]["text"].strip()
    except Exception as e:
        return f"⚠️ Не удалось сгенерировать рекомендацию: {e}"