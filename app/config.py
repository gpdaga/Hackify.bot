import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DDOS_CHANNEL_ID = int(os.getenv("DDOS_CHANNEL_ID", "-1001234567890"))  # Значение по умолчанию
    ADMIN_IDS = [int(os.getenv("ADMIN_ID", "1602146479"))]  # Значение по умолчанию
    IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")  # Ваш токен из .env
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")