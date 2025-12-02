from .client import CheckoClient

class LegalCasesAPI:
    def __init__(self, client: CheckoClient = None):
        self.client = client or CheckoClient()

    def get_cases(self, inn: str, role: str = None):
        payload = {"inn": inn}
        if role:
            payload["role"] = role
        return self.client.post("legal-cases", payload)


def get_legal_cases(inn: str, role: str = None):
    return LegalCasesAPI().get_cases(inn, role)
