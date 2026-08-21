# Secure Online Banking System

[![Live Demo](https://img.shields.io/badge/Live_Demo-Click_Here-success?style=for-the-badge)](http://Shrutig.pythonanywhere.com)

**Live Demo URL:** [http://Shrutig.pythonanywhere.com](http://Shrutig.pythonanywhere.com)

A full-fledged, real-world Python Flask web application demonstrating core web application security principles. This project serves as an educational model for secure architecture, authentication, parameter manipulation prevention, and cryptography within an Indian banking context.

## Features

- **User Registration & Authentication**: Secure sign up and login processes using `Flask-Login` and `bcrypt` for password hashing.
- **Role-Based Access Control (RBAC)**: Distinct roles for standard users and administrators.
- **Fund Transfers**: Users can securely transfer funds (₹) to other registered users.
- **Utility Bill Payments**: Users can pay mock Indian billers (BESCOM, BWSSB, Jio Fiber, HDFC).
- **Secure Statements**: Users can download their complete transaction history as a secure CSV file.
- **Admin Dashboard**: Administrators can view all system users and deposit initial funds into accounts.
- **Transaction History**: Every account modification is logged and visible on the user's dashboard.

## Security Principles Implemented

This application is built with security first:

1. **Architecture & Deployment**: Modular Blueprint architecture. Sensitive configurations (like `SECRET_KEY`) are loaded securely via environment variables.
2. **Input Validation**: `Flask-WTF` is used to enforce strict server-side validation on all forms (e.g., ensuring transfer amounts are positive floats, emails are valid, and passwords meet complexity criteria).
3. **Authentication & Session Management**: Secure session cookies configured with `HttpOnly`, `SameSite=Lax`, and inactivity timeouts to prevent session hijacking. Brute-force protection locks accounts for 15 minutes after 5 failed login attempts.
4. **Cryptography**: Passwords are never stored in plaintext (hashed with `bcrypt`). Highly sensitive data (like the user's `account_number`) is symmetrically encrypted at rest in the database using the `cryptography` library (Fernet).
5. **Cross-Site Request Forgery (CSRF)**: Globally protected via `CSRFProtect`. Every POST form requires a valid, hidden CSRF token.
6. **Cross-Site Scripting (XSS)**: Prevented via Jinja2's default auto-escaping and strict Content-Security-Policies (CSP) in HTTP response headers.
7. **Parameter Manipulation Protection**: Business logic ensures users cannot transfer negative amounts, cannot transfer to themselves, cannot download other users' statements, and cannot bypass HTML frontend limits.
8. **Exception Management**: Custom error pages (404, 403, 500) ensure internal stack traces and server details are never leaked to end users.
9. **Auditing and Logging**: Critical events (successful logins, failed logins, account lockouts, transactions, unauthorized access attempts) are logged securely to an audit trail (`bank_audit.log`).

## Setup and Installation (Local Development)

### Prerequisites
- Python 3.8+
- `pip`

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/secure-bank-pro.git
cd secure-bank-pro
```

### 2. Create a virtual environment & install dependencies
*(On Windows, you can simply run the provided `run.bat` script, or follow the manual steps below).*
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-random-secret-key
ENCRYPTION_KEY=2cI63bH6aXpGk1_8gJ6fL4d_Z-QeYwT7kV1lA2hG5xE=
```

### 4. Run the Application
```bash
python app.py
```
Navigate to `http://127.0.0.1:5000` in your web browser. (The database will auto-initialize on startup).

## Default Test Accounts
If running locally, the following accounts are auto-generated:
- **Admin**: `admin@bank.com` / `admin123`

---
*Disclaimer: This is an educational project demonstrating security principles. In a real-world scenario, you would use a production database like PostgreSQL and a robust Key Management Service (KMS) for encryption keys.*
