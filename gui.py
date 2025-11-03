# gui.py
import tkinter as tk
from tkinter import font, ttk, filedialog, messagebox, simpledialog
import encryption
import base64
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Encryptor/Decryptor")
        self.geometry("700x550")

        # --- Style Configuration ---
        self.configure(bg="#2E8B57") # SeaGreen background
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        style = ttk.Style(self)
        style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"))
        style.configure("TFrame", background="#F0FFF0") # Honeydew color for frames
        style.configure("TLabel", background="#F0FFF0", font=self.label_font)
        style.configure("TButton", font=self.button_font)

        self.eval('tk::PlaceWindow . center')

        self.setup_main_interface()

    def setup_main_interface(self):
        header_frame = tk.Frame(self, bg="#2E8B57", pady=10)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="🔒 Secure Text & File Tool", font=self.title_font, bg="#2E8B57", fg="white").pack()

        notebook = ttk.Notebook(self, padding=10)
        notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.create_text_panel(notebook)
        self.create_file_panel(notebook)

    def create_text_panel(self, notebook):
        text_frame = ttk.Frame(notebook, padding="20")
        notebook.add(text_frame, text='✉️ Encrypt/Decrypt Text')

        # --- Input ---
        tk.Label(text_frame, text="Enter Text Below:").grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")
        input_text = tk.Text(text_frame, height=8, width=60, font=("Helvetica", 11))
        input_text.grid(row=1, column=0, columnspan=2, pady=5)

        # --- Password ---
        tk.Label(text_frame, text="Password:").grid(row=2, column=0, pady=5, sticky="e")
        password_entry = tk.Entry(text_frame, show="*", width=30)
        password_entry.grid(row=2, column=1, pady=5, sticky="w")

        # --- Actions ---
        button_frame = ttk.Frame(text_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        def encrypt_action():
            password = password_entry.get()
            text = input_text.get("1.0", tk.END).strip()
            if not password or not text:
                messagebox.showwarning("Missing Info", "Please provide both text and a password.")
                return
            encrypted_blob = encryption.encrypt_text(text, password)
            # Use base64 for safe copy-pasting
            input_text.delete("1.0", tk.END)
            input_text.insert("1.0", base64.b64encode(encrypted_blob).decode('utf-8'))
            messagebox.showinfo("Success", "Text has been encrypted.")

        def decrypt_action():
            password = password_entry.get()
            b64_text = input_text.get("1.0", tk.END).strip()
            if not password or not b64_text:
                messagebox.showwarning("Missing Info", "Please provide the encrypted text and the password.")
                return
            try:
                encrypted_blob = base64.b64decode(b64_text)
                decrypted_text = encryption.decrypt_text(encrypted_blob, password)
                if decrypted_text is not None:
                    input_text.delete("1.0", tk.END)
                    input_text.insert("1.0", decrypted_text)
                    messagebox.showinfo("Success", "Text has been decrypted.")
                else:
                    messagebox.showerror("Decryption Failed", "Failed to decrypt. Check the password or data.")
            except (base64.binascii.Error, ValueError):
                messagebox.showerror("Invalid Data", "The input text is not valid encrypted data.")

        ttk.Button(button_frame, text="Encrypt", command=encrypt_action).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Decrypt", command=decrypt_action).pack(side="left", padx=10)

    def create_file_panel(self, notebook):
        file_frame = ttk.Frame(notebook, padding="20")
        notebook.add(file_frame, text='📁 Encrypt/Decrypt File')

        file_path_var = tk.StringVar()

        # --- File Selection ---
        tk.Label(file_frame, text="Selected File:").grid(row=0, column=0, sticky="w")
        file_label = tk.Label(file_frame, text="No file selected.", wraplength=400, anchor="w")
        file_label.grid(row=0, column=1, columnspan=2, sticky="w", pady=(0, 10))

        def select_file():
            path = filedialog.askopenfilename()
            if path:
                file_path_var.set(path)
                file_label.config(text=os.path.basename(path))

        ttk.Button(file_frame, text="Browse...", command=select_file).grid(row=1, column=0, columnspan=3, pady=10)

        # --- Password ---
        tk.Label(file_frame, text="Password:").grid(row=2, column=0, pady=20, sticky="e")
        password_entry = tk.Entry(file_frame, show="*", width=30)
        password_entry.grid(row=2, column=1, pady=20, sticky="w")

        # --- Actions ---
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)

        def encrypt_action():
            password = password_entry.get()
            input_file = file_path_var.get()
            if not password or not input_file:
                messagebox.showwarning("Missing Info", "Please select a file and provide a password.")
                return

            output_file = filedialog.asksaveasfilename(defaultextension=".enc",
                                                       initialfile=os.path.basename(input_file) + ".enc")
            if output_file:
                encryption.encrypt_file(input_file, output_file, password)
                messagebox.showinfo("Success", f"File encrypted successfully to:\n{output_file}")
                file_path_var.set("")
                file_label.config(text="No file selected.")

        def decrypt_action():
            password = password_entry.get()
            input_file = file_path_var.get()
            if not password or not input_file:
                messagebox.showwarning("Missing Info", "Please select a file and provide a password.")
                return

            output_file = filedialog.asksaveasfilename(initialfile=input_file.rsplit('.enc', 1)[0] if input_file.endswith('.enc') else input_file + ".dec")
            if output_file:
                success = encryption.decrypt_file(input_file, output_file, password)
                if success:
                    messagebox.showinfo("Success", f"File decrypted successfully to:\n{output_file}")
                    file_path_var.set("")
                    file_label.config(text="No file selected.")
                else:
                    messagebox.showerror("Decryption Failed", "Failed to decrypt. Check the password or file.")

        ttk.Button(button_frame, text="Encrypt File", command=encrypt_action).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Decrypt File", command=decrypt_action).pack(side="left", padx=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
