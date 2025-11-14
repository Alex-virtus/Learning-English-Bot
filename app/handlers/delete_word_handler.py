from telebot import TeleBot, types

from app.keyboards.main_menu import main_menu
from app.services.user_service import get_or_create_user
from app.services.word_service import (
    get_user_words,
    delete_user_word,
    delete_all_user_words,
)


def register_delete_word_handler(bot: TeleBot):
    @bot.message_handler(func=lambda m: m.text == "Удалить слово 🔙")
    def ask_word_to_delete(message):
        user = get_or_create_user(message.from_user.id)
        if not user:
            bot.send_message(
                message.chat.id,
                "❌ Ошибка: пользователь не найден."
            )
            return

        words = get_user_words(user.user_id)
        if not words:
            bot.send_message(
                message.chat.id,
                "📭 У вас пока нет добавленных слов.",
                reply_markup=main_menu()
            )
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for w in words:
            markup.row(f"{w.eng_word} → {w.rus_word}")
        markup.row("🧹 Удалить все слова", "Отмена ❌")

        bot.send_message(
            message.chat.id,
            "🗑 Выберите слово для удаления или "
            "<b>🧹 Удалить все слова</b>:",
            parse_mode="HTML",
            reply_markup=markup
        )
        bot.register_next_step_handler(message, process_delete)

    def process_delete(message):
        text = message.text.strip().lower()
        cancel = ["отмена", "отмена ❌", "cancel"]

        if text in cancel:
            bot.send_message(
                message.chat.id,
                "🚫 Удаление отменено.",
                reply_markup=main_menu()
            )
            return

        user = get_or_create_user(message.from_user.id)
        if not user:
            bot.send_message(
                message.chat.id,
                "❌ Ошибка: пользователь не найден.",
                reply_markup=main_menu()
            )
            return

        if text == "🧹 удалить все слова":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("✅ Да, удалить всё", "❌ Отмена")
            bot.send_message(
                message.chat.id,
                "⚠️ Удалить <b>все</b> слова? Это действие нельзя отменить.",
                parse_mode="HTML",
                reply_markup=markup
            )
            bot.register_next_step_handler(
                message,
                lambda m: confirm_delete_all(m, user.user_id)
            )
            return

        words = get_user_words(user.user_id)
        sel = next(
            (w for w in words if text == f"{w.eng_word} → {w.rus_word}"),
            None
        )
        if not sel:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Отмена ❌")
            bot.send_message(
                message.chat.id,
                "❌ Такого слова нет. Попробуйте снова.",
                reply_markup=markup
            )
            bot.register_next_step_handler(message, process_delete)
            return

        success = delete_user_word(user.user_id, sel.eng_word)
        if success:
            bot.send_message(
                message.chat.id,
                f"✅ <b>{sel.eng_word}</b> → <b>{sel.rus_word}</b> удалено.",
                parse_mode="HTML",
                reply_markup=main_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Не удалось удалить слово. Попробуйте позже.",
                reply_markup=main_menu()
            )

    def confirm_delete_all(message, user_id):
        text = message.text.strip().lower()
        if text.startswith("✅ да"):
            count = delete_all_user_words(user_id)
            bot.send_message(
                message.chat.id,
                f"🧹 Удалено слов: <b>{count}</b>.\nВаш словарь теперь пуст.",
                parse_mode="HTML",
                reply_markup=main_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "🚫 Удаление всех слов отменено.",
                reply_markup=main_menu()
            )
