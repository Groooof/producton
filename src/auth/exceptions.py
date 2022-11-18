from src.utils.custom import CustomHTTPException


INVALID_CLIENT = CustomHTTPException(400, 'invalid_client')
INVALID_TOKEN = CustomHTTPException(401, 'invalid_token')
TOKEN_EXPIRED = CustomHTTPException(401, 'token_expired')
USER_ALREARY_EXISIS = CustomHTTPException(409, 'user_already_exists')
