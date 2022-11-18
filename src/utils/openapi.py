import typing as tp
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI


class CustomOpenAPIGenerator:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        
    def __call__(self) -> tp.Dict[str, tp.Any]:
        if self.app.openapi_schema:
            return self.app.openapi_schema
        self.app.openapi_schema = get_openapi(
            title=self.app.title,
            version=self.app.version,
            description=self.app.description,
            routes=self.app.routes
        )
        self._del_response('422')
        self._del_schema('HTTPValidationError')
        self._del_schema('ValidationError')

        return self.app.openapi_schema
    
    def _del_response(self, status_code: str) -> None:
        for path in self.app.openapi_schema['paths'].keys():
            for method in self.app.openapi_schema['paths'][path].keys():
                if '422' in self.app.openapi_schema['paths'][path][method]['responses']:
                    del self.app.openapi_schema['paths'][path][method]['responses'][status_code]

    def _del_schema(self, schema: str) -> None:
        if 'components' not in self.app.openapi_schema:
            return
        if 'schemas' not in self.app.openapi_schema['components']:
            return
        if schema in self.app.openapi_schema['components']['schemas']:
            del self.app.openapi_schema['components']['schemas'][schema]

    

