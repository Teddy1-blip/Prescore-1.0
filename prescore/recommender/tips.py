def get_recommendations(metrics: dict) -> dict:
    """
    Пример логики рекомендаций на основе метрик.
    """
    recommendations = []

    if metrics.get("debt_ratio", 0) > 0.4:
        recommendations.append("Снизить долговую нагрузку.")

    if metrics.get("income_stability", 1) < 0.5:
        recommendations.append("Подтвердить стабильность дохода.")

    if not recommendations:
        recommendations.append("Все выглядит хорошо.")

    return {"recommendations": recommendations}
