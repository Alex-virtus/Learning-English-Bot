from telebot import TeleBot, types

from app.keyboards.main_menu import main_menu
from app.services.user_service import get_or_create_user
from app.services.word_service import add_user_word


def register_add_word_handler(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == "Добавить слово ➕")
    def ask_english_word(message):
        cancel_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cancel_markup.row("Отмена ❌")
        bot.send_message(
            message.chat.id,
            "📝 Введите слово на английском:",
            reply_markup=cancel_markup
        )
        bot.register_next_step_handler(message, process_english_word)

    def process_english_word(message):
        english = message.text.strip()
        cancel_words = ["отмена", "отмена ❌", "cancel"]

        if english.lower() in cancel_words:
            bot.send_message(
                message.chat.id,
                "🚫 Добавление слова отменено.",
                reply_markup=main_menu()
            )
            return

        if not english.isalpha():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Отмена ❌")
            bot.send_message(
                message.chat.id,
                "❌ Только буквы! Попробуйте снова.",
                reply_markup=markup
            )
            bot.register_next_step_handler(message, process_english_word)
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Отмена ❌")
        bot.send_message(
            message.chat.id,
            "🔤 Теперь введите перевод на русском:",
            reply_markup=markup
        )
        bot.register_next_step_handler(
            message,
            lambda msg: save_word(msg, english.lower())
        )

    def save_word(message, english):
        russian = message.text.strip()
        cancel_words = ["отмена", "отмена ❌", "cancel"]

        if russian.lower() in cancel_words:
            bot.send_message(
                message.chat.id,
                "🚫 Добавление слова отменено.",
                reply_markup=main_menu()
            )
            return

        if not russian:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Отмена ❌")
            bot.send_message(
                message.chat.id,
                "❌ Перевод не может быть пустым. Попробуйте снова.",
                reply_markup=markup
            )
            bot.register_next_step_handler(
                message,
                lambda msg: save_word(msg, english)
            )
            return

        user = get_or_create_user(message.from_user.id)
        if not user:
            bot.send_message(
                message.chat.id,
                "❌ Ошибка: пользователь не найден."
            )
            return

        success, msg_text = add_user_word(user.user_id, english, russian)
        text = (
            f"✅ <b>{english}</b> → <b>{russian}</b> добавлено!"
            if success else f"❌ {msg_text}"
        )
        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML",
            reply_markup=main_menu()
        )
