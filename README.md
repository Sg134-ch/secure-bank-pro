# Secure Online Banking System

A full-fledged, real-world Python Flask web application demonstrating core web application security principles. This project serves as an educational model for secure architecture, authentication, parameter manipulation prevention, and cryptography.

## Features

- **User Registration & Authentication**: Secure sign up and login processes using `Flask-Login` and `bcrypt` for password hashing.
- **Role-Based Access Control (RBAC)**: Distinct roles for standard users and administrators.
- **Fund Transfers**: Users can securely transfer funds to other registered users.
- **Admin Dashboard**: Administrators can view all system users and deposit initial funds into accounts.
- **Transaction History**: Every account modification is logged and visible on the user's dashboard.

## Security Principles Implemented

This application is built with security first:

1. **Architecture & Deployment**: Modular Blueprint architecture. Sensitive configurations (like `SECRET_KEY`) are loaded securely via environment variables. Ready for production WSGI deployment via `Procfile`.
2. **Input Validation**: `Flask-WTF` is used to enforce strict server-side validation on all forms (e.g., ensuring transfer amounts are positive floats, emails are valid, and passwords meet criteria).
3. **Authentication & Session Management**: Secure session cookies configured with `HttpOnly`, `SameSite=Lax`, and inactivity timeouts to prevent session hijacking.
4. **Cryptography**: Passwords are never stored in plaintext (hashed with `bcrypt`). Highly sensitive data (like the user's `account_number`) is symmetrically encrypted at rest in the database using the `cryptography` library (Fernet).
5. **Cross-Site Request Forgery (CSRF)**: Globally protected via `CSRFProtect`. Every POST form requires a valid, hidden CSRF token.
6. **Cross-Site Scripting (XSS)**: Prevented via Jinja2's default auto-escaping and strict Content-Security-Policies (CSP) in HTTP response headers.
7. **Parameter Manipulation Protection**: Business logic ensures users cannot transfer negative amounts, cannot transfer to themselves, and cannot bypass HTML frontend limits.
8. **Exception Management**: Custom error pages (404, 403, 500) ensure internal stack traces and server details are never leaked to end users.
9. **Auditing and Logging**: Critical events (successful logins, failed logins, transactions, unauthorized access attempts) are logged securely to an audit trail (`bank_audit.log`).

## Setup and Installation

### Prerequisites
- Python 3.8+
- `pip`

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/secure-banking-system.git
   cd secure-banking-system
   ```

2. **Create a virtual environment and install dependencies:**
   *(On Windows, you can simply run the provided `run.bat` script, or follow the manual steps below).*
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-random-secret-key
   ENCRYPTION_KEY=your-generated-fernet-key (e.g., 2cI63bH6aXpGk1_8gJ6fL4d_Z-QeYwT7kV1lA2hG5xE=)
   ```

4. **Initialize the Database:**
   ```bash
   python init_db.py
   ```
   *This creates the SQLite database and populates it with an Admin account and test users.*

5. **Run the Application:**
   ```bash
   python app.py
   ```
   Navigate to `http://127.0.0.1:5000` in your web browser.

## Deployment (Render / Heroku)

This application includes a `Procfile` and uses `gunicorn` for production deployment.

1. Create a new Web Service on Render and connect your GitHub repository.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `gunicorn app:app`
4. Make sure to add `SECRET_KEY` and `ENCRYPTION_KEY` into your Render Environment Variables!

## Default Test Accounts
If initialized via `init_db.py`:
- **Admin**: `admin@bank.com` / `admin123`
- **User**: `john@example.com` / `password123`

---
*Disclaimer: This is an educational project demonstrating security principles. In a real-world scenario, you would use a production database like PostgreSQL and a robust Key Management Service (KMS) for encryption keys.*
