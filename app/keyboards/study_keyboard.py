from telebot import types


def study_keyboard(options, source, target_id):
    markup = types.InlineKeyboardMarkup()
    for opt in options:
        callback_data = f"answer_{opt}_{source}_{target_id}"
        markup.add(types.InlineKeyboardButton(text=opt,
                                              callback_data=callback_data))
    return markup
