import os
import json
import logging
from flask import Blueprint, request, current_app, render_template
from werkzeug.utils import secure_filename

from prescore.parser.txt_parser import parse_txt
from prescore.core.calculator.metrics import calculate_metrics
from prescore.services.scoring_service import calculate_score

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)

ALLOWED_EXT = {'.txt'}

def allowed_file(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXT

@upload_bp.route('/', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files.get('file')
        if not uploaded_file or uploaded_file.filename == '':
            return "Ошибка: файл не выбран", 400

        filename = secure_filename(uploaded_file.filename)
        if not allowed_file(filename):
            return "Ошибка: поддерживаются только .txt файлы", 400

        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        uploaded_file.save(filepath)
        logger.info("Файл сохранён: %s", filepath)

        # Чтение файла с корректной кодировкой
        with open(filepath, 'rb') as f:
            content_bytes = f.read()
        try:
            content = content_bytes.decode('cp1251')
        except UnicodeDecodeError:
            content = content_bytes.decode('utf-8', errors='ignore')

        transactions = parse_txt(content)
        if not transactions:
            return "Файл обработан, но не найдено транзакций", 400

        # Расчёт метрик и скоринг
        metrics = calculate_metrics(transactions)
        scoring_result = calculate_score(metrics)

        formatted_metrics = {
            "Оборот": f"{metrics.get('total_income',0):,.0f} ₽".replace(",", " "),
            "Чистый поток": f"{metrics.get('net_cashflow',0):,.0f} ₽".replace(",", " "),
            "Средний доход/мес": f"{metrics.get('average_monthly_income',0):,.0f} ₽".replace(",", " "),
            "Контрагенты": f"{metrics.get('unique_payers_count',0)} контрагентов",
            "Операции": f"{metrics.get('total_transactions',0)} транзакций",
            "Период анализа": f"{metrics.get('analysis_period_months',0.0):.1f} мес"
        }

        recommendations = scoring_result.get("recommendations", [])

        # 🔹 Отдаём сразу готовый шаблон с результатами
        return render_template(
            'results.html',
            dashboards=formatted_metrics,
            scoringResults={
                "total_score": scoring_result.get("total_score",0),
                "risk_level": scoring_result.get("risk_level","Неизвестно"),
                "details": scoring_result.get("details",{})
            },
            recommendations=recommendations,
            transactions_count=len(transactions)
        )

    except Exception as e:
        import traceback
        logger.exception("Критическая ошибка при обработке файла:")
        return f"Критическая ошибка:\n{str(e)}\n\n{traceback.format_exc()}", 500
