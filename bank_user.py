# bank_user.py
# ciąg dalszy backendu do aplikacji użytkownika

import csv
from flask import jsonify

# Klasa z poleceniami dla aplikacji od strony użytkownika
class BankUser:
    def __init__(self):
        self.users = self.load_users()

    # Ładowanie użytkowników z pliku csv
    @staticmethod
    def load_users():
        users = {}
        with open('users.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users[row['username']] = {
                    'password': row['password'],
                    'balance': float(row['balance'])
                }
        return users

    # Zapisywanie wraz ze zmianami użytkowników
    def save_users(self):
        with open('users.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['username', 'password', 'balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for username, data in self.users.items():
                writer.writerow({
                    'username': username,
                    'password': data['password'],
                    'balance': data['balance']
                })

    # Logowanie
    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            return jsonify({"status": "success", "message": f"Zalogowano jako {username}"})

        return jsonify({"status": "error", "message": "Błędna nazwa użytkownika lub hasło"}), 401

    # Saldo
    def balance(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            return jsonify({"balance": self.users[username]["balance"]})

        return jsonify({"status": "error", "message": "Nieautoryzowany dostęp"}), 401

    # Przelew
    def transfer(self, username, password, amount, from_, to):
        # Warunek sprawdza zalogowanie użytkownika
        if username in self.users and self.users[username]["password"] == password:
            # Sprawdza, czy wartość salda pozwala na przelew
            if amount > 0:
                if self.users[from_]["balance"] >= amount:
                    self.users[from_]["balance"] -= amount
                    self.users[to]["balance"] += amount
                    self.save_users()
                    return jsonify({"status": "success",
                                    "message": f"Wykonano przelew na {amount} zł, z konta użytkownika {from_} na {to}\nDostępne środki (odpowiednio): {self.users[from_]["balance"]} i {self.users[to]["balance"]}"})

                return jsonify({"status": "error",
                                "message": "Niewystarczające środki"}), 400
            return jsonify({"status": "error",
                            "message": "Kwota musi być większa niż 0"}), 400
        return jsonify({"status": "error",
                        "message": "Nieautoryzowany dostęp"}), 401