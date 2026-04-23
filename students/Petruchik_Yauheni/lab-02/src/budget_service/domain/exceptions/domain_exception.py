"""
Базовый класс для ошибок бизнес-логики
"""

class DomainException(Exception):
    pass

class LimitExceededException(DomainException):
    pass