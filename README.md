# Job Portal Backend API

A secure RESTful backend API for a Job Portal system built with **FastAPI**, **MySQL**, **SQLAlchemy**, **Alembic**, and **JWT Authentication**.

The system supports two user roles:

- **Candidate**: can browse jobs and apply for jobs.
- **Employer**: can create, update, and delete their own jobs and manage applications.

The project implements authentication, authorization, job management, job applications, and role-based access control.

---

## 📌 Project Overview

The Job Portal Backend provides APIs for managing users, job postings, and job applications.

The main goals of the project are:

- Secure user authentication
- JWT-based authorization
- Role-based access control
- Job CRUD operations
- Candidate job applications
- Employer application management
- MySQL database integration
- Database migrations using Alembic
- Interactive API documentation using Swagger UI

---

# 🚀 Features

## Authentication

The API provides:

- User registration
- User login
- Password hashing
- JWT access tokens
- Protected endpoints
- Current-user information

## Authorization

The system supports two roles:

### Candidate

Candidates can:

- View available jobs
- View a specific job
- Apply for jobs
- View their applications

Candidates cannot:

- Create jobs
- Update jobs
- Delete jobs
- Accept or reject applications

### Employer

Employers can:

- Create jobs
- View jobs
- Update their own jobs
- Delete their own jobs
- View applications for their own jobs
- Accept or reject applications

Employers cannot apply for jobs.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Backend web framework |
| MySQL | Relational database |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| Pydantic | Data validation |
| JWT | Authentication |
| Passlib / bcrypt | Password hashing |
| PyMySQL | MySQL database driver |
| Swagger UI | API testing/documentation |

---

# 📁 Project Structure

```text
job-portal-backend/
│
├── app/
│   │
│   ├── core/
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── base.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── job.py
│   │   └── application.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── job.py
│   │   └── application.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   └── applications.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .env
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

The authentication flow is:

Register
   ↓
Password hashed
   ↓
User stored in MySQL
   ↓
Login
   ↓
Credentials verified
   ↓
JWT token generated
   ↓
Token sent in Authorization header
   ↓
Protected endpoint

The token is used to identify the currently authenticated user.

👥 Role-Based Access Control

The API checks the user's role before allowing access to protected operations.

Candidate permissions
```text
GET /jobs/
GET /jobs/{job_id}
POST /jobs/{job_id}/apply
GET /applications/
```
Employer permissions
```text
POST /jobs/
GET /jobs/
GET /jobs/{job_id}
PUT /jobs/{job_id}
DELETE /jobs/{job_id}
GET /applications/
PATCH /applications/{application_id}/status
```

<img width="960" height="510" alt="image" src="https://github.com/user-attachments/assets/cb072899-0bef-4ea2-a02b-535796f55bb3" />

 
 
## Deployment

### 1. Create Online MySQL Database

We used **Aiven MySQL** as the cloud database so the deployed FastAPI application can access the database online.

The database connection uses:

```env
DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:PORT/job_portal
````

### 2. Configure Environment Variables

The application reads the database and security settings from environment variables:

```env
DATABASE_URL=...
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The `.env` file is not uploaded to GitHub.

### 3. Run Database Migrations

After connecting the project to the online database:

```bash
alembic upgrade head
```

This creates the required tables:

```text
users
jobs
applications
```

### 4. Push Project to GitHub

```bash
git add .
git commit -m "Prepare project for deployment"
git push origin main
```

### 5. Create Render Web Service

On Render:

```text
New → Web Service
```

Connect the GitHub repository and select the `main` branch.

### 6. Configure Render

**Build Command:**

```bash
pip install -r requirements.txt
```

**Start Command:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 7. Add Environment Variables

In Render → Environment Variables, add:

```text
DATABASE_URL
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

### 8. Deploy

Click **Deploy Web Service**.

Render will:

```text
GitHub
   ↓
Install dependencies
   ↓
Start FastAPI
   ↓
Connect to Aiven MySQL
   ↓
Application online
```

### 9. Access the API

After deployment, Render provides a public URL:

```text
https://job-portal-backend.onrender.com
```

Swagger documentation:

```text
https://job-portal-backend.onrender.com/docs
```



