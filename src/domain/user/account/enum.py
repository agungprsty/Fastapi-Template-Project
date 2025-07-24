from src.utils.enum import BaseEnum

class AccountStatus(BaseEnum):
    ACTIVE = "active"
    PENDING = "pending"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class AuthenticationRole(BaseEnum):
    USER = "user"
    DOCTOR = "doctor"
    BACKOFFICE = "backoffice"

class DateFormat(BaseEnum):
    DDMMYY = "dd/mm/yy"
    MMDDYY = "mm/dd/yy"

class TimeFormat(BaseEnum):
    _24H = "24h"
    _12H = "12h"

class NumberFormat(BaseEnum):
    TITIK = "1.234.567"
    KOMA = "1,234,567"

class Currency(BaseEnum):
    IDR = "idr"

class Lang(BaseEnum):
    ID = "id"
    EN = "en"