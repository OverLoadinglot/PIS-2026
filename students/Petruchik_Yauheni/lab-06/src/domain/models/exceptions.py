class BudgetException(Exception):
    pass


class MemberNotFoundException(BudgetException):
    pass


class CategoryNotFoundException(BudgetException):
    pass


class BudgetAlreadyArchivedException(BudgetException):
    pass


class LimitExceededException(BudgetException):
    pass
