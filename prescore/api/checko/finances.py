from .client import CheckoClient

class FinancesAPI:
    def __init__(self, client: CheckoClient = None):
        self.client = client or CheckoClient()

    def get_finances(self, inn: str):
        payload = {"inn": inn}
        return self.client.post("finances", payload)


def get_finances(inn: str):
    return FinancesAPI().get_finances(inn)
