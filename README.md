# Mini DoorDash Backend (Python/FastAPI)

A modern, fast, and scalable backend for the Mini DoorDash application built with FastAPI and PostgreSQL.

## 🚀 Features

- **FastAPI Framework** - High-performance, modern Python web framework
- **PostgreSQL Database** - Robust relational database with Supabase
- **JWT Authentication** - Secure token-based authentication
- **SQLAlchemy ORM** - Powerful database abstraction layer
- **Pydantic Validation** - Automatic request/response validation
- **CORS Support** - Cross-origin resource sharing enabled
- **Auto-generated API Docs** - Interactive API documentation
- **Railway Deployment Ready** - Easy deployment configuration

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **Deployment**: Railway

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
```bash
cp env.example .env
# Edit .env with your database credentials
```

### 3. Run the Application
```bash
python main.py
```

The API will be available at `http://localhost:8080`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API Docs**: `http://localhost:8080/docs`
- **ReDoc Documentation**: `http://localhost:8080/redoc`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /users/register`
2. **Login**: `POST /users/login`
3. **Use Token**: Include `Authorization: Bearer <token>` in headers

## 🚀 Deployment on Railway

This project is configured for easy deployment on Railway with automatic health checks and scaling.
