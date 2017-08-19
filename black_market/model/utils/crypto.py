from cryptography.fernet import Fernet
from black_market.config import FERNET_KEY


def encrypt(text):
    cipher_suite = Fernet(FERNET_KEY.encode())
    return cipher_suite.encrypt(text.encode()).decode('utf-8')


def decrypt(cipher_text):
    cipher_suite = Fernet(FERNET_KEY.encode())
    return cipher_suite.decrypt(cipher_text.encode())
