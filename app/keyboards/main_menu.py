from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Изучать слова 🎯")
    markup.row("Добавить слово ➕", "Удалить слово 🔙")

    return markup
