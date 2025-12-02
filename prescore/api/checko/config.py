import os
from dotenv import load_dotenv

load_dotenv()

CHECKO_API_KEY = os.getenv("CHEKKO_API_KEY")
CHECKO_BASE_URL = "https://api.checko.ru/v2"

if not CHECKO_API_KEY:
    raise ValueError("CHEKKO_API_KEY не найден в .env")
