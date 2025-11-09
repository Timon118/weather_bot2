# Обработчик входящих сообщений
from telegram import Update
from telegram.ext import ContextTypes
from services.yandex_gpt import extract_and_translate_city, generate_clothing_recommendation
from services.weather_api import get_weather_by_city


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start"""
    await update.message.reply_text(
        "🌤 Привет! Я — бот погоды и стиля.\n"
        "Напишите название города, и я подскажу, какую одежду надеть сегодня!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка текстового сообщения от пользователя"""
    user_input = update.message.text.strip()
    chat_id = update.effective_chat.id

    # 1️⃣ Извлекаем и переводим город с помощью Yandex GPT
    city_en = extract_and_translate_city(user_input)
    if not city_en:
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось определить город. Попробуйте ещё раз (например: «Москва», «Paris», «Токио»)."
        )
        return

    # 2️⃣ Получаем погоду по городу
    weather_data = get_weather_by_city(city_en)
    if "error" in weather_data:
        error_msg = weather_data["error"]
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ Ошибка при получении погоды для *{city_en}*: `{error_msg}`",
            parse_mode="Markdown"
        )
        return

    # 3️⃣ Извлекаем данные
    city_name = weather_data["name"]
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    description = weather_data["weather"][0]["description"].lower()
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    # 4️⃣ Генерируем рекомендацию по одежде
    recommendation = generate_clothing_recommendation(city_name, description, temp)

    # 5️⃣ Формируем ответ
    reply = (
        f"📍 *{city_name}*\n"
        f"🌡 Температура: {temp:.1f}°C (ощущается как {feels_like:.1f}°C)\n"
        f"☁️ Погода: {description}\n"
        f"💧 Влажность: {humidity}% | 💨 Ветер: {wind_speed} м/с\n\n"
        f"👔 *Рекомендация:* {recommendation}"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=reply,
        parse_mode="Markdown"
    )