# special_client_api.py
# API aplikacji, pośredniczy między serwerem a frontend
import requests

# Klasa z zapytaniami
class BankClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.username = None
        self.password = None

    # Logowanie
    def special_login(self, username, password):
        response = requests.post(
            f"{self.server_url}/special_login",
            json={"username": username, "password": password}
        )
        data = response.json()
        if data["status"] == "success":
            self.username = username
            self.password = password
            return True
        return False

    # Wpłata
    def deposit(self, amount, username2):
        response = requests.post(
            f"{self.server_url}/deposit",
            json={
                "username": self.username,
                "password": self.password,
                "username2": username2,
                "amount": amount,
            }
        )

        return response.json()

    # Wypłata
    def withdraw(self, amount, username2):
        response = requests.post(
            f"{self.server_url}/withdraw",
            json={
                "username": self.username,
                "password": self.password,
                "username2": username2,
                "amount": amount,
            }
        )

        return response.json()

    # Dodawanie użytkownika
    def add_user(self, new_username, new_password):
        response = requests.post(
            f"{self.server_url}/add_user",
            json={
                "username": self.username,
                "password": self.password,
                "new_username": new_username,
                "new_password": new_password
            }
        )

        return response.json()

    # Usuwanie użytkownika
    def cancel_user(self, old_username):
        response = requests.post(
            f"{self.server_url}/cancel_user",
            json={
                "username": self.username,
                "password": self.password,
                "old_username": old_username,
            }
        )

        return response.json()

    # Pobieranie listy użytkowników
    def check_users(self):
        response = requests.post(
            f"{self.server_url}/users",
            json={
                "username": self.username,
                "password": self.password,
            }
        )

        return response.json()