from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Stage2Production:
    id: int
    order_id: int
    station: str
    started_at: str
    completed_at: str | None
    notes: str | None


SCHEMA = """
CREATE TABLE IF NOT EXISTS stage2_production (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    station TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    notes TEXT,
    FOREIGN KEY(order_id) REFERENCES orders(id)
);
"""


def create_table(conn: sqlite3.Connection) -> None:
    conn.execute(SCHEMA)
    conn.commit()


def insert(conn: sqlite3.Connection, *, order_id: int, station: str, started_at: str, completed_at: str | None, notes: str | None) -> int:
    cursor = conn.execute(
        """
        INSERT INTO stage2_production (order_id, station, started_at, completed_at, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (order_id, station, started_at, completed_at, notes),
    )
    conn.commit()
    return int(cursor.lastrowid)


def fetch_all(conn: sqlite3.Connection) -> Iterable[Stage2Production]:
    cursor = conn.execute(
        """
        SELECT id, order_id, station, started_at, completed_at, notes
        FROM stage2_production
        ORDER BY started_at DESC, id DESC
        """
    )
    rows = cursor.fetchall()
    return [Stage2Production(*row) for row in rows]
