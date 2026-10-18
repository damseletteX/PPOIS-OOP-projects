"""Domain classes for the transport company. Standard library only."""
from typing import Optional

class Invoice:
    """Domain entity: Invoice. Доменная сущность транспортной компании."""
    def __init__(self, invoice_number: str, issued_at: str, due_date: str, total_amount: float, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.invoice_number = invoice_number
        self.issued_at = issued_at
        self.due_date = due_date
        self.total_amount = total_amount
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def calculate_amount_due(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Вычитает зачтённые платежи и кредит-ноты из суммы счёта; результат не может быть отрицательным.'

    def mark_as_paid(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Разрешает переход в «оплачен» только при полном погашении остатка.'

    def issue_credit_note(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Создаёт кредит-ноту на допустимую сумму и связывает её с исходным счётом.'

class Payment:
    """Domain entity: Payment. Доменная сущность транспортной компании."""
    def __init__(self, payment_reference: str, amount: float, payment_method: str, received_at: str, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.payment_reference = payment_reference
        self.amount = amount
        self.payment_method = payment_method
        self.received_at = received_at
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def allocate_payment_to_invoice(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет валюту/сумму/состояние счёта, распределяет платёж и обновляет остаток.'

    def refund_payment(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет доступную к возврату сумму и помечает возврат; повторный возврат запрещён.'

class RateCard:
    """Domain entity: RateCard. Доменная сущность транспортной компании."""
    def __init__(self, rate_card_code: str, base_rate: float, per_km_rate: float, effective_from: str, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.rate_card_code = rate_card_code
        self.base_rate = base_rate
        self.per_km_rate = per_km_rate
        self.effective_from = effective_from
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def quote_transport_price(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Рассчитывает базовый тариф + расстояние × ставку за километр.'

    def apply_surcharge(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Добавляет надбавку по заданной причине и возвращает обновлённую цену.'

class Discount:
    """Domain entity: Discount. Доменная сущность транспортной компании."""
    def __init__(self, discount_code: str, percentage: float, valid_from: str, valid_until: str, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.discount_code = discount_code
        self.percentage = percentage
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def check_discount_eligibility(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет срок действия скидки и допустимость её применения к клиенту/заказу.'

    def apply_discount(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Уменьшает стоимость на процент скидки в допустимом диапазоне 0–100%.'

class Expense:
    """Domain entity: Expense. Доменная сущность транспортной компании."""
    def __init__(self, expense_id: str, category: str, amount: float, incurred_at: str, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.expense_id = expense_id
        self.category = category
        self.amount = amount
        self.incurred_at = incurred_at
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def submit_for_approval(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет сумму и обязательные подтверждающие сведения, затем переводит расход в ожидание согласования.'

    def allocate_expense_to_trip(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Связывает расход с рейсом и запрещает распределение на несуществующий/закрытый рейс.'

class PayrollRecord:
    """Domain entity: PayrollRecord. Доменная сущность транспортной компании."""
    def __init__(self, payroll_id: str, period_start: str, period_end: str, gross_pay: float, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.payroll_id = payroll_id
        self.period_start = period_start
        self.period_end = period_end
        self.gross_pay = gross_pay
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def calculate_net_pay(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Рассчитывает чистую выплату из начисленной суммы с учётом удержаний.'

    def finalise_payroll(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет период и расчёт, фиксирует ведомость и запрещает повторное закрытие.'

class FuelBudget:
    """Domain entity: FuelBudget. Доменная сущность транспортной компании."""
    def __init__(self, budget_id: str, period: str, allocated_amount: float, spent_amount: float, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.budget_id = budget_id
        self.period = period
        self.allocated_amount = allocated_amount
        self.spent_amount = spent_amount
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def calculate_budget_variance(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Возвращает разницу между бюджетом и фактическими расходами.'

    def forecast_fuel_spend(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Оценивает расходы на топливо по текущему темпу расходования бюджета.'

class InsurancePolicy:
    """Domain entity: InsurancePolicy. Доменная сущность транспортной компании."""
    def __init__(self, policy_number: str, provider: str, coverage_limit: float, expires_at: str, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.policy_number = policy_number
        self.provider = provider
        self.coverage_limit = coverage_limit
        self.expires_at = expires_at
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def check_claim_coverage(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет тип и сумму претензии относительно покрытия страхового полиса.'

    def renew_policy(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет данные страховщика и устанавливает новый период действия полиса.'

class Claim:
    """Domain entity: Claim. Доменная сущность транспортной компании."""
    def __init__(self, claim_number: str, claim_type: str, claim_amount: float, claim_status: str, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.claim_number = claim_number
        self.claim_type = claim_type
        self.claim_amount = claim_amount
        self.claim_status = claim_status
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def submit_claim_evidence(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет комплект доказательств и переводит претензию на рассмотрение.'

    def settle_claim(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Проверяет статус претензии и допустимую выплату, после чего закрывает её.'

class FinancialReport:
    """Domain entity: FinancialReport. Доменная сущность транспортной компании."""
    def __init__(self, report_id: str, period: str, revenue: float, operating_cost: float, customer_id: Optional[str] = None, related_document_id: Optional[str] = None):
        self.report_id = report_id
        self.period = period
        self.revenue = revenue
        self.operating_cost = operating_cost
        self.customer_id = customer_id
        self.related_document_id = related_document_id

    def calculate_profit_margin(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Рассчитывает (выручка − операционные затраты) / выручка × 100%; при нулевой выручке возвращает 0.'

    def export_financial_summary(self) -> None:
        """Выполняет доменную операцию класса."""
        return 'Формирует машиночитаемую сводку выручки, затрат, прибыли и маржинальности.'

