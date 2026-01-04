# Pastebin-Lite

A minimal pastebin application built with Django REST Framework and MySQL.

## Features
- Create text pastes with optional TTL and view limits
- Share pastes via unique URLs
- Automatic expiration based on time or view count

## Persistence Layer
**MySQL Database**: Provides persistent storage with ACID compliance for handling concurrent view counting and TTL expiration logic.

## Local Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd pastebin-lite
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create MySQL database:
```bash
mysql -u root -p
CREATE DATABASE pastebin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. Configure environment variables (create `.env`):
```
DB_NAME=pastebin_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `GET /api/healthz` - Health check
- `POST /api/pastes` - Create a paste
- `GET /api/pastes/:id` - Fetch paste (API)

## Design Decisions

1. **Atomic View Counting**: Used Django's `F()` expressions to prevent race conditions
2. **UUID Primary Keys**: Ensures unpredictable, unique paste IDs
3. **Timezone-aware timestamps**: Proper handling of TTL expiration across timezones
4. **Separation of API and HTML views**: API views count towards view limit, HTML views don't
5. **TEST_MODE support**: Deterministic time testing via `x-test-now-ms` header

## Deployment

Suitable for deployment on:
- Railway
- Render
- PythonAnywhere
- Any VPS with MySQL support
