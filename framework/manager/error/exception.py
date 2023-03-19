class BaseException(Exception):
    pass

class ModemLockedByOtherThreadException(BaseException):
    pass

class ModemRebootException(BaseException):
    pass

class NoTaskRunningException(BaseException):
    pass