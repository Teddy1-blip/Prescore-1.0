import os
from dotenv import load_dotenv
from pathlib import Path

# Вычисляем путь к корню проекта (на четыре уровня вверх от config.py).
# Это исправляет ошибку поиска пути, которую мы видели ранее.
DOTENV_PATH = Path(__file__).resolve().parent.parent.parent.parent / '.env'

# Загружаем файл .env по явному пути
load_dotenv(dotenv_path=DOTENV_PATH)

# Извлекаем переменные среды
CHECKO_API_KEY = os.getenv("CHECKO_API_KEY")
CHECKO_BASE_URL = os.getenv("CHECKO_BASE_URL", "https://api.checko.ru/v2")

# Проверка:
if not CHECKO_API_KEY:
    # ИСПРАВЛЕНИЕ: Исправлена опечатка в сообщении об ошибке (с 'CHEKKO' на 'CHECKO').
    # Теперь, если ключ не найден, сообщение будет корректным и укажет на правильный путь.
    raise ValueError(f"CHECKO_API_KEY не найден в {DOTENV_PATH}. Проверьте файл .env.")

# Если нужно использовать другие переменные, например DEBUG:
DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ('true', '1', 't')