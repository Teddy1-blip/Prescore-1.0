from .client import CheckoClient

class CompanyAPI:
    def __init__(self, client: CheckoClient = None):
        self.client = client or CheckoClient()

    def get_company_data(self, inn: str):
        payload = {"inn": inn}
        return self.client.post("company", payload)


# Для удобства: функция-обёртка
def get_company_data(inn: str):
    return CompanyAPI().get_company_data(inn)
