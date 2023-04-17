class BaseException(Exception):
    pass

class TimeoutException(BaseException):
    pass

class MiddlewareException(BaseException):
    pass

class MiddlewareAuthenticationException(BaseException):
    pass

class MiddlewareCarrierConnectionException(BaseException):
    pass