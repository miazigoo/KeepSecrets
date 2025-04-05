from cryptography.fernet import Fernet

from redis_db import get_redis_connection


def generate_key():
    """Генерация ключа для шифрования"""
    return Fernet.generate_key().decode('utf-8')


def encrypt_secret(secret, key):
    """Шифрование секрета"""
    fernet = Fernet(key)
    encrypted_secret = fernet.encrypt(secret.encode()).decode('utf-8')
    return encrypted_secret


def decrypt_secret(encrypted_secret, key):
    """Расшифровка секрета"""
    fernet = Fernet(key.encode())
    decrypted_secret = fernet.decrypt(encrypted_secret).decode('utf-8')
    return decrypted_secret


def store_secret_in_redis(secret_key, secret):
    """Сохраняем секрет в Redis"""
    redis_conn = get_redis_connection()
    redis_conn.set(secret_key, secret)
    redis_conn.expire(secret_key, 300)  # Устаревание через 5 минуток


def read_secret_from_redis(secret_key):
    """Получаем секрет из Redis"""
    redis_conn = get_redis_connection()
    return redis_conn.get(secret_key)


def delete_secret_from_redis(secret_key):
    """Удаляем секрет из Redis"""
    redis_conn = get_redis_connection()
    redis_conn.delete(secret_key)