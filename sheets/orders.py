from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Order:
    id: int
    customer_name: str
    item: str
    quantity: int
    status: str
    order_date: str


SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT NOT NULL,
    order_date TEXT NOT NULL
);
"""


def create_table(conn: sqlite3.Connection) -> None:
    conn.execute(SCHEMA)
    conn.commit()


def insert(conn: sqlite3.Connection, *, customer_name: str, item: str, quantity: int, status: str, order_date: str) -> int:
    cursor = conn.execute(
        """
        INSERT INTO orders (customer_name, item, quantity, status, order_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (customer_name, item, quantity, status, order_date),
    )
    conn.commit()
    return int(cursor.lastrowid)


def fetch_all(conn: sqlite3.Connection) -> Iterable[Order]:
    cursor = conn.execute(
        """
        SELECT id, customer_name, item, quantity, status, order_date
        FROM orders
        ORDER BY order_date DESC, id DESC
        """
    )
    rows = cursor.fetchall()
    return [Order(*row) for row in rows]
