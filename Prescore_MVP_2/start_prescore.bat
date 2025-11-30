@echo off
call .venv\Scripts\activate
uvicorn prescore.app.main:app --reload
pause
