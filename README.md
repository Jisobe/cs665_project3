# Healthcare Charting System

This application provides a charting system for US base healthcare facilities

## Table of Contents

- [Healthcare Charting System](#healthcare-charting-system)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Database Setup](#database-setup)
    - [Automatic setup](#automatic-setup)
    - [Foreign key enforcement](#foreign-key-enforcement)
  - [Seeding Sample Data](#seeding-sample-data)
    - [Run the seeder](#run-the-seeder)
    - [Reset and reseed](#reset-and-reseed)
  - [Running the App](#running-the-app)
    - [Development server](#development-server)
    - [Using a `.env` file (optional)](#using-a-env-file-optional)

## Project Description

HealthChart is simple application for tracking patient visits, vitals, and diagnoses. It provides the following functionality:

- Add patients and providers
- Record visit information
- Record multiple vitals readings per visit
- Assign diagnoses to a patient with an associated ICD
- Dashboard to view aggregate data for the system

## Tech Stack

| Purpose | Technology |
| --- | --- |
| Language | Python 3.12+ |
| Web framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite (file-based, serverless) |
| Package manager | uv |
| Templating | Jinja2 |

## Installation

### Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - install it with (suggested):

```bash
pip install uv
```

### Steps

1. Clone the repository

    ```bash
    git clone https://github.com/Jisobe/cs665_project3.git
    cd cs665_project3
    ```

2. Create the virtual environment and install dependencies

    `uv` handles the virtual environment automatically:

    ```bash
    uv sync
    ```

## Database Setup

For easy of use, HealthChart uses SQLite so no database server installation is required. The database file is created automatically at `instance/health.db` the first time the app starts.

### Automatic setup

On startup, the database and tables are created automatically. `db.create_all()` in the app factory creates all tables according to the SQLAlchemy models.

### Foreign key enforcement

SQLite does not enforce foreign keys by default. HealthChart enables this on every connection automatically via a SQLAlchemy event listener in `app/__init__.py`:

```python
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
```

No additional action is required for this.

## Seeding Sample Data

For easy of use and convenience, HealthChart has a `flask seed` command that populates the database with sample data.

### Run the seeder

```bash
uv run flask --app main seed
```

Example output:

```
  ICD codes: 7 inserted, 0 skipped.
  Patients: 5 inserted, 0 skipped.
  Providers: 5 inserted, 0 skipped.
  Provider Specialties: 5 inserted, 0 skipped.
  Provider State Licenses: 5 inserted, 0 skipped.
  Visits: 7 inserted, 0 skipped.
  Vitals: 7 inserted, 0 skipped.
  Diagnoses: 7 inserted, 0 skipped.
✓ Database seeded successfully.
```

The seeder is idempotent - running it multiple times will skip rows that already exist rather than inserting duplicates.

### Reset and reseed

**WARNING** This will override an existing data in the database. Use with caution.

To wipe the database and start fresh:

```bash
uv run flask --app main seed --reset
```

## Running the App

### Development server

```bash
uv run flask --app main run --debug
```

The app will be available at http://127.0.0.1:5000 by default. To run the application on a custom port, use the following command

```bash
uv run flask --app main run --debug --port 5001
```

### Using a `.env` file (optional)

Create a `.env` file in the project root to avoid typing `--app main` each time:

```bash
# .env
FLASK_APP=main
FLASK_DEBUG=1
```

Then run simply:

```bash
uv run flask run
```
