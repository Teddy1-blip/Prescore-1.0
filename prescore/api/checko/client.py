import requests
from .config import CHECKO_API_KEY, CHECKO_BASE_URL

class CheckoClient:
    def __init__(self, api_key: str = CHECKO_API_KEY):
        self.api_key = api_key

    def get(self, endpoint: str, params: dict):
        params["key"] = self.api_key
        url = f"{CHECKO_BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        return self._handle_response(response)

    def post(self, endpoint: str, payload: dict):
        payload["key"] = self.api_key
        url = f"{CHECKO_BASE_URL}/{endpoint}"
        response = requests.post(url, json=[payload], timeout=10)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        try:
            data = response.json()
        except Exception:
            raise Exception(f"Ошибка обработки ответа Checko: {response.text}")

        # Checko иногда возвращает список
        if isinstance(data, list):
            if len(data) and "data" in data[0]:
                return data[0]["data"]
            return data

        if "data" in data:
            return data["data"]

        return data
