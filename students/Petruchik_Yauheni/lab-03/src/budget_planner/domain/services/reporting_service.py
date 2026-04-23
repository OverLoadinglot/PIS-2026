from typing import List, Dict
from datetime import date
from ..models.entities import FamilyBudget, Transaction
from ..models.value_objects import Money, DateRange, TransactionType
from ..models.specifications import Specification, ByDateRangeSpecification, ByTypeSpecification

class BudgetReportingService:
    @staticmethod
    def generate_report(budget: FamilyBudget, period: DateRange) -> Dict:
        """
        Возвращает структурированный отчёт:
        {
            "total_income": Money,
            "total_expense": Money,
            "balance": Money,
            "by_category": {category_name: {"expense": Money, "income": Money}},
            "by_member": {member_name: {"expense": Money, "income": Money}}
        }
        """
        transactions = budget.get_transactions()
        # фильтруем по периоду
        period_spec = ByDateRangeSpecification(period)
        filtered = [t for t in transactions if period_spec.is_satisfied_by(t)]

        total_income = Money(0, "RUB")
        total_expense = Money(0, "RUB")
        by_category = {}
        by_member = {}

        # вспомогательные маппинги
        cat_name_by_id = {cat.id: cat.name.value for cat in budget.get_categories()}
        member_name_by_id = {mem.id: mem.name.value for mem in budget.get_members()}

        for t in filtered:
            amount = t.amount
            cat_name = cat_name_by_id.get(t.category_id, "Unknown")
            member_name = member_name_by_id.get(t.member_id, "Unknown")

            if t.type == TransactionType.INCOME:
                total_income += amount
                cat_key = cat_name
                mem_key = member_name
                # Для категории и члена храним доходы отдельно
                by_category.setdefault(cat_key, {"income": Money(0, "RUB"), "expense": Money(0, "RUB")})["income"] += amount
                by_member.setdefault(mem_key, {"income": Money(0, "RUB"), "expense": Money(0, "RUB")})["income"] += amount
            else:
                total_expense += amount
                by_category.setdefault(cat_name, {"income": Money(0, "RUB"), "expense": Money(0, "RUB")})["expense"] += amount
                by_member.setdefault(member_name, {"income": Money(0, "RUB"), "expense": Money(0, "RUB")})["expense"] += amount

        balance = total_income - total_expense  # Money supports subtraction

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "by_category": by_category,
            "by_member": by_member,
        }