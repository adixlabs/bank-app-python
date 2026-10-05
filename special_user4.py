# special_user4.py
# Główny plik aplikacji administratora

import tkinter as tk
from special_client_api import BankClient

# noinspection PyAttributeOutsideInit
class BankApp:
    def __init__(self, server_url):
        # Zmienne pomocnicze
        self.root = root
        self.content_frame = tk.Frame(self.root, bg="darkgreen")
        self.content_frame.pack(fill="both", expand=True)
        self.client = BankClient(server_url)

        # Obecny Frame
        self.current_frame = None

        # Tworzenie Frame
        self.create_header_frame()
        self.create_app_element_frame()
        self.create_login_frame()
        self.create_menu_frame()
        self.create_logout_frame()
        self.create_deposit_menu_frame()
        self.create_done_action_frame()
        self.create_withdraw_menu_frame()
        self.create_adding_user_frame()
        self.create_deleting_user_frame()

        # Wywołanie stałych Frame
        self.header_frame.pack()
        self.app_element_frame.pack(pady=10)

        # Wywołanie obecnego Frame
        self.show_frame(self.login_frame)

    # Zaktualizowanie Frame
    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        frame.pack(fill="both", before=self.app_element_frame)
        self.current_frame = frame

    # ---Tworzenie Frame---

    # Nagłówkowy Frame
    def create_header_frame(self):
        self.header_frame = tk.Frame(self.content_frame, bg="white")
        self.header = tk.Label(
            self.header_frame,
            text="System Bankowy",
            fg="darkgreen",
            font=("Arial", 20, "bold"),
            bg="white"
        )
        self.header.pack(pady=20)

    # Frame z listą użytkowników, wyświetlaną zawsze, kiedy użytkownik jest zalogowany
    def create_app_element_frame(self):
        self.app_element_frame = tk.Frame(self.content_frame, bg="darkgreen")
        self.users_label = tk.Label(self.app_element_frame, text="", bg="darkgreen", fg="white")
        self.users_label.pack()

    # Frame logowania
    def create_login_frame(self):
        self.login_frame = tk.Frame(self.content_frame, bg="darkgreen")

        # Login -> napis + pole
        tk.Label(self.login_frame, text="Login:", bg="darkgreen", fg="white").pack()
        self.username_input = tk.Entry(self.login_frame, width=40)
        self.username_input.pack()

        # Hasło -> napis + pole
        tk.Label(self.login_frame, text="Hasło:", bg="darkgreen", fg="white").pack()
        self.password_input = tk.Entry(self.login_frame, width=40, show="*")
        self.password_input.pack()

        self.login_button = tk.Button(self.login_frame, text="Zaloguj", command=self.login_made)
        self.login_button.pack()

        # Napis do wyświetlania ewentualnych błędów
        self.message_label = tk.Label(self.login_frame, text="", fg="red", bg="darkgreen")
        self.message_label.pack(pady=5)

    # Frame z menu aplikacji
    def create_menu_frame(self):
        self.menu_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.admin_text = tk.Label(self.menu_frame, text="Pomyślnie zalogowano do panelu administracyjnego", bg="darkgreen", fg="white", font=("Arial", 12))
        self.admin_text.pack()

        self.b1 = tk.Button(self.menu_frame, text="Dodaj użytkownika", command=self.add_user)
        self.b1.pack(pady=5)

        self.b2 = tk.Button(self.menu_frame, text="Usuń użytkownika", command=self.delete_user)
        self.b2.pack(pady=5)

        self.b3 = tk.Button(self.menu_frame, text="Wpłata", command=self.prepare_to_deposit)
        self.b3.pack(pady=5)

        self.b4 = tk.Button(self.menu_frame, text="Wypłata", command=self.prepare_to_withdraw)
        self.b4.pack(pady=5)

        self.b5 = tk.Button(self.menu_frame, text="Wyloguj", command=self.logout_made)
        self.b5.pack(pady=5)

    # Frame wylogowania
    def create_logout_frame(self):
        self.logout_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.end_text = tk.Label(self.logout_frame, text="Wylogowano pomyślnie!", bg="darkgreen", fg="white", )
        self.end_text.pack()

        self.login_again = tk.Button(self.logout_frame, text="Zaloguj ponownie", command=self.login_entry)
        self.login_again.pack()

    # Frame wpłaty
    def create_deposit_menu_frame(self):
        self.deposit_menu_frame = tk.Frame(self.content_frame, bg="darkgreen")

        tk.Label(self.deposit_menu_frame, text="Kwota:", bg="darkgreen", fg="white").pack()
        self.cash_input = tk.Entry(self.deposit_menu_frame, width=40)
        self.cash_input.pack()

        tk.Label(self.deposit_menu_frame, text="Użytkownik:", bg="darkgreen", fg="white").pack()
        self.username_deposit_input = tk.Entry(self.deposit_menu_frame, width=40)
        self.username_deposit_input.pack()

        self.continuation = tk.Button(self.deposit_menu_frame, text="Dalej", command=self.deposit_made)
        self.continuation.pack()

        self.false_continuation = tk.Button(self.deposit_menu_frame, text="Anuluj", command=self.shortcut_way)
        self.false_continuation.pack()


    # Frame wypłaty
    def create_withdraw_menu_frame(self):
        self.withdraw_menu_frame = tk.Frame(self.content_frame, bg="darkgreen")

        tk.Label(self.withdraw_menu_frame, text="Kwota:", bg="darkgreen", fg="white").pack()
        self.cash_input2 = tk.Entry(self.withdraw_menu_frame, width=40)
        self.cash_input2.pack()

        tk.Label(self.withdraw_menu_frame, text="Użytkownik:", bg="darkgreen", fg="white").pack()
        self.username_withdraw_input = tk.Entry(self.withdraw_menu_frame, width=40)
        self.username_withdraw_input.pack()

        self.continuation2 = tk.Button(self.withdraw_menu_frame, text="Dalej", command=self.withdraw_made)
        self.continuation2.pack()

        self.false_continuation2 = tk.Button(self.withdraw_menu_frame, text="Anuluj", command=self.shortcut_way)
        self.false_continuation2.pack()

    # Frame dodawania użytkownika
    def create_adding_user_frame(self):
        self.adding_user_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.inform_label = tk.Label(self.adding_user_frame, text="Nazwa tworzonego użytkownika", bg="darkgreen", fg="white",
                                       font=("Arial", 12))
        self.inform_label.pack()

        self.new_username_input = tk.Entry(self.adding_user_frame, width=40)
        self.new_username_input.pack()

        self.inform2_label = tk.Label(self.adding_user_frame, text="Hasło tworzonego użytkownika", bg="darkgreen",
                                     fg="white",
                                     font=("Arial", 12))
        self.inform2_label.pack()

        self.new_password_input = tk.Entry(self.adding_user_frame, width=40)
        self.new_password_input.pack()

        self.confirm_button = tk.Button(self.adding_user_frame, text="Potwierdź", command=self.add_user_made)
        self.confirm_button.pack()

        self.cancel_button = tk.Button(self.adding_user_frame, text="Anuluj", command=self.shortcut_way)
        self.cancel_button.pack()

    # Frame usuwania użytkownika
    def create_deleting_user_frame(self):
        self.deleting_user_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.inform_label2 = tk.Label(self.deleting_user_frame, text="Nazwa usuwanego użytkownika", bg="darkgreen",
                                     fg="white",
                                     font=("Arial", 12))
        self.inform_label2.pack()

        self.old_username_input = tk.Entry(self.deleting_user_frame, width=40)
        self.old_username_input.pack()

        self.confirm_button2 = tk.Button(self.deleting_user_frame, text="Potwierdź", command=self.delete_user_made)
        self.confirm_button2.pack()

        self.cancel_button2 = tk.Button(self.deleting_user_frame, text="Anuluj", command=self.shortcut_way)
        self.cancel_button2.pack()

    # Frame z informacją o wykonanej akcji
    def create_done_action_frame(self):
        self.done_action_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.deposit_label = tk.Label(self.done_action_frame, text="___________", bg="darkgreen", fg="white",
                                          font=("Arial", 12))
        self.deposit_label.pack()

        self.pass_button = tk.Button(self.done_action_frame, text="Powrót do menu głównego",
                                         command=self.shortcut_way)
        self.pass_button.pack(pady=10)

    # Akcje w większości jedynie jako UI

    # Wykonanie logowania z pozycji UI
    def login_entry(self):
        self.show_frame(self.login_frame)

    # Powrót do menu i zaktualizowanie informacji o użytkownikach
    def shortcut_way(self):
        self.show_frame(self.menu_frame)
        try:
            result = self.client.check_users()
            self.users_label.config(text=result["list"])
        except Exception as e:
            print(e)

    # Wykonanie wylogowania z pozycji UI
    def logout_made(self):
        self.users_label.config(text="")
        self.show_frame(self.logout_frame)

    # Przygotowanie do wpłaty
    def prepare_to_deposit(self):
        self.show_frame(self.deposit_menu_frame)

    # Przygotowanie do wypłaty
    def prepare_to_withdraw(self):
        self.show_frame(self.withdraw_menu_frame)

    # Dodanie użytkownika z pozycji UI
    def add_user(self):
        self.show_frame(self.adding_user_frame)

    # Usuwanie użytkownika z pozycji UI
    def delete_user(self):
        self.show_frame(self.deleting_user_frame)

    # Metody przygotowania danych do API

    # Logowanie
    def login_made(self):
        self.username = self.username_input.get()
        self.password = self.password_input.get()
        # Próba zalogowania przez klienta
        try:
            if self.client.special_login(self.username, self.password):  # <- BankClient.login()
                # Pokaż menu główne
                self.shortcut_way()
            else:
                # Jeśli logowanie nieudane, pokaż komunikat w GUI
                self.message_label.config(text="Błędne dane logowania")

        except Exception as e:
            # Obsługa błędu połączenia z serwerem
            self.message_label.config(text=f"Błąd połączenia: {e}")

        # Wyczyść pola logowania
        self.username_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)

    # Wpłata
    def deposit_made(self):
        amount = self.cash_input.get()
        username2 = self.username_deposit_input.get()
        try:
            result = self.client.deposit(int(amount), username2)
            self.deposit_label.config(text=result["message"])
            self.show_frame(self.done_action_frame)

        except Exception as e:
            print(e)

    # Wypłata
    def withdraw_made(self):
        amount = self.cash_input2.get()
        username2 = self.username_withdraw_input.get()
        try:
            result = self.client.withdraw(int(amount), username2)
            self.deposit_label.config(text=result["message"])
            self.show_frame(self.done_action_frame)

        except Exception as e:
            print(e)

    # Dodanie użytkownika
    def add_user_made(self):
        new_username = self.new_username_input.get()
        new_password = self.new_password_input.get()
        try:
            result = self.client.add_user(new_username, new_password)
            self.deposit_label.config(text=result["message"])
            self.show_frame(self.done_action_frame)
        except Exception as e:
            print(e)

    # Usunięcie użytkownika
    def delete_user_made(self):
        old_username = self.old_username_input.get()
        try:
            result = self.client.cancel_user(old_username)
            self.deposit_label.config(text=result["message"])
            self.show_frame(self.done_action_frame)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Pobranie adresu IP serwera
    with open("server_url.txt", "r", encoding="utf-8") as file:
        url = file.read().strip()
    # --- konfiguracja okna ---
    root = tk.Tk()

    app = BankApp(url)

    root.title("System Bankowy - Panel Administratora")

    width = root.winfo_screenwidth()
    high = root.winfo_screenheight()

    root.geometry(f"{width}x{high}")
    root.configure(bg="darkgreen")

    # --- start GUI ---
    root.mainloop()

#TODO: Naprawić naciskanie niewidocznych przyciskach