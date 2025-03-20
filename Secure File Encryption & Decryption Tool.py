from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib

# Function to pad data to be a multiple of 16 bytes
def pad(data):
    return data + b" " * (16 - len(data) % 16)

# Generate a key from a password
def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

# Encrypt function using AES-CBC
def encrypt_file(filename, password):
    key = generate_key(password)
    iv = get_random_bytes(16)  # Initialization Vector
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(pad(file_data))
    
    with open(filename + ".enc", 'wb') as file:
        file.write(iv + encrypted_data)  # Store IV at the beginning
    
    messagebox.showinfo("Success", "File encrypted successfully!")

# Decrypt function using AES-CBC
def decrypt_file(filename, password):
    key = generate_key(password)
    
    with open(filename, 'rb') as file:
        iv = file.read(16)  # Read the IV first
        encrypted_data = file.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data).rstrip(b" ")
    
    with open(filename.replace(".enc", "_decrypted"), 'wb') as file:
        file.write(decrypted_data)
    
    messagebox.showinfo("Success", "File decrypted successfully!")

# GUI setup
def open_file_encrypt():
    filename = filedialog.askopenfilename()
    if filename:
        password = tk.simpledialog.askstring("Password", "Enter encryption password:", show='*')
        if password:
            encrypt_file(filename, password)

def open_file_decrypt():
    filename = filedialog.askopenfilename()
    if filename:
        password = tk.simpledialog.askstring("Password", "Enter decryption password:", show='*')
        if password:
            decrypt_file(filename, password)

# GUI
tk_root = tk.Tk()
tk_root.title("File Encryption Tool")

tk.Button(tk_root, text="Encrypt File", command=open_file_encrypt).pack(pady=10)
tk.Button(tk_root, text="Decrypt File", command=open_file_decrypt).pack(pady=10)

tk_root.mainloop()
