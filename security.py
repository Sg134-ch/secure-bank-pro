from cryptography.fernet import Fernet
from config import Config
import logging

fernet = Fernet(Config.ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """Encrypts string data for secure storage."""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    """Decrypts string data retrieved from storage."""
    return fernet.decrypt(token.encode()).decode()

# Security: Configure auditing/logging
logging.basicConfig(
    filename='bank_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def audit_log(message: str):
    """Log an audit event."""
    logging.info(message)
