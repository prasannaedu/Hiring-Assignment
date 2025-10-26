# Almabase SDE Intern — Global Phone Directory (Django REST API)

**Project:** Global Phone Directory API (Almabase SDE Intern Hiring Assignment)  
**Author:** [prasannaedu](https://github.com/prasannaedu)  
**Repository:** [Hiring-Assignment](https://github.com/prasannaedu/Hiring-Assignment)  
**Status:**  Part 1 (Contacts, Search, Auth) completed | 🚀 Part 2 (Interaction Dashboard) implemented

---

##  Overview

This project implements a **Django REST Framework backend** for a global phone directory system.  
It supports user authentication (JWT), contact management, spam reporting, search (partial/fuzzy), and an interaction dashboard to track calls, messages, and spam reports.

### ✨ Core Features

- Secure user signup and login with JWT authentication  
- Contact creation and management (duplicate prevention)  
- Spam reporting with user-based restriction  
- Search by name or phone (supports partial & fuzzy matches)  
- Detailed contact view API  
- Interaction Dashboard (recent interactions, top contacts, spam aggregates)

---

##  Tech Stack

- **Python:** 3.13.x  
- **Django:** 5.0.6  
- **Django REST Framework (DRF)**  
- **SQLite (development)** → PostgreSQL (for production)  
- **JWT** for user authentication  
- **fuzzywuzzy / rapidfuzz** for fuzzy search  
- **Git & GitHub** for version control

---

##  Project Structure

```
.
├─ app/                 # Main Django app (models, serializers, views, routers)
├─ manage.py
├─ requirements.txt
├─ db.sqlite3
├─ README.md
└─ .gitignore
```

### Inside `app/`
- `models/` → User, Contact, Interaction models  
- `serializers/` → Input & output serializers  
- `api/viewsets/` → API views  
- `api/router/` → URL routing  
- `migrations/` → Django migrations

---

##  Setup Instructions

### Clone the repository
```bash
git clone https://github.com/prasannaedu/Hiring-Assignment.git
cd Hiring-Assignment
```

### Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run migrations
```bash
python manage.py migrate
```

### (Optional) Add sample data
```bash
python manage.py populate
```

### Start the server
```bash
python manage.py runserver
```

> API Base URL: **http://127.0.0.1:8000/**

---

##  Configuration Notes

- Default DB: SQLite (change to PostgreSQL for production)
- Keep `SECRET_KEY`, `DEBUG`, and JWT configs in environment variables
- Replace `fuzzywuzzy` with `rapidfuzz` for better performance and licensing

---

##  API Reference

> All endpoints (except signup/login) require JWT authentication.  
> Send token as: `Authorization: Bearer <access_token>`

###  Authentication
- **POST /api/user/signup** → Register a new user  
- **POST /api/user/login** → Login and get JWT tokens  

###  Contacts
- **POST /api/contact/** → Create a new contact (prevents duplicates)

###  Spam Reporting
- **POST /api/spam** → Report a number as spam  

###  Search
- **GET /api/search/?q=<query>** → Search by name/phone  
- **GET /api/search/detail/<uuid:id>** → Detailed contact info  

###  Interactions (Dashboard)
- **POST /api/interactions/** → Log a call/message/spam  
- **GET /api/interactions/recent** → List recent interactions  
- **GET /api/interactions/top** → Top interacted contacts  
- **GET /api/interactions/spam-reports** → Aggregated spam data  
- **POST /api/interactions/spam-reports** → Add new spam report  

---

##  Example cURL Commands

> Replace `YOUR_ACCESS_TOKEN` with your JWT access token.

### Login
```cmd
curl -X POST "http://127.0.0.1:8000/api/user/login" -H "Content-Type: application/json" -d "{"phone_number": "6300453865", "password": "63004538pk"}"
```

### Create Contact
```cmd
curl -X POST "http://127.0.0.1:8000/api/contact" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{"first_name": "Alice", "last_name": "Smith", "phone_number": "9876543212"}"
```

### Report Spam
```cmd
curl -X POST "http://127.0.0.1:8000/api/spam" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{"phone_number": "9876543211", "description": "Spam call"}"
```

### Search Contact
```cmd
curl -X GET "http://127.0.0.1:8000/api/search/?q=Jane" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Log Interaction
```cmd
curl -X POST "http://127.0.0.1:8000/api/interactions/" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{"receiver_contact_id":"5482c191-6cb4-4a64-8c14-69600caf19e2","type":"message","metadata":{"content":"Hey!"}}"
```

---

##  Testing

All APIs were tested locally using `curl` on Windows.  
Each endpoint returned expected responses (status codes + JSON).  
Logs and screenshots are included in the project submission.

---

##  Completed Functionality

- JWT Authentication (Signup/Login)  
- Contact creation and duplication prevention  
- Spam reporting (user-based restriction)  
- Search API (partial/fuzzy)  
- Interaction Dashboard (recent, top, spam reports)  

---

##  Next Steps

- Add relevance scoring to fuzzy search  
- Normalize phone numbers with country codes  
- Add unit tests using `pytest`  
- Integrate GitHub Actions for CI/CD  
- Deploy using PostgreSQL + Docker  

---

**Suggested commit message:**
```
✨ Added Interaction Dashboard APIs (recent interactions, top contacts, spam reports)
```

**Pull Request Link:**  
[View Pull Requests](https://github.com/prasannaedu/Hiring-Assignment/pulls)

---

Built with ❤️ using **Django REST Framework**
