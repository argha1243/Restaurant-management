from __future__ import annotations

import os
import sqlite3
from typing import Callable

from flask import Flask, flash, g, redirect, render_template, request, url_for

from sheets import losses, orders, purchases, stage2_production

DATABASE = os.environ.get("RESTAURANT_DB", os.path.join(os.path.dirname(__file__), "restaurant.db"))


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")

    @app.before_request
    def before_request() -> None:
        g.db = get_db()

    @app.teardown_appcontext
    def teardown(exception: BaseException | None) -> None:  # pragma: no cover - lifecycle hook
        db = g.pop("db", None)
        if db is not None:
            db.close()

    ensure_schema()

    register_routes(app)
    return app


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        connection = sqlite3.connect(DATABASE)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def ensure_schema() -> None:
    conn = sqlite3.connect(DATABASE)
    for creator in (
        orders.create_table,
        purchases.create_table,
        stage2_production.create_table,
        losses.create_table,
    ):
        creator(conn)
    conn.close()


def register_routes(app: Flask) -> None:
    @app.route("/")
    def index():
        return render_template("index.html")

    register_sheet_routes(
        app,
        name="orders",
        list_template="orders.html",
        insert_callback=orders.insert,
        fetch_callback=orders.fetch_all,
        form_fields=(
            "customer_name",
            "item",
            "quantity",
            "status",
            "order_date",
        ),
        converters={"quantity": lambda value: int(value) if value is not None else None},
    )

    register_sheet_routes(
        app,
        name="purchases",
        list_template="purchases.html",
        insert_callback=purchases.insert,
        fetch_callback=purchases.fetch_all,
        form_fields=(
            "supplier",
            "item",
            "quantity",
            "unit_cost",
            "purchase_date",
        ),
        converters={
            "quantity": lambda value: int(value) if value is not None else None,
            "unit_cost": lambda value: float(value) if value is not None else None,
        },
    )

    register_sheet_routes(
        app,
        name="stage2",
        list_template="stage2_production.html",
        insert_callback=stage2_production.insert,
        fetch_callback=stage2_production.fetch_all,
        form_fields=(
            "order_id",
            "station",
            "started_at",
            "completed_at",
            "notes",
        ),
        converters={"order_id": lambda value: int(value) if value is not None else None},
    )

    register_sheet_routes(
        app,
        name="losses",
        list_template="losses.html",
        insert_callback=losses.insert,
        fetch_callback=losses.fetch_all,
        form_fields=(
            "item",
            "quantity",
            "loss_date",
            "reason",
        ),
        converters={"quantity": lambda value: int(value) if value is not None else None},
    )


def register_sheet_routes(
    app: Flask,
    *,
    name: str,
    list_template: str,
    insert_callback: Callable[..., int],
    fetch_callback: Callable[[sqlite3.Connection], object],
    form_fields: tuple[str, ...],
    converters: dict[str, Callable[[str | None], object]] | None = None,
) -> None:
    list_endpoint = f"{name}_list"
    add_endpoint = f"{name}_add"

    @app.route(f"/{name}")
    def list_records():
        rows = fetch_callback(g.db)
        return render_template(list_template, rows=rows, name=name)

    list_records.__name__ = list_endpoint

    @app.route(f"/{name}/add", methods=["GET", "POST"])
    def add_record():
        if request.method == "POST":
            payload = {field: request.form.get(field, "").strip() or None for field in form_fields}
            if converters:
                for field, converter in converters.items():
                    payload[field] = converter(payload.get(field))
            try:
                insert_callback(g.db, **payload)
            except Exception as exc:  # pragma: no cover - defensive user input handling
                flash(f"Could not save record: {exc}", "error")
            else:
                flash("Saved successfully", "success")
                return redirect(url_for(list_endpoint))
        return render_template(f"{name}_form.html", name=name)

    add_record.__name__ = add_endpoint


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
