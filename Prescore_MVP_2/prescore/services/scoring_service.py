# prescore/services/scoring_service.py
def calculate_score(metrics: dict) -> dict:
    """
    Простая эвристика скоринга:
      - total_income -> баллы
      - net_cashflow -> баллы
      - диверсификация (unique_payers_count)
      - income_to_outgoing_ratio
    Возвращает словарь с total_score (0-100), risk_level и деталями.
    """
    total_income = metrics.get('total_income', 0.0)
    net_cashflow = metrics.get('net_cashflow', 0.0)
    unique_payers = metrics.get('unique_payers_count', 0)
    ratio = metrics.get('income_to_outgoing_ratio', 0.0)

    # Базовые компоненты (весовые коэффициенты)
    # Это простая и прозрачная эвристика; при желании можно заменить на ML или более сложную формулу
    score = 0

    # Обороты — шкала (к 30 баллам)
    if total_income > 5_000_000:
        score += 30
    elif total_income > 1_000_000:
        score += 20
    elif total_income > 200_000:
        score += 10
    else:
        score += 5

    # Денежный поток (к 25 баллам)
    if net_cashflow > 1_000_000:
        score += 25
    elif net_cashflow > 100_000:
        score += 15
    elif net_cashflow > 0:
        score += 8
    else:
        score += 0

    # Диверсификация контрагентов (к 20 баллам)
    if unique_payers >= 10:
        score += 20
    elif unique_payers >= 5:
        score += 12
    elif unique_payers >= 2:
        score += 6
    else:
        score += 0

    # Соотношение доход/расход (к 25 баллам)
    if ratio == float('inf'):
        score += 25
    elif ratio >= 3:
        score += 20
    elif ratio >= 1.5:
        score += 12
    elif ratio >= 1.0:
        score += 6
    else:
        score += 0

    # Ограничиваем 0-100
    total_score = max(0, min(100, int(score)))

    # Уровень риска
    if total_score >= 80:
        risk = "Низкий"
    elif total_score >= 60:
        risk = "Средний"
    else:
        risk = "Высокий"

    # Детали (для отображения)
    details = {
        "total_income": total_income,
        "net_cashflow": net_cashflow,
        "unique_payers": unique_payers,
        "income_to_outgoing_ratio": ratio
    }

    # Простые рекомендации
    recs = []
    if total_score >= 80:
        recs.append("✅ Отличные финансовые показатели — можно рассмотреть кредит с выгодными условиями.")
    elif total_score >= 60:
        recs.append("📊 Хорошие показатели — работайте над диверсификацией клиентов и стабильностью потока.")
    else:
        recs.append("⚠️ Низкий балл — требуется увеличение оборотов и улучшение денежного потока.")

    if unique_payers < 5:
        recs.append("🔍 Расширьте базу контрагентов (минимум 5-10 активных плательщиков).")
    if metrics.get('net_cashflow', 0) < 0:
        recs.append("💡 Обратите внимание: отрицательный денежный поток. Оптимизируйте расходы.")
    if metrics.get('income_to_outgoing_ratio', 0) < 1.1:
        recs.append("💰 Оптимизируйте соотношение доходов и расходов (рекомендуем >1.2).")

    return {
        "total_score": total_score,
        "risk_level": risk,
        "details": details,
        "recommendations": recs
    }
