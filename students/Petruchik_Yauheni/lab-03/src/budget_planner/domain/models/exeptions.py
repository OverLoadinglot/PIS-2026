class DomainException(Exception):
    """Базовое исключение домена"""
    pass

class LimitExceededException(DomainException):
    pass

class InvalidTransactionException(DomainException):
    pass

class MemberNotFoundException(DomainException):
    pass

class CategoryNotFoundException(DomainException):
    pass

class BudgetAlreadyArchivedException(DomainException):
    pass