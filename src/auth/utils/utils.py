from functools import lru_cache
import typing as tp

from src.utils.crypto import (
    pbkdf2_hmac,
    generate_random_string,
    compare_strings,
    hs256
)
from src.utils.converters import (
    _str,
    _b64
)


class PasswordHasher:
    '''
    Класс, содержащий методы для реализации хэширования паролей
    '''
    _salt_len = 32
    
    @classmethod
    def hash(cls, password) -> str:
        '''
        Генерация хэша с солью для заданного паспорта
        '''
        salt = cls._gen_salt()
        salted_hash = cls._gen_hash_with_salt(password, salt)
        return cls._join_salt_to_hash(salted_hash, salt)
        
    @classmethod
    def verify(cls, password_for_verify, salted_hash_with_salt):
        '''
        Проверка соответствует ли пароль (строка) хэшированному паролю
        '''
        salt, _ = cls._split_hash_with_salt(salted_hash_with_salt)
        salted_hash_for_verify = cls._gen_hash_with_salt(password_for_verify, salt)
        salted_hash_with_salt_for_verify = cls._join_salt_to_hash(salted_hash_for_verify, salt)
        return compare_strings(salted_hash_with_salt_for_verify, salted_hash_with_salt)
        
        
    @staticmethod
    def _join_salt_to_hash(hash, salt) -> str:
        return f'{salt}{hash}'
    
    @classmethod
    def _split_hash_with_salt(cls, salted_hash_with_salt) -> tp.Tuple[str, str]:
        return salted_hash_with_salt[:cls._salt_len], salted_hash_with_salt[cls._salt_len:]
    
    @classmethod
    def _gen_salt(cls) -> str:
        return generate_random_string(cls._salt_len // 2)
    
    @staticmethod
    def _gen_hash_with_salt(string: str, salt: str) -> str:
        return pbkdf2_hmac(string, salt)
    
    
class BaseJWTToken:
    def __init__(self, token: tp.Optional[str] = None) -> None:
        self.header = {}
        self.payload = {}
        self.signature = b''
        
        if token is not None:
            try:
                self._parse(token)
            except Exception:
                raise ValueError
    
    def sign(self, secret: str):
        '''
        Генерация подписи на основе имеющихся в объекте данных
        '''
        self.signature = self._gen_sign(secret)

    def verify(self, secret: str) -> bool:
        '''
        Проверка, соответствуют ли данные объекта с имеющейся подписью
        '''
        correct_sign = self._gen_sign(secret)
        return correct_sign == self.signature
    
    def _gen_sign(self, secret: str) -> bytes:
        '''
        Генерация подписи
        '''
        header_b64 = _b64.from_dict(self.header)
        payload_b64 = _b64.from_dict(self.payload)
        
        unsigned_token = header_b64 + '.' + payload_b64
        
        return hs256(unsigned_token, secret)
    
    @lru_cache(maxsize=128)
    def _parse(self, token: str):
        '''
        Токен в виде строки преобразеутся в объект
        '''
        header_b64, payload_b64, signature_b64 = token.split('.')
        self.header = _b64.to_dict(header_b64)
        self.payload = _b64.to_dict(payload_b64)
        self.signature = _b64.to_bytes(_str.to_bytes(signature_b64))
    
    def __str__(self) -> str:
        header_b64 = _b64.from_dict(self.header)
        payload_b64 = _b64.from_dict(self.payload)
        signature_b64 = _str.from_bytes(_b64.from_bytes(self.signature))
        return header_b64 + '.' + payload_b64 + '.' + signature_b64 


class JWTToken(BaseJWTToken):
    '''
    Расширение базового класса для удобного доступа к данным
    '''
    @property
    def user(self) -> str:
        return self.payload['sub']
    
    @property
    def exp(self) -> int:
        return self.payload['exp']
    
    @property
    def role(self) -> str:
        return self.payload['role']
    
    @property
    def is_superuser(self) -> bool:
        return self.payload['is_superuser']
    
    
