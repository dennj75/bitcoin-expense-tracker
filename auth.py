from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from db.db_utils import crea_utente, get_user_by_username, get_user_by_id
from app import app, login_manager

auth_bp = Blueprint('auth', __name__)


class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def from_db_row(row):
        if not row:
            return None
        return User(id=row[0], username=row[1], email=row[2], password_hash=row[3])


@login_manager.user_loader
def load_user(user_id):
    row = get_user_by_id(user_id)
    return User.from_db_row(row)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not password:
            flash('Username e password richiesti', 'error')
            return redirect(url_for('auth.register'))
        # check existing
        existing = get_user_by_username(username)
        if existing:
            flash('Username già presente', 'error')
            return redirect(url_for('auth.register'))
        pw_hash = generate_password_hash(password)
        user_id = crea_utente(username, email, pw_hash)
        user = User(user_id, username, email, pw_hash)
        login_user(user)
        flash('Registrazione completata', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        row = get_user_by_username(username)
        if not row:
            flash('Credenziali non valide', 'error')
            return redirect(url_for('auth.login'))
        user = User.from_db_row(row)
        if not check_password_hash(user.password_hash, password):
            flash('Credenziali non valide', 'error')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('Login effettuato', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout effettuato', 'success')
    return redirect(url_for('home'))
