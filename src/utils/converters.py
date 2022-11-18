import base64
import json
import datetime as dt
import typing as tp


class _str:
    @staticmethod
    def to_bytes(value: str, encoding='ascii') -> bytes:
        return value.encode(encoding=encoding)
    
    @staticmethod
    def from_bytes(value: bytes, encoding='ascii') -> str:
        return value.decode(encoding=encoding)
    
    @staticmethod
    def to_dict(value: str) -> dict:
        return json.loads(value)
    
    @staticmethod
    def from_dict(value: dict) -> str:
        return json.dumps(value).replace(' ', '')
       

class _b64:
    @staticmethod
    def from_bytes(value: bytes) -> bytes:
        return base64.urlsafe_b64encode(value)
    
    @staticmethod
    def to_bytes(value: bytes) -> bytes:
        return base64.urlsafe_b64decode(value)
    
    @classmethod
    def from_dict(cls, value: dict) -> str:
        return _str.from_bytes(cls.from_bytes(_str.to_bytes(_str.from_dict(value))))

    @classmethod
    def to_dict(cls, value: str) -> dict:
        return _str.to_dict(_str.from_bytes(cls.to_bytes(_str.to_bytes(value))))


class _dt:
    @classmethod
    def to_timestamp(cls, value: dt.datetime) -> int:
        return int(value.timestamp())
    
    @classmethod
    def from_timestamp(cls, value: tp.Union[int, float]) -> dt.datetime:
        return dt.datetime.fromtimestamp(value)
