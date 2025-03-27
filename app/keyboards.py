from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    buttons = [
        "DDos Miku Miku⚡",
        "Deep seek разговор💬",
        "Deep seek Проверка кода🔍",
        "Sqlmap проверка сайта🛡️",
        "Support🆘",
        "Премиум Hackify💎",
        "OSINT🕵️"
    ]
    for button in buttons:
        builder.button(text=button)
    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True)

def back_to_menu_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ В главное меню", callback_data="main_menu")
    return builder.as_markup()