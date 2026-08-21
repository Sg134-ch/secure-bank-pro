from flask import render_template, redirect, url_for, flash, request, abort, Blueprint, Response
from flask_login import login_user, current_user, logout_user, login_required
from models import db, User, Account, Transaction
from forms import LoginForm, TransferForm, RegistrationForm, AdminDepositForm, BillPayForm, ChangePasswordForm
from security import audit_log
from urllib.parse import urlparse
from datetime import datetime, timedelta
import random
import csv
import io

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        acc_num = str(random.randint(100000000, 999999999))
        account = Account(user_id=user.id, account_number=acc_num, balance=0.0)
        db.session.add(account)
        db.session.commit()
        
        audit_log(f"New user registered: {user.email}")
        flash('Registration successful! Please log in to access your dashboard.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Security: Brute-force account lockout protection
        if user:
            if user.locked_until and user.locked_until > datetime.utcnow():
                audit_log(f"Locked account attempted login: {form.email.data}")
                flash('Your account is temporarily locked due to multiple failed login attempts. Please try again later.', 'danger')
                return redirect(url_for('main.login'))
                
            if not user.check_password(form.password.data):
                user.failed_logins += 1
                if user.failed_logins >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=15)
                    audit_log(f"SECURITY ALERT: Account locked for {form.email.data} due to brute force attempt.")
                db.session.commit()
                audit_log(f"Failed login attempt for email: {form.email.data}")
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('main.login'))
                
            # Success - reset failed logins
            user.failed_logins = 0
            user.locked_until = None
            db.session.commit()
            
            login_user(user)
            audit_log(f"User {user.email} logged in successfully.")
            
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.dashboard')
            return redirect(next_page)
        else:
            # Prevent user enumeration by giving same error if user doesn't exist
            audit_log(f"Failed login attempt for unknown email: {form.email.data}")
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('main.login'))
            
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
@login_required
def logout():
    audit_log(f"User {current_user.email} logged out.")
    logout_user()
    flash('You have been securely logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    account = current_user.account
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.timestamp.desc()).limit(15).all()
    
    # Calculate simple stats for UI
    total_in = sum(t.amount for t in transactions if t.amount > 0)
    total_out = sum(abs(t.amount) for t in transactions if t.amount < 0)
    
    return render_template('dashboard.html', title='Dashboard', account=account, transactions=transactions, total_in=total_in, total_out=total_out)

@main.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    form = TransferForm()
    if form.validate_on_submit():
        amount = form.amount.data
        recipient_email = form.recipient_email.data
        
        if amount <= 0:
            flash('Amount must be strictly positive.', 'danger')
            return redirect(url_for('main.transfer'))
            
        recipient = User.query.filter_by(email=recipient_email).first()
        if recipient.id == current_user.id:
            flash('You cannot transfer funds to your own account.', 'danger')
            return redirect(url_for('main.transfer'))
            
        sender_account = current_user.account
        recipient_account = recipient.account
        
        if sender_account.balance < amount:
            audit_log(f"Failed transfer: User {current_user.email} attempted to transfer {amount} (Insufficient Funds)")
            flash('Insufficient funds to complete this transfer.', 'danger')
            return redirect(url_for('main.transfer'))
            
        try:
            sender_account.balance -= amount
            recipient_account.balance += amount
            
            t_out = Transaction(account_id=sender_account.id, amount=-amount, transaction_type='TRANSFER_OUT', description=f"Transfer to {recipient.email}")
            t_in = Transaction(account_id=recipient_account.id, amount=amount, transaction_type='TRANSFER_IN', description=f"Transfer from {current_user.email}")
            
            db.session.add(t_out)
            db.session.add(t_in)
            db.session.commit()
            
            audit_log(f"Successful transfer: User {current_user.email} transferred {amount} to {recipient.email}")
            flash('Fund transfer completed successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            audit_log(f"Exception during transfer: {str(e)}")
            flash('An internal error occurred during the transfer. Our security team has been notified.', 'danger')
            
    return render_template('transfer.html', title='Transfer Funds', form=form)

@main.route('/bill_pay', methods=['GET', 'POST'])
@login_required
def bill_pay():
    form = BillPayForm()
    if form.validate_on_submit():
        amount = form.amount.data
        biller = form.biller.data
        account = current_user.account
        
        if account.balance < amount:
            audit_log(f"Failed bill pay: User {current_user.email} attempted to pay {amount} (Insufficient Funds)")
            flash('Insufficient funds to pay this bill.', 'danger')
            return redirect(url_for('main.bill_pay'))
            
        try:
            account.balance -= amount
            t = Transaction(account_id=account.id, amount=-amount, transaction_type='BILL_PAY', description=f"Payment to {biller} (Acct: {form.account_number.data[-4:]})")
            db.session.add(t)
            db.session.commit()
            
            audit_log(f"Successful bill payment: User {current_user.email} paid {amount} to {biller}")
            flash(f'Successfully paid ₹{amount:.2f} to {biller}.', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            audit_log(f"Exception during bill pay: {str(e)}")
            flash('Error processing payment.', 'danger')
            
    return render_template('bill_pay.html', title='Pay Bills', form=form)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            audit_log(f"Failed password change attempt by {current_user.email} (wrong current password)")
            flash('Your current password was incorrect.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            audit_log(f"User {current_user.email} successfully updated their password.")
            flash('Your password has been updated securely.', 'success')
            return redirect(url_for('main.profile'))
            
    return render_template('profile.html', title='Security Profile', form=form)

@main.route('/statement/download')
@login_required
def download_statement():
    # Security: Ensure users can only download their own transactions
    transactions = Transaction.query.filter_by(account_id=current_user.account.id).order_by(Transaction.timestamp.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Timestamp (UTC)', 'Description', 'Transaction Type', 'Amount (INR)'])
    
    for t in transactions:
        writer.writerow([t.timestamp.strftime('%Y-%m-%d %H:%M:%S'), t.description, t.transaction_type, f"{t.amount:.2f}"])
        
    audit_log(f"User {current_user.email} downloaded account statement.")
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=secure_statement_{current_user.account.account_number[-4:]}.csv"}
    )

@main.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        audit_log(f"Unauthorized access attempt to admin panel by {current_user.email}")
        abort(403) 
    
    users = User.query.all()
    form = AdminDepositForm()
    return render_template('admin.html', title='Admin Dashboard', users=users, form=form)

@main.route('/admin/deposit/<int:user_id>', methods=['POST'])
@login_required
def admin_deposit(user_id):
    if current_user.role != 'admin':
        abort(403)
        
    form = AdminDepositForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        amount = form.amount.data
        if user.account:
            user.account.balance += amount
            t_in = Transaction(account_id=user.account.id, amount=amount, transaction_type='DEPOSIT', description='Bank Deposit')
            db.session.add(t_in)
            db.session.commit()
            audit_log(f"Admin deposited {amount} to user {user.email}")
            flash(f'Successfully deposited ₹{amount:.2f} to {user.email}', 'success')
        else:
            flash('User does not have a valid account setup.', 'danger')
    return redirect(url_for('main.admin_panel'))
