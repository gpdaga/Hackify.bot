from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.generate import ai_generate
from app.keyboards import back_to_menu_button
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "Deep seek разговор💬")
async def deepseek_chat(message: Message, state: FSMContext):
    await message.answer(
        "💬 Режим общения с DeepSeek\nВведите запрос:",
        reply_markup=back_to_menu_button()
    )
    await state.set_state("deepseek_chat")

@router.message(F.text == "Deep seek Проверка кода🔍")
async def deepseek_code_check(message: Message, state: FSMContext):
    await message.answer(
        "🔍 Режим проверки кода\nОтправьте код:",
        reply_markup=back_to_menu_button()
    )
    await state.set_state("deepseek_code")

@router.message(F.state == "deepseek_chat")
@router.message(F.state == "deepseek_code")
async def handle_deepseek(message: Message, state: FSMContext):
    try:
        response = await ai_generate(message.text)
        await message.answer(
            response,
            reply_markup=back_to_menu_button()
        )
    except Exception as e:
        logger.error(f"DeepSeek error: {e}")
        await message.answer("⚠️ Ошибка обработки!")
    await state.clear()


@router.message(F.state == "deepseek_chat")
async def handle_deepseek(message: Message, state: FSMContext):
    try:
        # Отправляем сообщение о обработке
        processing_msg = await message.answer("🔄 Обработка запроса...")

        # Получаем ответ
        response = await ai_generate(message.text)

        # Удаляем сообщение "Обработка"
        await processing_msg.delete()

        # Отправляем ответ
        await message.answer(
            f"💬 Ответ:\n{response}",
            reply_markup=back_to_menu_button()
        )

    except Exception as e:
        print(f"[ERROR] Ошибка обработки: {e}")
        await message.answer(
            "⚠️ Произошла ошибка при обработке запроса",
            reply_markup=back_to_menu_button()
        )
    finally:
        await state.clear()