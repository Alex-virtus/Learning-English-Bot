from telebot import TeleBot
from telebot.types import BotCommand
from app.keyboards.main_menu import main_menu
from app.services.user_service import get_or_create_user


def register_start_handlers(bot: TeleBot):
    set_persistent_menu(bot)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        user = get_or_create_user(message.from_user.id)
        if not user:
            bot.send_message(
                message.chat.id, "❌ Ошибка при создании пользователя."
            )
            return

        text = (
            "👋 Привет! Давай попрактикуемся в английском языке.\n\n"
            "Ты можешь изучать слова в своём темпе и собирать базу слов.\n\n"
            "📚 Используй кнопки:\n"
            "• Изучать слова 🎯\n"
            "• Добавить слово ➕\n"
            "• Удалить слово 🔙\n\n"
            "Готов? Нажимай «Изучать слова 🎯»! 🚀"
        )

        bot.send_message(
            message.chat.id, text, reply_markup=main_menu()
        )
        print(
            f"👋 Пользователь {message.from_user.id} запустил "
            "бота командой /start"
        )

    @bot.message_handler(commands=["help"])
    def help_message(message):
        help_text = (
            "🧠 <b>Команды:</b>\n\n"
            "• /start — запустить бота и открыть главное меню\n"
            "• /help — показать справку\n\n"
            "📋 Кнопки:\n"
            "🎯 Изучать слова — начать обучение\n"
            "➕ Добавить слово — добавить новое слово\n"
            "🔙 Удалить слово — удалить своё слово\n\n"
            "Если что-то пошло не так — просто напиши /start 🙂"
        )
        bot.send_message(
            message.chat.id, help_text, parse_mode="HTML"
        )


def set_persistent_menu(bot: TeleBot):
    commands = [
        BotCommand("start", "Главное меню"),
        BotCommand("help", "Помощь ℹ️"),
    ]
    bot.set_my_commands(commands)
