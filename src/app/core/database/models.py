from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AuthUser:
    id: int
    login: str
    password_hash: str
    role: str
    client_id: Optional[int] = None


@dataclass
class Client:
    id: int
    first_name: str
    last_name: str
    passport_number: str
    phone_number: Optional[str]
    email: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class Account:
    id: int
    client_id: int
    account_number: str
    account_type: str
    balance: float
    currency: str
    opened_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class Transaction:
    id: int
    from_account_id: Optional[int]
    to_account_id: int
    amount: float
    transaction_type: str
    description: Optional[str]
    transaction_date: datetime
    status: str
    created_at: datetime
