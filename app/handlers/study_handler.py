from telebot import TeleBot, types

from app.database.db import get_session
from app.database.models import UserWord, Word
from app.keyboards.study_keyboard import study_keyboard
from app.services.study_service import (get_random_study_word,
                                        reset_user_study_session)


def register_study_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == "Изучать слова 🎯")
    def start_study(message):

        target, options, source, target_id, progress = get_random_study_word(
            message.from_user.id
        )

        if not target:
            bot.send_message(
                message.chat.id,
                "🎉 Все слова изучены! Добавьте новые для продолжения."
            )
            return

        markup = study_keyboard(options, source, target_id)
        bot.send_message(
            message.chat.id,
            f"📘 <b>{progress}</b>\nКак переводится слово: "
            f"<b>{target.russian}</b>?",
            parse_mode="HTML",
            reply_markup=markup,
        )

    @bot.callback_query_handler(func=lambda c: c.data.startswith("answer_"))
    def handle_answer(call: types.CallbackQuery):

        data_parts = call.data.split("_")
        if len(data_parts) < 4:
            bot.answer_callback_query(
                call.id,
                "⚠️ Клавиатура устарела. Нажмите 'Изучать слова 🎯' снова."
            )
            return

        _, user_choice, source, target_id_str = data_parts
        target_id = int(target_id_str)

        session = get_session()
        try:
            if source == "base":
                target = session.query(Word).filter_by(id=target_id).first()
            else:
                target = session.query(UserWord).filter_by(id=target_id).first()

            if not target:
                bot.answer_callback_query(call.id,
                                          "⚠️ Это слово больше недоступно.")
                return

            if user_choice.lower() == target.english.lower():
                bot.answer_callback_query(call.id, "✅ Верно!")

                next_word, options, next_source, next_id, progress = (
                    get_random_study_word(call.from_user.id)
                )
                if not next_word:
                    bot.send_message(
                        call.message.chat.id,
                        "🎉 Отлично! Вы изучили все слова!\n"
                        "Добавьте новые, чтобы продолжить обучение.",
                    )
                    reset_user_study_session(call.from_user.id)
                    return

                markup = study_keyboard(options, next_source, next_id)
                bot.edit_message_text(
                    f"📘 <b>{progress}</b>\nКак переводится слово: "
                    f"<b>{next_word.russian}</b>?",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup,
                    parse_mode="HTML",
                )
            else:
                bot.answer_callback_query(
                    call.id, "❌ Неверно! Подумай и попробуй ещё раз 😉"
                )

        except Exception as e:
            print(f"❌ Ошибка при обработке ответа: {e}")
            bot.answer_callback_query(call.id, "⚠️ Ошибка, попробуйте снова.")
        finally:
            session.close()
