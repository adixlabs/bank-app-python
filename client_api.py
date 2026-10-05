# client_api.py
# API aplikacji, pośredniczy między serwerem a frontend
import requests

# Klasa z zapytaniami
class BankClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.username = None
        self.password = None

    # Logowanie
    def login(self, username, password):
        response = requests.post(
            f"{self.server_url}/login",
            json={"username": username, "password": password}
        )
        data = response.json()
        if data["status"] == "success":
            self.username = username
            self.password = password
            return True
        return False

    # Pobieranie salda
    def get_balance(self):
        response = requests.post(
            f"{self.server_url}/balance",
            json={
                "username": self.username,
                "password": self.password
            }
        )

        return response.json()["balance"]

    # Przelew
    def transfer(self, to_user, amount):
        amount = int(amount)

        response = requests.post(
            f"{self.server_url}/transfer",
            json={
                "username": self.username,
                "password": self.password,
                "amount": amount,
                "from_": self.username,
                "to": to_user
            }
        )

        return response.json()