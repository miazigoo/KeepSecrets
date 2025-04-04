from cryptography.fernet import Fernet


def generate_key():
    """Генерация ключа для шифрования"""
    return Fernet.generate_key().decode('utf-8')


def encrypt_secret(secret, key):
    """Шифрование секрета"""
    fernet = Fernet(key)
    encrypted_secret = fernet.encrypt(secret.encode()).decode('utf-8')
    return encrypted_secret