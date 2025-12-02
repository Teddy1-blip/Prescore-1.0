from datetime import datetime
from dateutil.relativedelta import relativedelta
from .stop_factors_schema import StopFactors, BankStopRules

class StopFactorsEngine:
    def __init__(self, stop_factors: StopFactors):
        self.stop_factors = stop_factors

    def calculate_age_months(self, registration_date: str) -> int:
        """registration_date: '2020-05-12'"""
        d = datetime.strptime(registration_date, "%Y-%m-%d")
        diff = relativedelta(datetime.now(), d)
        return diff.years * 12 + diff.months

    def check_company(self, company_data: dict) -> dict:
        """
        company_data приходит из Chekko /company:
        {
            "name": "...",
            "registration_date": "2021-06-23",
            "okved_main": "47.11",
            "region": "Москва"
        }
        """

        age_months = self.calculate_age_months(company_data["registration_date"])
        okved = company_data["okved_main"]
        region = company_data["region"]

        results = {}

        for bank, rules in self.stop_factors.banks.items():
            reason = []

            # --- 1. Возраст ---
            if rules.min_age and age_months < rules.min_age:
                reason.append(f"Возраст < {rules.min_age} мес")

            # --- 2. Регионы ---
            if rules.stop_regions and region in rules.stop_regions:
                reason.append(f"Стоп регион: {region}")

            if rules.allowed_regions and region not in rules.allowed_regions:
                reason.append(f"Регион не в списке разрешённых")

            # --- 3. ОКВЭД ---
            if rules.stop_okved and okved in rules.stop_okved:
                reason.append(f"Стоп ОКВЭД: {okved}")

            if rules.allowed_okved and okved not in rules.allowed_okved:
                reason.append(f"ОКВЭД не разрешён")

            results[bank] = {
                "allowed": len(reason) == 0,
                "reasons": reason
            }

        return results
