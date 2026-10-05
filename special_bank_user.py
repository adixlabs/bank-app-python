# special_bank_user.py
# ciąg dalszy backendu do panelu administratora

import csv
from flask import jsonify

# Klasa z poleceniami panelu administratora
class SpecialBankUser:
    def __init__(self, bank_user):
        self.special_users = self.load_special_users()
        self.bank_user = bank_user

    # Ładowanie użytkowników z pliku csv
    @staticmethod
    def load_special_users():
        special_users = {}
        with open('special_users.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            print(reader.fieldnames)
            for row in reader:
                special_users[row['username']] = {
                    "password": row['password'],
                }
        return special_users

    # Logowanie
    def login(self, username, password):
        if username in self.special_users and self.special_users[username]["password"] == password:
            return jsonify({"status": "success", "message": f"Zalogowano jako {username} -admin"})

        return jsonify({"status": "error", "message": "Błędna nazwa użytkownika lub hasło"}), 401

    # Wyświetlenie listy użytkowników
    def check_users(self, username, password):
        if username in self.special_users and self.special_users[username]["password"] == password:
            to_return = ""
            for user, info in self.bank_user.users.items():
                line = str(info["balance"]).rjust(6, "_")
                final_line = f"{user.ljust(21, "_")}{line}\n"
                to_return += final_line
            return jsonify({"status": "success", "list": to_return})

        return jsonify({"status": "error", "message": "Nieautoryzowany dostęp"}), 401

    # Wpłata
    def deposit(self, username, password, amount, username2):
        # Warunek sprawdza, czy administrator jest zalogowany
        if username in self.special_users and self.special_users[username]["password"] == password:
            # Warunek sprawdza, czy użytkownik istnieje
            if username2 in self.bank_user.users:
                # Warunek sprawdza, czy kwota jest większa od zera.
                if type(amount) == int:
                    if amount > 0:
                        self.bank_user.users[username2]["balance"] += amount
                        self.bank_user.save_users()
                        return jsonify({"status": "success",
                                "message": f"Wpłacono {amount} zł\nDostępne środki klienta: {self.bank_user.users[username2]["balance"]}"})

                    return jsonify({"status": "error",
                                    "message": "Kwota musi być większa niż 0"}), 400
                return jsonify({"status": "error",
                                "message": "Zły format danych"}), 400
            return jsonify({"status": "error",
                            "message": "Podany użytkownik nie istnieje"}), 404
        return jsonify({"status": "error",
                        "message": "Nieautoryzowany dostęp"}), 401

    # Wypłata
    def withdraw(self, username, password, amount, username2):
        # Warunek sprawdza, czy administrator jest zalogowany
        if username in self.special_users and self.special_users[username]["password"] == password:
            # Warunek sprawdza, czy użytkownik istnieje
            if username2 in self.bank_user.users:
                # Warunek sprawdza, czy kwota jest większa od zera.
                if amount > 0:
                    if self.bank_user.users[username2]["balance"] >= amount:
                        self.bank_user.users[username2]["balance"] -= amount
                        self.bank_user.save_users()
                        return jsonify({"status": "success",
                                        "message": f"Wypłacono {amount} zł\nDostępne środki: {self.bank_user.users[username2]["balance"]}"}), 200

                    return jsonify({"status": "error",
                                    "message": "Niewystarczające środki"}), 400
                return jsonify({"status": "error",
                                    "message": "Kwota musi być większa niż 0"}), 400
            return jsonify({"status": "error",
                            "message": "Podany użytkownik nie istnieje"}), 404
        return jsonify({"status": "error",
                        "message": "Nieautoryzowany dostęp"}), 401

    # Dodawanie użytkownika
    def add_user(self, username, password, new_username, new_password):
        # Warunek sprawdza, czy administrator jest zalogowany
        if username in self.special_users and self.special_users[username]["password"] == password:
            # Warunek sprawdza, czy nie istnieje już użytkownik o tej samej nazwie
            if new_username not in self.bank_user.users:
                self.bank_user.users[new_username] = {"password": new_password, "balance": 0}
                self.bank_user.save_users()
                return jsonify({"status": "success",
                                "message": f"Dodano nowego użytkownika o nazwie: {new_username} i haśle: {new_password}"}), 200

            return jsonify({"status": "error",
                            "message": "Użytkownik o tej nazwie już istnieje"}), 409
        return jsonify({"status": "error",
                        "message": "Nieautoryzowany dostęp"}), 401

    # Usuwanie użytkownika
    def cancel_user(self, username, password, old_username):
        # Warunek sprawdza, czy administrator jest zalogowany
        if username in self.special_users and self.special_users[username]["password"] == password:
            # Warunek sprawdza, czy taki użytkownik istnieje
            if old_username in self.bank_user.users:
                del self.bank_user.users[old_username]
                self.bank_user.save_users()
                return jsonify({"status": "success",
                                "message": "Usunięto użytkownika"}), 200

            return jsonify({"status": "error",
                            "message": "Użytkownik o tej nazwie nie istnieje"}), 409
        return jsonify({"status": "error",
                        "message": "Nieautoryzowany dostęp"}), 401