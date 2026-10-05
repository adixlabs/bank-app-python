# user_with_grafic3.py
# Główny plik aplikacji użytkownika

import tkinter as tk
from client_api import BankClient

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
        self.create_login_frame()
        self.create_menu_frame()
        self.create_transfer_frame()
        self.create_done_transfer_frame()
        self.create_logout_frame()

        # Wywołanie stałego Frame
        self.header_frame.pack()

        # Wywołanie obecnego Frame
        self.show_frame(self.login_frame)

    # Zaktualizowanie Frame
    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        frame.pack(fill="both", expand=True)
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

        # Napis do wyświetlenia ewentualnych błędów
        self.message_label = tk.Label(self.login_frame, text="", fg="red", bg="darkgreen")
        self.message_label.pack(pady=5)

    # Frame z menu aplikacji
    def create_menu_frame(self):
        self.menu_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.balance_text = tk.Label(self.menu_frame, text="Twoje saldo to: ____", bg="darkgreen", fg="white", font=("Arial", 12))
        self.balance_text.pack()
        self.b1 = tk.Button(self.menu_frame, text="Wykonaj przelew", command=self.prepare_to_transfer_made)
        self.b1.pack(pady=5)

        self.b2 = tk.Button(self.menu_frame, text="Wyloguj", command=self.logout_made)
        self.b2.pack(pady=5)

    # Frame przelewu
    def create_transfer_frame(self):
        self.transfer_frame = tk.Frame(self.content_frame, bg="darkgreen")

        tk.Label(self.transfer_frame, text="Kwota:", bg="darkgreen", fg="white").pack()
        self.cash_input = tk.Entry(self.transfer_frame, width=40)
        self.cash_input.pack(pady=5)

        tk.Label(self.transfer_frame, text="Użytkownik:", bg="darkgreen", fg="white").pack()
        self.user_input = tk.Entry(self.transfer_frame, width=40)
        self.user_input.pack(pady=5)

        self.send = tk.Button(self.transfer_frame, text="Wyślij przelew", command=self.transfer_made)
        self.send.pack(pady=10)

        self.cancel = tk.Button(self.transfer_frame, text="Anuluj", command=self.shortcut_way)
        self.cancel.pack()

    # Frame wykonanego przelewu
    def create_done_transfer_frame(self):
        self.done_transfer_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.transfer_label = tk.Label(self.done_transfer_frame, text="___________", bg="darkgreen", fg="white", font=("Arial", 12))
        self.transfer_label.pack()

        self.download_button = tk.Button(self.done_transfer_frame, text="Pobierz potwierdzenie przelewu", state="disabled")
        self.download_button.pack(pady=10)

        self.pass_button = tk.Button(self.done_transfer_frame, text="Powrót do menu głównego", command=self.start_balance)
        self.pass_button.pack(pady=10)

    # Frame wylogowania
    def create_logout_frame(self):
        self.logout_frame = tk.Frame(self.content_frame, bg="darkgreen")

        self.end_text = tk.Label(self.logout_frame, text="Wylogowano pomyślnie!", bg="darkgreen", fg="white", )
        self.end_text.pack()

        self.login_again = tk.Button(self.logout_frame, text="Zaloguj ponownie", command=self.login_entry)
        self.login_again.pack()

    # Wykonanie logowania z pozycji UI

    # Logowanie
    def login_entry(self):
        self.show_frame(self.login_frame)

    # Pobranie salda
    def start_balance(self):
        # Pobranie salda zalogowanego użytkownika
        balance = self.client.get_balance()

        # Aktualizacja Label w GUI
        self.balance_text.config(text=f"Twoje saldo to: {balance} zł")
        self.show_frame(self.menu_frame)

    # Przelew z poziomu UI
    def prepare_to_transfer_made(self):
        self.cash_input.delete(0, tk.END)
        self.user_input.delete(0, tk.END)
        self.show_frame(self.transfer_frame)

    # Powrót do menu
    def shortcut_way(self):
        self.show_frame(self.menu_frame)

    # Wylogowania z poziomu UI
    def logout_made(self):
        self.show_frame(self.logout_frame)

    # Metody przygotowania danych do API

    # Logowanie
    def login_made(self):
        self.username = self.username_input.get()
        self.password = self.password_input.get()
        # 2️⃣ Próba zalogowania przez klienta
        try:
            if self.client.login(self.username, self.password):
                # Pobranie salda zalogowanego użytkownika
                balance = self.client.get_balance()

                # Aktualizacja Label w GUI
                self.balance_text.config(text=f"Twoje saldo to: {balance} zł")

                # Pokaż menu główne
                self.show_frame(self.menu_frame)
            else:
                # Jeśli logowanie nieudane, pokaż komunikat w GUI
                self.message_label.config(text="Błędne dane logowania")

        except Exception as e:
            # Obsługa błędu połączenia z serwerem
            self.message_label.config(text=f"Błąd połączenia: {e}")

        # Wyczyść pola logowania
        self.username_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)

    # Przelew
    def transfer_made(self):
        cash = self.cash_input.get()
        user = self.user_input.get()
        try:
            result = self.client.transfer(user, cash)
            self.transfer_label.config(text=result['message'])

        except Exception as e:
            # 7️⃣ Obsługa błędu połączenia z serwerem
            self.message_label.config(text=f"Błąd połączenia: {e}")

        self.show_frame(self.done_transfer_frame)

if __name__ == '__main__':
    # Pobranie adresu IP serwera
    with open("server_url.txt", "r", encoding="utf-8") as file:
        url = file.read().strip()

    # --- konfiguracja okna ---
    username = None
    password = None

    root = tk.Tk()

    app = BankApp(url)

    root.title("System Bankowy")

    width = root.winfo_screenwidth()
    high = root.winfo_screenheight()

    root.geometry(f"{width}x{high}")
    root.configure(bg="darkgreen")

    # --- start GUI ---
    root.mainloop()