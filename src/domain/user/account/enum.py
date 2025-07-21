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