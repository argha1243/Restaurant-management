# Restaurant Management

This Flask app converts the original spreadsheet process into a web interface. Each sheet is mapped to its own Python module and database table for Orders, Purchases, Stage 2 Production, and Losses.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app

```bash
export FLASK_APP=app:create_app
flask run
```

The application uses a local SQLite database (`restaurant.db`). Adjust the `RESTAURANT_DB` environment variable to change the location.
