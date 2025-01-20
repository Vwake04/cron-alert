# Cron Alert

A Python-based monitoring system that checks for upgrades and sends notifications on a scheduled basis.

## Features

- Scheduled monitoring at configurable times
- Database-backed storage using SQLModel (supports both PostgreSQL and SQLite)
- Email notifications
- Configurable logging
- Docker support

## Prerequisites

- Python 3.10+
- PostgreSQL (for production) or SQLite (for local development)
- Docker (optional)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cron-alert.git
cd cron-alert
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Create a `.env` file with the following variables:

```env
# Database (Choose one)
# For PostgreSQL:
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# For SQLite:
DATABASE_URL=sqlite:///./cron_alert.db

# Email Configuration
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
FROM_EMAIL=sender@example.com
TO_EMAIL=recipient@example.com

# Schedule Configuration (optional)
SCHEDULE_TIMES=09:00,21:00  # Default is "09:00,21:00"
```

### Database Setup

#### Using SQLite (Recommended for local development)

SQLite is a lightweight, file-based database that requires no additional setup. Just specify the SQLite URL in your `.env` file:

```env
DATABASE_URL=sqlite:///./cron_alert.db
```

The database file will be automatically created when you first run the application.

#### Using PostgreSQL (Recommended for production)

For PostgreSQL, ensure the database server is running and create a database:

```bash
createdb cron_alert  # If you have PostgreSQL CLI tools installed
```

Then configure the PostgreSQL URL in your `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/cron_alert
```

## Usage

### Running Locally

```bash
python app.py
```

### Running with Docker

1. Build the container:

```bash
docker-compose build
```

2. Start the services:

```bash
docker-compose up -d
```

## Project Structure

```
cron-alert/
├── app.py           # Main application entry point
├── db.py            # Database configuration and utilities
├── notify.py        # Notification handling
├── logger.py        # Logging configuration
├── models/          # Database models
├── tests/           # Test files
└── docker-compose.yml
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Logging

Logs are written to `logs/app.log` by default. The logging level and format can be configured in `logger.py`.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
