import requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import Config
from app.keyboards import back_to_menu_button
import logging

router = Router()
config = Config()
logger = logging.getLogger(__name__)


@router.message(F.text.regexp(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
async def handle_ip_lookup(message: Message):
    try:
        ip = message.text
        # Проверка IP через IPInfo
        ipinfo_response = requests.get(
            f"https://ipinfo.io/{ip}/json?token={config.IPINFO_TOKEN}",
            timeout=10
        )

        # Проверка IP через Shodan (если есть API ключ)
        shodan_data = {}
        if config.SHODAN_API_KEY and config.SHODAN_API_KEY != "your_real_shodan_api_key_here":
            try:
                shodan_response = requests.get(
                    f"https://api.shodan.io/shodan/host/{ip}?key={config.SHODAN_API_KEY}",
                    timeout=10
                )
                if shodan_response.status_code == 200:
                    shodan_data = shodan_response.json()
            except Exception as e:
                logger.warning(f"Shodan error: {e}")

        if ipinfo_response.status_code == 200:
            data = ipinfo_response.json()
            report = f"""
🔍 <b>OSINT по IP {ip}</b>
├ Город: <code>{data.get('city', 'N/A')}</code>
├ Регион: <code>{data.get('region', 'N/A')}</code>
├ Страна: <code>{data.get('country', 'N/A')}</code>
├ Координаты: <code>{data.get('loc', 'N/A')}</code>
├ Провайдер: <code>{data.get('org', 'N/A')}</code>
└ Часовой пояс: <code>{data.get('timezone', 'N/A')}</code>
"""

            if shodan_data:
                report += f"""
🛰 <b>Shodan данные:</b>
├ Портів: <code>{len(shodan_data.get('ports', []))}</code>
├ ОС: <code>{shodan_data.get('os', 'N/A')}</code>
└ Уязвимостей: <code>{len(shodan_data.get('vulns', []))}</code>
"""

            kb = InlineKeyboardBuilder()
            kb.button(text="🔎 AbuseIPDB", url=f"https://www.abuseipdb.com/check/{ip}")
            kb.button(text="🛰️ Shodan", url=f"https://www.shodan.io/host/{ip}")
            kb.button(text="🗺️ Google Maps",
                      url=f"https://maps.google.com/?q={data.get('loc', '0,0')}")
            kb.adjust(2)

            await message.answer(
                report,
                parse_mode="HTML",
                reply_markup=kb.as_markup()
            )
        else:
            await message.answer("⚠️ Ошибка запроса к API", reply_markup=back_to_menu_button())

    except Exception as e:
        logger.error(f"IP lookup error: {e}")
        await message.answer(
            "❌ Ошибка обработки запроса",
            reply_markup=back_to_menu_button()
        )