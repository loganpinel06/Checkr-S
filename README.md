# <img src="app/static/images/banner.svg" width="100%" height="350px">

# About the App
Checkr S is a secure and intuitive web application that is designed to allow users to track monthly transactions digitally with ease.
This project aims to provide more than just a basic CRUD application that works but to ensure that user information is safe and secure.
Built primarily with Flask, the app features strong authentication, session security, CSRF protection, rate limiting, and a clean user interface.

# Tech Stack
- **Core Technologies:**
    - Flask
    - HTML
    - SCSS
- **Flask Extensions:**
    - Flask-SQLAlchemy (ORM to create database models written in python)
    - Flask-WTF (create secure HTML form with CSRF protection)
    - Flask-Login (handle authentication logic)
    - Flask-Limiter (handle rate limiting to prevent brute force attacks)
- **Databases:**
    - PostgreSQL hosted on Supabase (stores all user, transaction, and balance data)
    - Redis hosted on Upstash (used for storing rate limiting data which is constantly being updated)

# Run the Project Locally
```
#mac
python3 -m venv env
#windows
python -m venv env
```

