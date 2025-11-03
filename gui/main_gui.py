import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
# Add path to encryption module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'encryption')))
from encryptor import encrypt_message, decrypt_message

# GUI setup
root = tk.Tk()
root.title("Secure Message Sender")
root.geometry("600x400")

# Create tabbed layout
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create two tabs (frames)
message_tab = ttk.Frame(notebook)
file_tab = ttk.Frame(notebook)

# Add tabs to notebook
notebook.add(message_tab, text="Message Tools")
notebook.add(file_tab, text="File Tools")

# ---------- Message Encryption ----------
tk.Label(message_tab, text="Enter your message:").pack(pady=5)
entry = tk.Entry(message_tab, width=60)
entry.pack(pady=5)

def send_message():
    message = entry.get()
    encrypted = encrypt_message(message)
    encrypted_output.set(encrypted)

tk.Button(message_tab, text="Encrypt Message", command=send_message).pack(pady=5)

# Display encrypted message (copyable)
tk.Label(message_tab, text="Encrypted message:").pack(pady=5)
encrypted_output = tk.StringVar()
output_entry = tk.Entry(message_tab, textvariable=encrypted_output, width=60)
output_entry.pack(pady=5)

# ---------- Message Decryption ----------
tk.Label(message_tab, text="Paste encrypted message:").pack(pady=5)
decrypt_entry = tk.Entry(message_tab, width=60)
decrypt_entry.pack(pady=5)

def clear_fields():
    entry.delete(0, tk.END)
    encrypted_output.set("")
    decrypt_entry.delete(0, tk.END)


tk.Button(message_tab, text="Clear All Fields", command=clear_fields).pack(pady=5)

def decrypt_message_gui():
    encrypted_text = decrypt_entry.get()
    try:
        decrypted = decrypt_message(encrypted_text)
        messagebox.showinfo("Decrypted Message", decrypted)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid encrypted message.\n{str(e)}")


tk.Button(message_tab, text="Decrypt Message", command=decrypt_message_gui).pack(pady=5)

# ---------- File Encryption ----------
def encrypt_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                file_data = f.read().strip()
            encrypted = encrypt_message(file_data)
            encrypted_output.set(encrypted)
            messagebox.showinfo("Success", "File encrypted. You can now save it.")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed.\n{str(e)}")

tk.Button(file_tab, text="Encrypt File", command=encrypt_file).pack(pady=5)

def save_encrypted_to_file():
    encrypted_text = encrypted_output.get()
    if encrypted_text:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(encrypted_text.strip())
            messagebox.showinfo("Saved", f"Encrypted message saved to:\n{filepath}")
    else:
        messagebox.showwarning("Empty", "No encrypted message to save.")

tk.Button(file_tab, text="Save Encrypted Message", command=save_encrypted_to_file).pack(pady=5)

def decrypt_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                encrypted_data = f.read().strip()
            decrypted = decrypt_message(encrypted_data)
            messagebox.showinfo("Decrypted File", decrypted)
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed.\n{str(e)}")

tk.Button(file_tab, text="Decrypt File", command=decrypt_file).pack(pady=5)

root.mainloop()