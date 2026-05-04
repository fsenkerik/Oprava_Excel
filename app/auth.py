from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from .models import Teacher

auth_bp = Blueprint('auth', __name__, url_prefix='/teacher')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        teacher = Teacher.query.filter_by(username=username).first()
        if teacher and check_password_hash(teacher.password_hash, password):
            login_user(teacher, remember=True)
            return redirect(url_for('teacher.dashboard'))
        flash('Nesprávné přihlašovací údaje.', 'danger')
    return render_template('teacher/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('student.index'))
