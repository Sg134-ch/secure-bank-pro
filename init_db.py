from app import create_app
from models import db, User, Account
from security import audit_log
import os

app = create_app()

def initialize_database():
    with app.app_context():
        # Security: Drop old tables to start fresh in this dev environment
        db.drop_all()
        db.create_all()
        
        # Create Admin User
        admin = User(username='admin', email='admin@bank.com', role='admin')
        admin.set_password('admin123') # In a real system, never use hardcoded simple passwords
        db.session.add(admin)
        db.session.commit() # Commit to get ID
        
        admin_account = Account(user_id=admin.id, account_number='100000001', balance=1000000.0)
        db.session.add(admin_account)
        
        # Create Standard User
        user1 = User(username='johndoe', email='john@example.com', role='user')
        user1.set_password('password123')
        db.session.add(user1)
        db.session.commit()
        
        user1_account = Account(user_id=user1.id, account_number='100000002', balance=50000.0)
        db.session.add(user1_account)
        
        # Create Another Standard User
        user2 = User(username='janedoe', email='jane@example.com', role='user')
        user2.set_password('password123')
        db.session.add(user2)
        db.session.commit()
        
        user2_account = Account(user_id=user2.id, account_number='100000003', balance=25000.0)
        db.session.add(user2_account)
        
        db.session.commit()
        print("Database initialized with test users:")
        print("- admin@bank.com / admin123 (Role: admin)")
        print("- john@example.com / password123 (Role: user)")
        print("- jane@example.com / password123 (Role: user)")
        
        audit_log("System database initialized.")

if __name__ == '__main__':
    initialize_database()
