from flask import Flask, render_template
from config import Config
from models import db, User
from routes import main
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    
    # Security: Enable CSRF protection globally for all forms
    csrf = CSRFProtect(app)
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'
    # Security: Session protection prevents session hijacking
    login_manager.session_protection = 'strong'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)

    # Security: Custom error handlers to avoid leaking stack traces
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    # Security: Adding security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net"
        return response

    # Auto-initialize database on startup (Great for Render ephemeral disks)
    with app.app_context():
        db.create_all()
        # Check if admin exists, if not, seed the database
        if not User.query.filter_by(email='admin@bank.com').first():
            from init_db import initialize_database
            # We skip dropping tables here, just create
            admin = User(username='admin', email='admin@bank.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
            admin_account = Account(user_id=admin.id, account_number='100000001', balance=1000000.0)
            db.session.add(admin_account)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) # Set debug=False in production
