import tkinter as tk
from tkinter import messagebox
import auth

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure File and Message Transfer")
        self.geometry("400x300")

        # Center the window
        self.eval('tk::PlaceWindow . center')

        self.show_login_frame()

    def show_login_frame(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(self.login_frame, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.pack()

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        is_authenticated, role = auth.authenticate_user(username, password)

        if is_authenticated:
            self.login_frame.destroy()
            self.show_main_app(role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_main_app(self, role):
        main_frame = tk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        tk.Label(main_frame, text=f"Welcome! Your role is: {role}").pack()
        tk.Label(main_frame, text="Main application window placeholder.").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
