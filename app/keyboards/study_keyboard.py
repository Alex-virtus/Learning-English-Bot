from telebot import types


def study_keyboard(options, source, target_id):
    markup = types.InlineKeyboardMarkup()
    for opt in options:
        callback_data = f"answer_{source}_{target_id}_{opt}"
        markup.add(types.InlineKeyboardButton(text=opt,
                                              callback_data=callback_data))
    return markup
