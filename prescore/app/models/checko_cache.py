# prescore/app/models/checko_cache.py

import sqlite3
import json
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "scoring_results.db")

CACHE_LIFETIME_DAYS = 30  # срок годности кеша

# ------------------------------
# Создание таблицы кеша (если нет)
# ------------------------------
def init_cache_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checko_cache (
            inn TEXT PRIMARY KEY,
            company_json TEXT NOT NULL,
            finances_json TEXT NOT NULL,
            stop_factors_json TEXT,
            updated_at TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()


# ------------------------------
# Получение данных из кеша
# ------------------------------
def load_from_cache(inn: str):
    init_cache_table()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT company_json, finances_json, stop_factors_json, updated_at FROM checko_cache WHERE inn = ?", (inn,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        return None  # нет в кеше

    company_json, finances_json, stop_json, updated_at = row

    updated_dt = datetime.fromisoformat(updated_at)
    if datetime.now() - updated_dt > timedelta(days=CACHE_LIFETIME_DAYS):
        return None  # кеш устарел

    return {
        "company": json.loads(company_json),
        "finances": json.loads(finances_json),
        "stop_factors": json.loads(stop_json) if stop_json else None,
    }


# ------------------------------
# Сохранение данных в кеш
# ------------------------------
def save_to_cache(inn: str, company, finances, stop_factors):
    init_cache_table()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO checko_cache (inn, company_json, finances_json, stop_factors_json, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        inn,
        json.dumps(company, ensure_ascii=False),
        json.dumps(finances, ensure_ascii=False),
        json.dumps(stop_factors or {}, ensure_ascii=False),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
