import unittest
from datetime import date
from src.budget_planner.domain.models.value_objects import Money, CategoryName, MemberName, DateRange, TransactionType
from src.budget_planner.domain.models.entities import FamilyBudget, FamilyMember, Category, Transaction
from src.budget_planner.domain.models.exceptions import LimitExceededException, MemberNotFoundException, CategoryNotFoundException
from src.budget_planner.domain.models.events import TransactionAddedEvent, LimitExceededEvent
from src.budget_planner.domain.services.reporting_service import BudgetReportingService
from src.budget_planner.domain.models.specifications import ByCategoryIdSpecification, ByDateRangeSpecification, AndSpecification

class TestFamilyBudget(unittest.TestCase):
    def setUp(self):
        self.budget = FamilyBudget("b1", "Семейный бюджет")
        self.member = FamilyMember("m1", MemberName("Анна"), "admin")
        self.category = Category("c1", CategoryName("Продукты"), "#FF0000")
        self.budget.add_member(self.member)
        self.budget.add_category(self.category)

    def test_add_transaction_success_generates_event(self):
        tx = Transaction("t1", Money(500, "RUB"), TransactionType.EXPENSE,
                         "c1", "m1", date(2026, 4, 1), "Хлеб")
        self.budget.add_transaction(tx)
        events = self.budget.pull_events()
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], TransactionAddedEvent)
        self.assertEqual(events[0].amount.amount, 500)

    def test_limit_exceeded_raises_exception(self):
        # Устанавливаем лимит на апрель 2026
        period = DateRange(date(2026, 4, 1), date(2026, 4, 30))
        self.budget.set_limit("c1", Money(1000, "RUB"), period)
        tx1 = Transaction("t1", Money(600, "RUB"), TransactionType.EXPENSE,
                          "c1", "m1", date(2026, 4, 5), "Покупка 1")
        self.budget.add_transaction(tx1)  # OK
        tx2 = Transaction("t2", Money(500, "RUB"), TransactionType.EXPENSE,
                          "c1", "m1", date(2026, 4, 10), "Покупка 2")
        with self.assertRaises(LimitExceededException):
            self.budget.add_transaction(tx2)

    def test_cannot_add_transaction_with_invalid_member(self):
        tx = Transaction("t2", Money(100, "RUB"), TransactionType.EXPENSE,
                         "c1", "unknown", date(2026, 4, 1))
        with self.assertRaises(MemberNotFoundException):
            self.budget.add_transaction(tx)

    def test_archive_budget_prevents_changes(self):
        self.budget.archive()
        with self.assertRaises(Exception):  # BudgetAlreadyArchivedException
            self.budget.add_category(Category("c2", CategoryName("Транспорт")))

    def test_reporting_service(self):
        tx1 = Transaction("t1", Money(1000, "RUB"), TransactionType.INCOME,
                          "c1", "m1", date(2026, 4, 1), "ЗП")
        tx2 = Transaction("t2", Money(300, "RUB"), TransactionType.EXPENSE,
                          "c1", "m1", date(2026, 4, 2), "Обед")
        self.budget.add_transaction(tx1)
        self.budget.add_transaction(tx2)

        period = DateRange(date(2026, 4, 1), date(2026, 4, 30))
        report = BudgetReportingService.generate_report(self.budget, period)
        self.assertEqual(report["total_income"].amount, 1000)
        self.assertEqual(report["total_expense"].amount, 300)
        self.assertEqual(report["balance"].amount, 700)
        self.assertEqual(report["by_category"]["Продукты"]["expense"].amount, 300)

    def test_specifications(self):
        tx1 = Transaction("t1", Money(200, "RUB"), TransactionType.EXPENSE,
                          "c1", "m1", date(2026, 4, 1), "")
        tx2 = Transaction("t2", Money(150, "RUB"), TransactionType.EXPENSE,
                          "c1", "m1", date(2026, 4, 2), "")
        self.budget.add_transaction(tx1)
        self.budget.add_transaction(tx2)

        spec = ByCategoryIdSpecification("c1") & ByDateRangeSpecification(DateRange(date(2026,4,1), date(2026,4,1)))
        filtered = [t for t in self.budget.get_transactions() if spec.is_satisfied_by(t)]
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].id, "t1")

if __name__ == '__main__':
    unittest.main()