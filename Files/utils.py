"""
Proste szyfrowanie i odszyfrowywanie haseł przy użyciu `cryptography.Fernet`.
"""

import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    open(KEY_FILE, "wb").write(Fernet.generate_key())
fernet = Fernet(open(KEY_FILE, "rb").read())

def encrypt(data):
    """Zwraca zaszyfrowany tekst (base64)."""
    return fernet.encrypt(data.encode()).decode()

def decrypt(token):
    """Odszyfrowuje zaszyfrowany token do tekstu jawnego."""
    return fernet.decrypt(token.encode()).decode()
