# Almabase SDE Intern — Global Phone Directory (Django REST API)

**Project:** Global Phone Directory API (Almabase SDE Intern Hiring Assignment)  
**Author / Repo:** prasannaedu — https://github.com/prasannaedu/Hiring-Assignment  
**Status:** Part 1 complete (Contacts, Search, Auth). Part 2 (Interaction Dashboard) implemented or in-progress per assignment notes.

---

## Overview

This repository implements a Django REST Framework backend for a global phone directory system.  
It supports user authentication (JWT), contact management, spam reporting, search (partial/fuzzy), and an interaction dashboard to track calls/messages/spam reports.

Features:
- User signup/login with JWT authentication
- Per-user contact creation (duplicate prevention)
- Spam reporting for any phone number (prevent duplicate reports by the same user)
- Search by name or phone with deduplication and pagination
- Contact detail endpoint
- Interaction endpoints (recent interactions, top contacts, spam aggregates) — implemented in the Interaction Dashboard module

This README was generated from the attached assignment notes and test logs included with the project. fileciteturn0file0

---

## Tech stack

- Python 3.13.x  
- Django 5.0.6  
- Django REST Framework (DRF)  
- SQLite (development; swap to PostgreSQL for production)  
- JWT for authentication  
- `fuzzywuzzy` (or `rapidfuzz`) for fuzzy search  
- Git for version control

---

## Project structure (high level)

```
.
├─ app/                 # Django app (models, serializers, views)
├─ manage.py
├─ requirements.txt
├─ db.sqlite3
├─ README.md
└─ .gitignore
```

Key directories inside `app/`:
- `models/` (User, Contact, Interaction/ScamRecord)
- `serializers/` (input/output serializers)
- `api/viewsets/` (viewsets & endpoints)
- `api/router/` (URL routing)
- `migrations/`

---

## Quickstart (development)

Clone the repo:

```bash
git clone https://github.com/prasannaedu/Hiring-Assignment.git
cd Hiring-Assignment
```

Create & activate virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

(Optional) Populate with test data:

```bash
python manage.py populate
```

Run the server:

```bash
python manage.py runserver
```

API base: `http://127.0.0.1:8000/`

---

## Configuration notes

- For development the project uses SQLite. For production, update `DATABASES` in `settings.py` to use PostgreSQL and set proper credentials.
- Ensure `SECRET_KEY`, `ALLOWED_HOSTS`, and JWT settings are configured via environment variables in production.
- Consider replacing `fuzzywuzzy` with `rapidfuzz` for speed and licensing.

---

## API Reference (core endpoints)

> All endpoints require JWT authentication (send `Authorization: Bearer <access_token>`), unless noted.

### Authentication
- `POST /api/user/signup`  
  Body: `{"first_name","last_name","phone_number","password","email"}`  
  Response: user object + `access_token`, `refresh_token`.

- `POST /api/user/login`  
  Body: `{"phone_number","password"}`  
  Response: user object + tokens. Auto-creates user if phone not found (per assignment logic).

### Contacts
- `POST /api/contact/`  
  Create contact for authenticated user.  
  Body: `{"first_name","last_name","phone_number"}`  
  Error on duplicate per-user contact.

### Spam reporting
- `POST /api/spam`  
  Report any phone number as spam.  
  Body: `{"phone_number","description"}`  
  Duplicate reports by same reporter are prevented.

### Search
- `GET /api/search/?q=<query>`  
  Search by name (partial/fuzzy) or phone (exact). Returns paginated, de-duplicated results with fields: `id`, `name`, `is_registered`, `spammed_by_count`, `phone_number`.

- `GET /api/search/detail/<uuid:id>`  
  Get full details for a contact/user by UUID.

### Interactions (Interaction Dashboard)
- `POST /api/interactions/`  
  Create an interaction (`call`, `message`, `spam`) with metadata.

- `GET /api/interactions/recent`  
  Recent interactions (paginated). Optional `?type=message` filter.

- `GET /api/interactions/top`  
  Top contacts by interaction frequency.

- `POST /api/interactions/spam-reports`  
  Report spam via interaction (by contact id or phone).

- `GET /api/interactions/spam-reports`  
  Aggregated spam reports (paginated). Optional filters `?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`.

---

## Example cURL tests (Windows-friendly)

> Replace `YOUR_ACCESS_TOKEN` with the `access_token` from login response.

Login (obtain token):
```cmd
curl -X POST "http://127.0.0.1:8000/api/user/login" -H "Content-Type: application/json" -d "{"phone_number": "6300453865", "password": "63004538pk"}"
```

Create contact:
```cmd
curl -X POST "http://127.0.0.1:8000/api/contact" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{"first_name": "Alice", "last_name": "Smith", "phone_number": "9876543212"}"
```

Report spam:
```cmd
curl -X POST "http://127.0.0.1:8000/api/spam" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{"phone_number": "9876543211", "description": "Spam call"}"
```

Search by name:
```cmd
curl -X GET "http://127.0.0.1:8000/api/search/?q=Jane" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Get contact detail:
```cmd
curl -X GET "http://127.0.0.1:8000/api/search/detail/5482c191-6cb4-4a64-8c14-69600caf19e2" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Interactions (create message):
```cmd
curl -X POST "http://127.0.0.1:8000/api/interactions/" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{"receiver_contact_id":"5482c191-6cb4-4a64-8c14-69600caf19e2","type":"message","metadata":{"content":"Hey!"}}"
```

---

## Testing

- The APIs were tested locally using `curl` on Windows and returned expected JSON responses (status codes, body). Test cases and sample logs are included in the project notes. fileciteturn0file0

---

## Evaluation & Next Steps

**What's complete**
- Authentication (signup/login with JWT)
- Contact creation and duplication prevention
- Spam reporting with per-user duplicate prevention
- Search (basic partial search and detail endpoint)
- Interaction APIs scaffolded or implemented (see project notes)

**Recommended improvements**
1. Improve fuzzy-search ranking (use `rapidfuzz` and add relevance scoring).  
2. Normalize phone numbers (handle country codes consistently).  
3. Add unit tests and CI (pytest + GitHub Actions).  
4. Swap SQLite → PostgreSQL for production deployments.  
5. Optionally add a frontend dashboard (Chart.js / React) to visualize interactions.

---

## Commit & PR guidance

Suggested commit message for final push:
```
✨ Added Interaction Dashboard APIs (recent interactions, top contacts, spam reports)
```

Suggested PR description: include summary of features implemented, testing steps, and link to running demo or screenshot (if available). Example PR created: https://github.com/prasannaedu/Hiring-Assignment/pull/1

---

## License
Add an appropriate license (e.g., MIT) in `LICENSE` if you'd like the repository public.

---

If you want, I can:
- Add/format this README directly into your repo (provide exact `git` commands).  
- Produce a shorter `README-short.md` for GitHub PR summary.  
- Create a Markdown `CHANGELOG.md` with the commits listed in your logs.

Download the generated README below:
