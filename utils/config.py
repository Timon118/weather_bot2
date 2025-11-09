# Загрузка конфигурации из .env
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_CATALOG_ID = os.getenv("YANDEX_CATALOG_ID")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Проверка обязательных переменных
if not all([TELEGRAM_BOT_TOKEN, YANDEX_API_KEY, YANDEX_CATALOG_ID, OPENWEATHER_API_KEY]):
    raise ValueError("Не указаны обязательные переменные окружения.")