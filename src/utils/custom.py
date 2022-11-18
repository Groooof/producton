import typing as tp


class CustomHTTPException(Exception):
    def __init__ (self,
                  status_code: int,
                  error: tp.Optional[str] = None,
                  error_description: tp.Optional[str] = None,
                  headers: tp.Optional[dict] = None,
                  ) -> None:
        self.status_code = status_code
        self.error = error
        self.error_description = error_description
        self.headers = headers
        
    def __call__(self, 
                 status_code: tp.Optional[int] = None,
                 error: tp.Optional[str] = None,
                 error_description: tp.Optional[str] = None,
                 headers: tp.Optional[dict] = None,) -> 'CustomHTTPException':
        self.status_code = status_code if status_code is not None else self.status_code
        self.error = error if error is not None else self.error
        self.error_description = error_description if error_description is not None else self.error_description
        self.headers = headers if headers is not None else self.headers
        return self