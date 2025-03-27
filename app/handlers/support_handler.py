from aiogram import Router, F
from aiogram.types import Message
from app.keyboards import back_to_menu_button

router = Router()

SUPPORT_TEXT = """
🛠 <b>Техподдержка Hackify</b>

Свяжитесь с нами:
• Разработчик: @Gpd_py
• Чат: @HAKATOON
• Email: support@hackify.io
"""

@router.message(F.text == "Support🆘")
async def handle_support(message: Message):
    await message.answer(
        SUPPORT_TEXT,
        parse_mode="HTML",
        reply_markup=back_to_menu_button()
    )