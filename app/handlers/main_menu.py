from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.keyboards import main_menu_keyboard, back_to_menu_button

router = Router()

@router.callback_query(F.data == "main_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await cmd_start(callback.message)

@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    welcome_text = """
🌀 <b>≪ 𝐇𝐀𝐂𝐊𝐈𝐅𝐘 𝐒𝐘𝐒𝐓𝐄𝐌 ≫</b> ▓▒░⛧░▒▓

<code>Initializing cyber interface...</code>
█▓▒░🌀▬▬ι═══════ﺤ -═══════ι▬▬🌀░▒▓█
⚡ <i>Your ultimate hacking toolkit</i>
"""
    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

@router.message(F.text == "OSINT🕵️")
async def handle_osint(message: types.Message):
    await message.answer(
        "🕵️ <b>OSINT Инструменты</b>\n\n"
        "Отправьте IP-адрес для анализа (пример: 8.8.8.8)",
        parse_mode="HTML",
        reply_markup=back_to_menu_button()
    )
