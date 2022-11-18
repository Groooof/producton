import pydantic as pd
import uuid
import enum
import typing as tp


class Roles(str, enum.Enum):
    moderator = 'moderator'
    marker = 'marker'
    undefined = 'undefined'


class User(pd.BaseModel):
    id: int
    hashed_password: tp.Optional[str]
    role: Roles
    is_superuser: bool
    