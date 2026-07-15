# TypeHints
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Protocol
from uuid import UUID, uuid4


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class OrderItem:
    product_id: UUID
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("unit_price cannot be negative")

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass(slots=True)
class Order:
    items: list[OrderItem]
    id: UUID = field(default_factory=uuid4)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    def mark_as_paid(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"cannot pay an order in status {self.status}")
        self.status = OrderStatus.PAID


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def get_by_id(self, order_id: UUID) -> Order | None: ...


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[UUID, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def get_by_id(self, order_id: UUID) -> Order | None:
        return self._orders.get(order_id)