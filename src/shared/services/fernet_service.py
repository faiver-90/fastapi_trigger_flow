
import os
from typing import Union
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()


class FernetService:
    def __init__(self, fernet_key: str = None):
        """
        :param fernet_key: Ключ в виде строки. Если None, берется из FERNET_KEY.
        """
        key = os.getenv("FERNET_KEY", fernet_key)
        if not key:
            raise ValueError("Fernet key not specified (neither in argument nor in FERNET_KEY)")
        self.fernet = Fernet(key.encode())

    def encrypt_str(self, data: Union[str, bytes]) -> str:
        """Шифрует строку или байты, возвращает base64-строку."""
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.fernet.encrypt(data)
        return encrypted.decode()

    def decrypt_str(self, encrypted_data: Union[str, bytes]) -> str:
        """Расшифровывает данные в исходную строку."""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        try:
            decrypted = self.fernet.decrypt(encrypted_data)
            return decrypted.decode()
        except InvalidToken as e:
            raise ValueError("Invalid key or corrupted data") from e
