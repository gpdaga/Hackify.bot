import subprocess
import asyncio
import tempfile
import os
import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import Config
from app.keyboards import back_to_menu_button
import logging

router = Router()
config = Config()
logger = logging.getLogger(__name__)

# Разрешенные тестовые домены
ALLOWED_DOMAINS = [
    "testphp.vulnweb.com",
    "demo.testfire.net",
    "zero.webappsecurity.com"
]


# Правильное объявление состояний через StatesGroup
class ScanStates(StatesGroup):
    waiting_url = State()
    scanning = State()


def is_test_site(url: str) -> bool:
    """Проверяет, является ли сайт тестовым"""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.lower()
        return any(test_domain in domain for test_domain in ALLOWED_DOMAINS)
    except Exception:
        return False


async def run_sqlmap(url: str, output_file: str) -> str:
    """Асинхронный запуск sqlmap"""
    cmd = [
        "sqlmap",
        "-u", url,
        "--batch",
        "--output-dir", os.path.dirname(output_file),
        "--flush-session",
        "--crawl=1"
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    return stdout.decode()


def format_results(output: str) -> str:
    """Форматирование результатов для Telegram"""
    cleaned = re.sub(r'\x1b\[.*?m', '', output)
    important = [line for line in cleaned.split('\n') if any(
        kw in line.lower() for kw in ['target', 'injection', 'vulnerable', 'payload']
    )]
    return "\n".join(important[:20]) or "Не удалось получить результаты"


@router.message(Command("cancel"))
async def cancel_scan(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Сканирование отменено", reply_markup=back_to_menu_button())


@router.message(F.text == "Sqlmap проверка сайта🛡️")
async def request_url(message: Message, state: FSMContext):
    """Запрос URL для сканирования"""
    sites = "\n".join(f"• http://{domain}" for domain in ALLOWED_DOMAINS)
    await message.answer(
        f"🔍 <b>Введите URL тестового сайта</b>\n\n"
        f"<u>Разрешенные сайты:</u>\n{sites}\n\n"
        f"<i>Используйте /cancel для отмены</i>",
        parse_mode="HTML"
    )
    await state.set_state(ScanStates.waiting_url)


@router.message(ScanStates.waiting_url, F.text.startswith(('http://', 'https://')))
async def start_scan(message: Message, state: FSMContext):
    """Начало сканирования"""
    url = message.text.strip()

    if not is_test_site(url):
        await message.answer(
            "⚠️ <b>Это не тестовый сайт!</b>\n\n"
            "Используйте только разрешенные ресурсы.",
            parse_mode="HTML"
        )
        return

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_file = tmp.name

        await state.set_state(ScanStates.scanning)
        status_msg = await message.answer(
            f"🔎 <b>Сканирую</b> {url}\n\n"
            "Это займет 2-5 минут...",
            parse_mode="HTML"
        )

        output = await run_sqlmap(url, tmp_file)
        result = format_results(output)

        if "vulnerable" in output.lower():
            response = f"🛑 <b>Найдены уязвимости!</b>\n\n<code>{result}</code>"
        else:
            response = f"✅ <b>Уязвимости не обнаружены</b>\n\n<code>{result}</code>"

        await message.answer(response, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Scan error: {e}")
        await message.answer(
            "❌ <b>Ошибка сканирования</b>\n\n"
            f"<code>{str(e)}</code>",
            parse_mode="HTML"
        )
    finally:
        if os.path.exists(tmp_file):
            os.unlink(tmp_file)
        await state.clear()
        try:
            await status_msg.delete()
        except:
            pass