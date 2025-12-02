from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import sqlite3
from datetime import datetime
from prescore.services.parser_service import parse_file
from prescore.services.scoring_service import calculate_score

router = APIRouter(prefix="/upload", tags=["Upload"])

DB_PATH = "scoring_results.db"


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()

    if not (filename.endswith(".txt") or filename.endswith(".csv")):
        raise HTTPException(status_code=400, detail="Только TXT или CSV файлы поддерживаются")

    content = await file.read()

    # 1. Парсим файл (универсальный парсер)
    transactions = parse_file(content, filename)

    # 2. Считаем скоринг
    total_score = calculate_score(transactions)

    # 3. Сохраняем в БД
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scores (filename, total_score, created_at) VALUES (?, ?, ?)",
        (filename, total_score, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return JSONResponse({
        "filename": filename,
        "transactions": len(transactions),
        "total_score": total_score
    })
