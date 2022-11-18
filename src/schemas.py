import pydantic as pd
import typing as tp


class Error(pd.BaseModel):
    error: str
    error_description: str = pd.Field('')
    
    

