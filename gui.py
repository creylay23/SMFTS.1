import tkinter as tk
from tkinter import messagebox, font, ttk, filedialog, simpledialog
import auth
import database
import encryption
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Transfer System")
        self.geometry("800x600")

        # --- Style Configuration ---
        self.configure(bg="#2E8B57")
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        self.entry_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        style = ttk.Style(self)
        style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"))

        self.eval('tk::PlaceWindow . center')

        self.current_user = None
        self.show_login_frame()

    def show_login_frame(self):
        # ... (Login frame code remains the same)
        self.login_frame = tk.Frame(self, bg="#2E8B57")
        self.login_frame.pack(pady=40, padx=40, fill="both", expand=True)

        tk.Label(self.login_frame, text="Secure Login", font=self.title_font, bg="#2E8B57", fg="white").pack(pady=(0, 20))

        username_frame = tk.Frame(self.login_frame, bg="#2E8B57")
        username_frame.pack(pady=10)
        tk.Label(username_frame, text="👤", font=self.label_font, bg="#2E8B57", fg="black").pack(side="left", padx=5)
        self.username_entry = tk.Entry(username_frame, width=30, font=self.entry_font, bg="#F0FFF0", fg="black", insertbackground="black")
        self.username_entry.pack(side="left")

        password_frame = tk.Frame(self.login_frame, bg="#2E8B57")
        password_frame.pack(pady=10)
        tk.Label(password_frame, text="🔑", font=self.label_font, bg="#2E8B57", fg="black").pack(side="left", padx=5)
        self.password_entry = tk.Entry(password_frame, show="*", width=30, font=self.entry_font, bg="#F0FFF0", fg="black", insertbackground="black")
        self.password_entry.pack(side="left")

        tk.Button(self.login_frame, text="Login", command=self.login, font=self.button_font, bg="black", fg="white", relief="flat", padx=10).pack(pady=20)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        is_authenticated, role = auth.authenticate_user(username, password)

        if is_authenticated:
            self.current_user = {'username': username, 'role': role, 'password': password}
            self.login_frame.destroy()
            self.show_main_app(self.current_user['role'])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_main_app(self, role):
        main_frame = tk.Frame(self, bg="#2E8B57")
        main_frame.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        if role == 'Admin':
            self.create_admin_panel(self.notebook)
        else: # Doctor or Nurse
            self.create_inbox_panel(self.notebook)
            self.create_messaging_panel(self.notebook)
            self.create_file_transfer_panel(self.notebook)

    def create_admin_panel(self, notebook):
        admin_frame = ttk.Frame(notebook, padding="10")
        notebook.add(admin_frame, text='User Management')

        form_frame = tk.LabelFrame(admin_frame, text="Create New User", font=self.label_font, padx=10, pady=10)
        form_frame.pack(fill="x", pady=10)

        tk.Label(form_frame, text="Username:", font=self.label_font).grid(row=0, column=0, sticky="w")
        new_username = tk.Entry(form_frame, font=self.entry_font, width=25)
        new_username.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Password:", font=self.label_font).grid(row=1, column=0, sticky="w")
        new_password = tk.Entry(form_frame, show="*", font=self.entry_font, width=25)
        new_password.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Role:", font=self.label_font).grid(row=2, column=0, sticky="w")
        role_var = tk.StringVar()
        role_menu = ttk.Combobox(form_frame, textvariable=role_var, values=['Doctor', 'Nurse'], state="readonly", width=23)
        role_menu.grid(row=2, column=1, pady=5)
        role_menu.set('Doctor')

        list_frame = tk.LabelFrame(admin_frame, text="Current Users", font=self.label_font, padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, pady=10)

        user_tree = ttk.Treeview(list_frame, columns=("Username", "Role"), show="headings")
        user_tree.heading("Username", text="Username")
        user_tree.heading("Role", text="Role")
        user_tree.pack(fill="both", expand=True)

        def refresh_user_list():
            for i in user_tree.get_children():
                user_tree.delete(i)
            for user in database.get_all_users():
                user_tree.insert("", "end", values=(user['username'], user['role']))

        def create_user_action():
            success, msg = auth.create_user(new_username.get(), new_password.get(), role_var.get())
            messagebox.showinfo("User Creation", msg)
            if success:
                new_username.delete(0, tk.END)
                new_password.delete(0, tk.END)
                refresh_user_list()

        tk.Button(form_frame, text="Create User", command=create_user_action, font=self.button_font).grid(row=3, columnspan=2, pady=10)
        refresh_user_list()

    def create_inbox_panel(self, notebook):
        inbox_frame = ttk.Frame(notebook, padding="10")
        notebook.add(inbox_frame, text='📥 Inbox')

        tk.Label(inbox_frame, text="Your received messages and files:", font=self.label_font).pack(pady=10)

        self.inbox_tree = ttk.Treeview(inbox_frame, columns=("Type", "From", "Timestamp"), show="headings")
        self.inbox_tree.heading("Type", text="Type")
        self.inbox_tree.heading("From", text="From")
        self.inbox_tree.heading("Timestamp", text="Timestamp")
        self.inbox_tree.pack(fill="both", expand=True)

        self.refresh_inbox()

        tk.Button(inbox_frame, text="Decrypt Selected", command=self.decrypt_selected, font=self.button_font).pack(pady=10)

    def refresh_inbox(self):
        for i in self.inbox_tree.get_children():
            self.inbox_tree.delete(i)

        messages = database.get_messages_for_user(self.current_user['username'])
        for msg in messages:
            self.inbox_tree.insert("", "end", values=("Message", msg['sender_username'], msg['timestamp']), iid=f"msg_{msg['id']}")

        files = database.get_files_for_user(self.current_user['username'])
        for f in files:
            self.inbox_tree.insert("", "end", values=("File", f['sender_username'], f['timestamp']), iid=f"file_{f['id']}")

    def decrypt_selected(self):
        selected_item = self.inbox_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item to decrypt.")
            return

        item_id = selected_item[0]
        item_type, db_id = item_id.split("_")
        db_id = int(db_id)

        password = simpledialog.askstring("Password", "Please enter your password to decrypt:", show='*')
        if not password or not auth.check_password(password, database.get_user(self.current_user['username'])['password_hash']):
            messagebox.showerror("Authentication Failed", "Incorrect password.")
            return

        if item_type == "msg":
            messages = database.get_messages_for_user(self.current_user['username'])
            message_to_decrypt = next((m for m in messages if m['id'] == db_id), None)

            if message_to_decrypt:
                encrypted_key = message_to_decrypt['encrypted_session_key']
                session_key = encryption.decrypt_with_private_key(encrypted_key, self.current_user['username'], password)

                if session_key:
                    decrypted_message = encryption.decrypt_message(message_to_decrypt['encrypted_message'], session_key)
                    messagebox.showinfo("Decrypted Message", decrypted_message)
                else:
                    messagebox.showerror("Decryption Failed", "Could not decrypt the message key. The password may be incorrect or the key is corrupt.")

        elif item_type == "file":
            files = database.get_files_for_user(self.current_user['username'])
            file_to_decrypt = next((f for f in files if f['id'] == db_id), None)

            if file_to_decrypt:
                encrypted_key = file_to_decrypt['encrypted_session_key']
                session_key = encryption.decrypt_with_private_key(encrypted_key, self.current_user['username'], password)

                if session_key:
                    save_path = filedialog.asksaveasfilename(initialfile=file_to_decrypt['filename'])
                    if save_path:
                        decrypted_data = encryption.decrypt_data(file_to_decrypt['encrypted_file'], session_key)
                        if decrypted_data:
                            with open(save_path, "wb") as f:
                                f.write(decrypted_data)
                            messagebox.showinfo("Success", f"File decrypted and saved to {save_path}")
                        else:
                            messagebox.showerror("Decryption Failed", "File content could not be decrypted.")
                else:
                    messagebox.showerror("Decryption Failed", "Could not decrypt the file key. The password may be incorrect or the key is corrupt.")

    def create_messaging_panel(self, notebook):
        messaging_frame = ttk.Frame(notebook, padding="10")
        notebook.add(messaging_frame, text='✉️ Send Message')

        tk.Label(messaging_frame, text="Compose a secure message:", font=self.label_font).pack(pady=5)

        message_text = tk.Text(messaging_frame, height=10, width=60, font=self.entry_font)
        message_text.pack(pady=10, padx=10)

        recipient_frame = tk.Frame(messaging_frame)
        recipient_frame.pack(pady=5)
        tk.Label(recipient_frame, text="Recipient:", font=self.label_font).pack(side="left")

        users = [user['username'] for user in database.get_all_users() if user['username'] != self.current_user['username']]
        recipient_var = tk.StringVar()
        recipient_menu = ttk.Combobox(recipient_frame, textvariable=recipient_var, values=users, state="readonly")
        recipient_menu.pack(side="left")

        def send_message_action():
            recipient = recipient_var.get()
            message = message_text.get("1.0", tk.END).strip()
            if not recipient or not message:
                messagebox.showwarning("Missing Info", "Please select a recipient and write a message.")
                return

            session_key = encryption.generate_key()
            encrypted_message = encryption.encrypt_message(message, session_key)

            recipient_public_key = database.get_public_key(recipient)
            encrypted_key = encryption.encrypt_with_public_key(session_key, recipient_public_key)

            database.save_message(self.current_user['username'], recipient, encrypted_message, encrypted_key)
            messagebox.showinfo("Success", "Message sent successfully.")
            message_text.delete("1.0", tk.END)
            self.refresh_inbox()

        tk.Button(messaging_frame, text="Encrypt & Send", command=send_message_action, font=self.button_font).pack(pady=10)

    def create_file_transfer_panel(self, notebook):
        file_frame = ttk.Frame(notebook, padding="10")
        notebook.add(file_frame, text='📁 Transfer File')

        tk.Label(file_frame, text="Select a file to encrypt and send:", font=self.label_font).pack(pady=10)

        file_path_var = tk.StringVar()

        def select_file():
            path = filedialog.askopenfilename()
            if path:
                file_path_var.set(path)
                file_label.config(text=os.path.basename(path))

        tk.Button(file_frame, text="Browse...", command=select_file, font=self.button_font).pack()
        file_label = tk.Label(file_frame, text="No file selected.", font=self.label_font, wraplength=400)
        file_label.pack(pady=10)

        recipient_frame = tk.Frame(file_frame)
        recipient_frame.pack(pady=10)
        tk.Label(recipient_frame, text="Recipient:", font=self.label_font).pack(side="left")

        users = [user['username'] for user in database.get_all_users() if user['username'] != self.current_user['username']]
        recipient_var = tk.StringVar()
        recipient_menu = ttk.Combobox(recipient_frame, textvariable=recipient_var, values=users, state="readonly")
        recipient_menu.pack(side="left")

        def send_file_action():
            recipient = recipient_var.get()
            filepath = file_path_var.get()
            if not recipient or not filepath:
                messagebox.showwarning("Missing Info", "Please select a file and a recipient.")
                return

            session_key = encryption.generate_key()

            with open(filepath, "rb") as f:
                file_data = f.read()

            encrypted_file_data = encryption.encrypt_data(file_data, session_key)

            recipient_public_key = database.get_public_key(recipient)
            encrypted_key = encryption.encrypt_with_public_key(session_key, recipient_public_key)

            database.save_file(self.current_user['username'], recipient, os.path.basename(filepath), encrypted_file_data, encrypted_key)
            messagebox.showinfo("Success", "File sent successfully.")
            file_path_var.set("")
            file_label.config(text="No file selected.")
            self.refresh_inbox()

        tk.Button(file_frame, text="Encrypt & Send", command=send_file_action, font=self.button_font).pack(pady=20)


if __name__ == "__main__":
    database.create_tables()
    app = App()
    app.mainloop()
