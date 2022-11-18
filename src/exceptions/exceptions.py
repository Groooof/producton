from src.utils.custom import CustomHTTPException

    
INVALID_REQUEST_EXCEPTION = CustomHTTPException(400, 'invalid_request', 'Invalid request data')
ACCESS_DENIED = CustomHTTPException(403, 'access_denied')




    
