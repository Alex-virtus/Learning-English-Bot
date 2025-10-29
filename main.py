import telebot

from app.database.config import TG_TOKEN
from app.database.init_db import init_db
from app.handlers.add_word_handler import register_add_word_handler
from app.handlers.delete_word_handler import register_delete_word_handler
from app.handlers.start_handler import register_start_handlers
from app.handlers.study_handler import register_study_handlers


def main():
    bot = telebot.TeleBot(TG_TOKEN, parse_mode="HTML")

    register_start_handlers(bot)
    register_study_handlers(bot)
    register_add_word_handler(bot)
    register_delete_word_handler(bot)

    init_db()

    print("✅ Бот запущен и готов к работе...")
    print("📊 Статус: Ожидание сообщений от пользователей")

    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
