from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import Config
from app.keyboards import back_to_menu_button
import logging

router = Router()
config = Config()
logger = logging.getLogger(__name__)


class DDoSStates(StatesGroup):
    waiting_url = State()
    waiting_time = State()


@router.message(F.text == "DDos Miku Miku⚡")
async def handle_ddos_start(message: Message, state: FSMContext):
    await message.answer("🌀 Отправьте URL для теста (пример: http://example.com):")
    await state.set_state(DDoSStates.waiting_url)


@router.message(DDoSStates.waiting_url)
async def handle_ddos_url(message: Message, state: FSMContext):
    if not message.text.startswith(("http://", "https://")):
        await message.answer("❌ Неверный формат URL! Должен начинаться с http:// или https://")
        return

    await state.update_data(url=message.text)

    kb = InlineKeyboardBuilder()
    kb.button(text="1 мин", callback_data="ddos_1")
    kb.button(text="3 мин", callback_data="ddos_3")
    kb.button(text="5 мин (премиум)", callback_data="ddos_5")
    kb.button(text="10 мин (премиум)", callback_data="ddos_10")
    kb.adjust(2)

    await message.answer("⏳ Выберите время атаки:", reply_markup=kb.as_markup())
    await state.set_state(DDoSStates.waiting_time)


@router.callback_query(F.data.startswith("ddos_"), DDoSStates.waiting_time)
async def handle_ddos_time(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    time = callback.data.split("_")[1]

    try:
        await callback.message.bot.send_message(
            config.DDOS_CHANNEL_ID,
            f"🎯 Новая DDoS-атака!\n"
            f"🔗 Цель: {url}\n"
            f"⏱ Время: {time} мин\n"
            f"👤 От: @{callback.from_user.username}"
        )
        await callback.message.answer(
            f"✅ Атака на {url} запущена на {time} минут!",
            reply_markup=back_to_menu_button()
        )
    except Exception as e:
        logger.error(f"DDoS error: {e}")
        await callback.message.answer("⚠️ Ошибка отправки!")
    finally:
        await state.clear()