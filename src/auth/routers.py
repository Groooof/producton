import asyncpg
from fastapi import APIRouter, Depends, Response
from fastapi.responses import Response

from src.dependencies import get_db_connection
from src.auth import service as auth
from src.auth import backends
from src.auth import exceptions as exc
from src.auth import schemas as sch
from src.schemas import Error
from src.auth import utils
from src import config

router = APIRouter(prefix='/api/v1', tags=['auth'])


@router.post('/user', 
             response_class=Response, 
             responses={409: {'description': 'User already exists', 'model': Error}})
async def signup(body: sch.UserCredentials, con: asyncpg.Connection = Depends(get_db_connection)):  
    await auth.create_user(con, body.login, body.password)


@router.post('/login', 
             response_model=sch.JWTTokensResponse, 
             responses={400: {'description': 'Incorrect login/password', 'model': Error}})
async def login(response: Response, body: sch.UserCredentials, con: asyncpg.Connection = Depends(get_db_connection)):
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    
    # проверяем в бд наличие предоставленной комбинации логин/пароль и соответствие логина паролю
    user = await auth.verify_user(con, body.login, body.password)
    # генерация токенов
    access_token = auth.generate_jwt_access(user.id, user.role, user.is_superuser)
    refresh_token = auth.generate_jwt_refresh()
    await auth.create_refresh_token(con, user.id, refresh_token)
    
    return sch.JWTTokensResponse(access_token=access_token, 
                                 refresh_token=refresh_token, 
                                 expires_in=config.JWT_AT_LIFETIME.seconds, 
                                 role=user.role)
    

@router.post('/logout', response_class=Response)
async def logout(body: sch.RefreshTokenRequest,
                 access_token: utils.JWTToken = Depends(backends.jwt_auth),
                 con: asyncpg.Connection = Depends(get_db_connection)):
    # принимаем оба токена, получаем id пользователя
    user_id = access_token.payload.get('sub')
    # проверяем в бд принадлежит ли refresh token данному пользователю
    await auth.verify_refresh_token(con, user_id, body.refresh_token)
    # удаляем токен
    await auth.delete_refresh_token(con, body.refresh_token)


@router.post('/refresh',
             response_model=sch.JWTTokensResponse,
             responses={401: {'description': 'Invalid access and (or) refresh token(s)', 'model': Error}})
async def refresh(response: Response,
                  body: sch.RefreshTokenRequest, 
                  access_token: utils.JWTToken = Depends(backends.check_signature), 
                  con: asyncpg.Connection = Depends(get_db_connection)):
    
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    
    # получае данные о пользователе из токена
    user_id = access_token.user
    role = access_token.role
    is_superuser = access_token.is_superuser
    # проверяем в бд принадлежит ли refresh token данному пользователю
    await auth.verify_refresh_token(con, user_id, body.refresh_token)
    # генерируем новые токены
    new_access_token = auth.generate_jwt_access(user_id, role, is_superuser)
    new_refresh_token = auth.generate_jwt_refresh()
    # обновляем токен в бд
    await auth.update_refresh_token(con, body.refresh_token, new_refresh_token)
    return sch.JWTTokensResponse(access_token=new_access_token, 
                                 refresh_token=new_refresh_token, 
                                 expires_in=config.JWT_AT_LIFETIME.seconds,
                                 role=access_token.role)
