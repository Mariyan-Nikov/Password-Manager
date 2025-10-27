import json
import os
import base64
from cryptography.fernet import Fernet

DATA_FILE = "passwords.json"
KEY_FILE = "key.key"

#Ключове#

def generate_key():
    """Generate a new encryption key if one doesn't exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    """Load the existing encryption key."""
    return open(KEY_FILE, "rb").read()

#Енкрипция#

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()

#Мениджър#
def load_passwords():
    """Load passwords from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_passwords(passwords):
    """Save passwords to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

def add_password(master_key):
    """Add a new password entry."""
    account = input("Account name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    encrypted_password = encrypt_message(password, master_key)

    data = load_passwords()
    data[account] = {"username": username, "password": encrypted_password}
    save_passwords(data)
    print("✅ Password saved successfully!")

def view_passwords(master_key):
    """View saved passwords (decrypted)."""
    data = load_passwords()
    if not data:
        print("No passwords saved yet.")
        return

    for account, info in data.items():
        decrypted_pass = decrypt_message(info["password"], master_key)
        print(f"🔹 {account}\n   Username: {info['username']}\n   Password: {decrypted_pass}\n")

def list_accounts():
    """List saved account names."""
    data = load_passwords()
    if not data:
        print("No accounts saved yet.")
        return
    print("🔐 Saved accounts:")
    for account in data.keys():
        print(f" - {account}")

#Главно#

def main():
    print("=== Secure Password Manager ===")
    generate_key()
    master_key = load_key()

    while True:
        print("\nMenu:")
        print("1. Add new password")
        print("2. View all passwords")
        print("3. List accounts")
        print("4. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            add_password(master_key)
        elif choice == "2":
            view_passwords(master_key)
        elif choice == "3":
            list_accounts()
        elif choice == "4":
            print("Goodbye 👋 Stay safe!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
