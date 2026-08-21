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

## Deployment (Free & No Credit Card Required)

Since this application uses SQLite (which requires persistent storage), the best place to host it for free without a credit card is **PythonAnywhere**.

### Step 1: Push Code to GitHub
Ensure all your project files are pushed to a public or private GitHub repository.

### Step 2: Set up PythonAnywhere
1. Create a free "Beginner" account on [PythonAnywhere](https://www.pythonanywhere.com/).
2. From the dashboard, open a new **Bash Console**.
3. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/secure-bank-pro.git
   ```
4. Install dependencies:
   ```bash
   cd secure-bank-pro
   pip3.10 install --user -r requirements.txt
   ```

### Step 3: Create the Web App
1. Go to the **Web** tab in PythonAnywhere and click **Add a new web app**.
2. Skip the domain name screen by clicking Next.
3. Select **Manual Configuration** (Do NOT select Flask) and choose **Python 3.10**.
4. Once created, scroll down to the **Code** section:
   - Set **Source code** to: `/home/YOUR_USERNAME/secure-bank-pro`
   - Set **Working directory** to: `/home/YOUR_USERNAME/secure-bank-pro`

### Step 4: Configure WSGI
1. In the Web tab, click the link under **WSGI configuration file**.
2. Delete everything inside the file and paste this:

```python
import sys
import os

path = '/home/YOUR_USERNAME/secure-bank-pro'
if path not in sys.path:
    sys.path.insert(0, path)

# Secure Environment Variables
os.environ['SECRET_KEY'] = 'generate-a-secure-random-key'
os.environ['ENCRYPTION_KEY'] = '2cI63bH6aXpGk1_8gJ6fL4d_Z-QeYwT7kV1lA2hG5xE='

from app import create_app
application = create_app()
```
*(Make sure to replace `YOUR_USERNAME` with your PythonAnywhere username!)*

3. Click **Save** and then hit the big green **Reload** button on the Web tab. Your app is now live!

## Default Test Accounts
If initialized via `init_db.py`:
- **Admin**: `admin@bank.com` / `admin123`
- **User**: `john@example.com` / `password123`

---
*Disclaimer: This is an educational project demonstrating security principles. In a real-world scenario, you would use a production database like PostgreSQL and a robust Key Management Service (KMS) for encryption keys.*
