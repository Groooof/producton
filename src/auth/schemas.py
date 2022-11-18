import uuid
import pydantic as pd
from src import config


class UserCredentials(pd.BaseModel):
    login: str
    password: str
    
    
class JWTTokensResponse(pd.BaseModel):
    access_token: str
    token_type: str = config.JWT_AT_TYPE
    expires_in: int
    refresh_token: uuid.UUID
    role: str
    
    
class RefreshTokenRequest(pd.BaseModel):
    refresh_token: uuid.UUID
    
