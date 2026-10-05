# server.py
# backend w Flask

import datetime
from flask import Flask, request
from bank_user import BankUser
from special_bank_user import SpecialBankUser

bank_user = BankUser()
special_bank_user = SpecialBankUser(bank_user)
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Serwer działa!</h1> " + str(datetime.datetime.now())

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    return bank_user.login(username, password)

@app.route('/balance', methods=['POST'])
def balance():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    return bank_user.balance(username, password)

@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    amount = data.get("amount")
    from_ = data.get("from_")
    to = data.get("to")
    return bank_user.transfer(username, password, amount, from_, to)

@app.route('/special_login', methods=['POST'])
def special_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    return special_bank_user.login(username, password)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    new_username = data.get("new_username")
    new_password = data.get("new_password")
    return special_bank_user.add_user(username, password, new_username, new_password)

@app.route('/cancel_user', methods=['POST'])
def cancel_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    old_username = data.get("old_username")
    return special_bank_user.cancel_user(username, password, old_username)

@app.route("/users", methods=["POST"])
def check_users():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    return special_bank_user.check_users(username, password)

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    amount = data.get("amount")
    username2 = data.get("username2")
    return special_bank_user.deposit(username, password, amount, username2)

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    amount = data.get("amount")
    username2 = data.get("username2")
    return special_bank_user.withdraw(username, password, amount, username2)

if __name__ == '__main__':
    print("Serwer uruchomiony!")
    app.run(host='0.0.0.0', port=5000, debug=True)