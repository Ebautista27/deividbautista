# Click Application

This is a simple monolithic web application built with Flask. It demonstrates a basic architecture including:

- Web interface with buttons
- SQLite database for persistence
- Business logic to store clicks, reset counts, and keep a reset history

## Setup

1. Install dependencies (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

The application will start on `http://localhost:5000`. Open this address in your web browser.

## Usage

- **Click me!** button increases the click counter and stores each click in the database.
- **Reset** button saves the current click count to the history and resets the counter.
- **View history** link shows how many clicks were recorded at each reset.

## Files

- `app.py` – main Flask application.
- `requirements.txt` – Python dependencies.
- `database.db` – SQLite database file created at runtime.

