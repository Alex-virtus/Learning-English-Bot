from telebot import TeleBot, types

from app.keyboards.study_keyboard import study_keyboard
from app.services.study_service import get_random_study_word


def register_study_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == "Изучать слова 🎯")
    def start_study(message):
        send_next_word(message.chat.id, bot, message.from_user.id)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("answer_"))
    def handle_answer(call: types.CallbackQuery):
        _, source, target_id_str, choice = call.data.split("_", 3)
        target_id = int(target_id_str)

        from app.database.db import SessionLocal
        from app.database.models import Words

        with SessionLocal() as session:
            target = session.query(Words).filter_by(word_id=target_id).first()
            if not target:
                bot.answer_callback_query(
                    call.id, "⚠️ Слово не найдено."
                )
                return

            if choice.lower() == target.eng_word.lower():
                bot.answer_callback_query(call.id, "✅ Верно!")
                send_next_word(call.message.chat.id, bot, call.from_user.id)
            else:
                bot.answer_callback_query(
                    call.id, "❌ Неверно! Попробуй снова 😉"
                )


def send_next_word(chat_id, bot, user_id):
    target, options, source, target_id, progress = get_random_study_word(user_id)
    if not target:
        bot.send_message(
            chat_id,
            "🎉 Все слова изучены! Добавьте новые для продолжения."
        )
        return

    markup = study_keyboard(options, source, target_id)
    bot.send_message(
        chat_id,
        f"📘 <b>{progress}</b>\nКак переводится слово: <b>{target.rus_word}</b>?",
        parse_mode="HTML",
        reply_markup=markup
    )
