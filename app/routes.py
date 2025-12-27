from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from .models import User, Employee
from .forms import LoginForm, RegisterForm, EmployeeForm
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from functools import wraps
from . import bcrypt

main = Blueprint('main', __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required", "danger")
            return redirect(url_for('main.login'))
        return fn(*args, **kwargs)
    return wrapper

@main.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered", "danger")
        else:
            user = User(name=form.name.data, email=form.email.data, is_admin=form.is_admin.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User registered", "success")
            return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.employee_list'))  # Go to employee list page
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/')
@login_required
def index():
    return redirect(url_for('main.employee_list'))

@main.route('/employees')
@login_required
def employee_list():
    employees = Employee.query.all()
    return render_template('employees/list.html', employees=employees)

@main.route('/employees/create', methods=['GET','POST'])
@login_required
@admin_required
def employee_create():
    form = EmployeeForm()
    if form.validate_on_submit():
        emp = Employee(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            department=form.department.data,
            position=form.position.data,
            salary=form.salary.data,
            date_joined=form.date_joined.data
        )
        # handle file upload
        file = request.files.get('profile_pic')
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            emp.profile_pic = filename

        db.session.add(emp)
        db.session.commit()
        flash("Employee added", "success")
        return redirect(url_for('main.employee_list'))
    return render_template('employees/form.html', form=form)

@main.route('/employees/<int:id>/edit', methods=['GET','POST'])
@login_required
@admin_required
def employee_edit(id):
    emp = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=emp)
    if form.validate_on_submit():
        form.populate_obj(emp)
        file = request.files.get('profile_pic')
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            emp.profile_pic = filename
        db.session.commit()
        flash("Employee updated", "success")
        return redirect(url_for('main.employee_list'))
    return render_template('employees/form.html', form=form, emp=emp)

@main.route('/employees/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def employee_delete(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    flash("Employee deleted", "success")
    return redirect(url_for('main.employee_list'))

@main.route('/employees/<int:id>')
@login_required
def employee_detail(id):
    emp = Employee.query.get_or_404(id)
    return render_template('employees/detail.html', emp=emp)
