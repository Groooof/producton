import typing as tp
import datetime as dt
from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security.http import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from src.auth import dto    
from src import exceptions as exc
from src.auth import utils
from src.utils.converters import _dt
from src import config


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> tp.Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise exc.INVALID_TOKEN
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise exc.INVALID_TOKEN
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


def get_token(token = Depends(CustomHTTPBearer())) -> utils.JWTToken:
    '''
    Получаем и парсим токен из заголовка
    '''
    try:
        jwt = utils.JWTToken(token.credentials) 
    except ValueError:
        raise exc.INVALID_TOKEN
    return jwt
    
    
def check_signature(jwt: utils.JWTToken = Depends(get_token)) -> utils.JWTToken:
    '''
    Проверяем подпись токена
    '''
    if not jwt.verify(config.jwt_env.SECRET):
        raise exc.INVALID_TOKEN
    return jwt


def check_expires(jwt: utils.JWTToken = Depends(get_token)) -> utils.JWTToken:
    '''
    Проверяем срок действия токена
    '''
    token_expires_timestamp = jwt.exp
    token_expires_dt = _dt.from_timestamp(token_expires_timestamp)
    if dt.datetime.now() > token_expires_dt:
        raise exc.TOKEN_EXPIRED
    return jwt


def check_role(role: str, jwt: utils.JWTToken = Depends(get_token)) -> utils.JWTToken:
    '''
    Проверяем роль пользователя
    '''
    if role != jwt.role:
        raise exc.ACCESS_DENIED(error_description=f'Only for {role}')
    return jwt


def is_superuser(jwt: utils.JWTToken = Depends(get_token)) -> utils.JWTToken:
    '''
    Проверяем, является ли пользователь суперпользователем
    '''
    if not jwt.is_superuser:
        raise exc.ACCESS_DENIED(error_description='Only for superuser')
    return jwt


def is_moderator(jwt: utils.JWTToken = Depends(get_token)) -> utils.JWTToken:
    '''
    Проверяем, является ли пользователь модератором
    '''
    return check_role(dto.Roles.moderator, jwt)


def is_marker(jwt: utils.JWTToken = Depends(get_token)) -> utils.JWTToken:
    '''
    Проверяем, является ли пользователь разметчиком
    '''
    return check_role(dto.Roles.marker, jwt)


def jwt_auth(jwt: utils.JWTToken = Depends(get_token)) -> utils.JWTToken:
    '''
    Базовый алгоритм авторизации (проверка подписи и срока действия токена)
    '''
    check_signature(jwt)
    check_expires(jwt)
    return jwt


