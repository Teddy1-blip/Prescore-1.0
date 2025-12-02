# prescore/core/calculator/metrics.py
from typing import List, Dict
import pandas as pd

def calculate_metrics(transactions: List[Dict]) -> Dict:
    print("РАСЧЕТ МЕТРИК: %s транзакций" % len(transactions))
    if not transactions:
        print("НЕТ ДАННЫХ ДЛЯ АНАЛИЗА")
        return {
            "total_income": 0.0,
            "total_outgoing": 0.0,
            "net_cashflow": 0.0,
            "average_monthly_income": 0.0,
            "unique_payers_count": 0,
            "total_transactions": 0,
            "analysis_period_months": 0.0,
            "income_to_outgoing_ratio": 0.0,
        }

    df = pd.DataFrame(transactions)
    # безопасное парсение дат: пытаемся распознать dd.mm.yyyy, если нет — pandas сам попробует
    try:
        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
    except Exception:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.dropna(subset=['date'])  # чтобы не ломать расчеты

    income_tx = df[df['type'] == 'incoming']
    outgoing_tx = df[df['type'] == 'outgoing']

    total_income = float(income_tx['amount'].sum())
    total_outgoing = float(outgoing_tx['amount'].sum())
    net_cashflow = total_income - total_outgoing

    start_date = df['date'].min()
    end_date = df['date'].max()
    days = (end_date - start_date).days if start_date is not None and end_date is not None else 0
    analysis_period_months = max(days / 30.0, 1.0)

    average_monthly_income = total_income / analysis_period_months if analysis_period_months else 0.0
    unique_payers_count = int(income_tx['counterparty'].nunique()) if not income_tx.empty else 0
    total_transactions = len(df)

    if total_outgoing > 0:
        income_to_outgoing_ratio = total_income / total_outgoing
    else:
        income_to_outgoing_ratio = float('inf')

    return {
        "total_income": total_income,
        "total_outgoing": total_outgoing,
        "net_cashflow": net_cashflow,
        "average_monthly_income": average_monthly_income,
        "unique_payers_count": unique_payers_count,
        "total_transactions": total_transactions,
        "analysis_period_months": analysis_period_months,
        "income_to_outgoing_ratio": income_to_outgoing_ratio
    }
