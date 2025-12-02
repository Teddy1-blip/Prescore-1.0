import pandas as pd
from pathlib import Path
from .stop_factors_schema import StopFactors, BankStopRules

def load_stop_factors(excel_path: str = "Стоп факторы.xlsx") -> StopFactors:
    """
    Загружает Excel файл стоп-факторов в структуру StopFactors.
    """
    file = Path(excel_path)
    if not file.exists():
        raise FileNotFoundError(f"Файл не найден: {excel_path}")

    df = pd.read_excel(file)

    banks = {}

    for col in df.columns[1:]:   # первая колонка — названия правил
        bank_name = col.strip()

        min_age = None
        stop_regions = []
        allowed_regions = []
        stop_okved = []
        allowed_okved = []

        for _, row in df.iterrows():
            rule_name = row[df.columns[0]].strip()
            value = str(row[col]).strip()

            if value == "nan" or value == "":
                continue

            # ---- Разбор каждого правила ----
            if rule_name == "Возраст минимально (мес)":
                try:
                    min_age = int(value)
                except:
                    pass

            elif rule_name == "Стоп регионы":
                stop_regions = [x.strip() for x in value.split(",")]

            elif rule_name == "Регионы для рассмотрения":
                allowed_regions = [x.strip() for x in value.split(",")]

            elif rule_name == "Стоп ОКВЭД":
                stop_okved = [x.strip() for x in value.split(",")]

            elif rule_name == "ОКВЭД для рассмотрения":
                allowed_okved = [x.strip() for x in value.split(",")]

        banks[bank_name] = BankStopRules(
            min_age=min_age,
            stop_regions=stop_regions,
            allowed_regions=allowed_regions,
            stop_okved=stop_okved,
            allowed_okved=allowed_okved,
        )

    return StopFactors(banks=banks)
