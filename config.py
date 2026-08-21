import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security: Secret key for session management and CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-change-in-prod'
    
    # Security: Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bank.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security: Session configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production (requires HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes session timeout
    
    # Encryption key for sensitive data (e.g., account numbers)
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or b'2cI63bH6aXpGk1_8gJ6fL4d_Z-QeYwT7kV1lA2hG5xE='
