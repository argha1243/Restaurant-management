from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Loss:
    id: int
    item: str
    quantity: int
    loss_date: str
    reason: str


SCHEMA = """
CREATE TABLE IF NOT EXISTS losses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    loss_date TEXT NOT NULL,
    reason TEXT NOT NULL
);
"""


def create_table(conn: sqlite3.Connection) -> None:
    conn.execute(SCHEMA)
    conn.commit()


def insert(conn: sqlite3.Connection, *, item: str, quantity: int, loss_date: str, reason: str) -> int:
    cursor = conn.execute(
        """
        INSERT INTO losses (item, quantity, loss_date, reason)
        VALUES (?, ?, ?, ?)
        """,
        (item, quantity, loss_date, reason),
    )
    conn.commit()
    return int(cursor.lastrowid)


def fetch_all(conn: sqlite3.Connection) -> Iterable[Loss]:
    cursor = conn.execute(
        """
        SELECT id, item, quantity, loss_date, reason
        FROM losses
        ORDER BY loss_date DESC, id DESC
        """
    )
    rows = cursor.fetchall()
    return [Loss(*row) for row in rows]
