import uuid
import secrets
import hashlib
import hmac
from .converters import _str


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def generate_random_string(n: int) -> str:
    return secrets.token_hex(n)


def pbkdf2_hmac(string: str, salt: str, alg='sha512', iterations=50_000) -> str:
    return hashlib.pbkdf2_hmac(alg, string.encode(), salt.encode(), iterations).hex()


def hs256(string: str, key: str) -> bytes:
    return hmac.new(_str.to_bytes(key), _str.to_bytes(string), hashlib.sha256).digest()


def compare_strings(s_1: str, s_2: str) -> bool:
    return secrets.compare_digest(s_1, s_2)
