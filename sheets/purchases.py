from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Purchase:
    id: int
    supplier: str
    item: str
    quantity: int
    unit_cost: float
    purchase_date: str


SCHEMA = """
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    purchase_date TEXT NOT NULL
);
"""


def create_table(conn: sqlite3.Connection) -> None:
    conn.execute(SCHEMA)
    conn.commit()


def insert(conn: sqlite3.Connection, *, supplier: str, item: str, quantity: int, unit_cost: float, purchase_date: str) -> int:
    cursor = conn.execute(
        """
        INSERT INTO purchases (supplier, item, quantity, unit_cost, purchase_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (supplier, item, quantity, unit_cost, purchase_date),
    )
    conn.commit()
    return int(cursor.lastrowid)


def fetch_all(conn: sqlite3.Connection) -> Iterable[Purchase]:
    cursor = conn.execute(
        """
        SELECT id, supplier, item, quantity, unit_cost, purchase_date
        FROM purchases
        ORDER BY purchase_date DESC, id DESC
        """
    )
    rows = cursor.fetchall()
    return [Purchase(*row) for row in rows]
