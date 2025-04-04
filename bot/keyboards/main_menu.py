from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Додати витрату 💰")
    builder.button(text="Отримати звіт 📊")
    builder.button(text="Видалити витрату 🗑")
    builder.button(text="Редагувати витрату 📝")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)