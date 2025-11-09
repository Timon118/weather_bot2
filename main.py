# Точка входа. Запуск бота в режиме polling (без webhook)
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.message_handler import start, handle_message
from utils.config import TELEGRAM_BOT_TOKEN

def main():
    # Создаём приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    print("✅ Бот запущен и ожидает сообщений...")
    application.run_polling()

if __name__ == "__main__":
    main()