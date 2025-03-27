from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards import back_to_menu_button

router = Router()

PREMIUM_TEXT = """
💎 <b>Hackify Premium</b> ▓▒░⛧░▒▓

Доступные функции:
• Полный доступ к инструментам
• Базы данных уязвимостей
• Эксклюзивные материалы

Стоимость: $10/мес
"""

@router.message(F.text == "Премиум Hackify💎")
async def handle_premium(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🔐 Купить доступ", callback_data="premium_buy")
    kb.button(text="📌 Примеры материалов", callback_data="premium_examples")
    kb.button(text="💬 Консультация", callback_data="premium_consult")
    kb.adjust(2)

    await message.answer(
        PREMIUM_TEXT,
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "premium_buy")
async def handle_premium_buy(callback: CallbackQuery):
    await callback.message.answer(
        "💳 <b>Оплата Premium</b>\n\n"
        "1. Переведите $10 на наш BTC кошелек:\n"
        "<code>bc1qxy2kgdygjrsqtzq2n0yrf2493w83k4fj5g6h4u</code>\n\n"
        "2. Отправьте скриншот оплаты @Gpd_py",
        parse_mode="HTML",
        reply_markup=back_to_menu_button()
    )

@router.callback_query(F.data == "premium_examples")
async def handle_premium_examples(callback: CallbackQuery):
    await callback.message.answer(
        "📂 <b>Примеры Premium-материалов</b>:\n\n"
        "• Базы данных уязвимостей CVE\n"
        "• Эксклюзивные туториалы\n"
        "• Приватные инструменты\n\n"
        "Для доступа требуется активация Premium",
        parse_mode="HTML",
        reply_markup=back_to_menu_button()
    )

@router.callback_query(F.data == "premium_consult")
async def handle_premium_consult(callback: CallbackQuery):
    await callback.message.answer(
        "👨‍💻 <b>Консультация</b>\n\n"
        "По вопросам Premium подписки обращайтесь к @Gpd_py",
        parse_mode="HTML",
        reply_markup=back_to_menu_button()
    )