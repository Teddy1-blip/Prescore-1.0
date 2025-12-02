from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/scoring", tags=["Scoring"])

DB_PATH = "scoring_results.db"


@router.get("/")
def list_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, total_score, created_at FROM scores ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": r[0], "filename": r[1], "total_score": r[2], "created_at": r[3]}
        for r in rows
    ]
