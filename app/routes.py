from flask import request, jsonify, render_template, session, redirect, url_for, flash, current_app as app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required
from app import db
from app.models import User, Product, Company, Document
from app.forms import RegistrationForm, LoginForm, UploadForm
import os

def configure_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        companies = Company.query.all()
        form.company_id.choices = [(company.id, company.name) for company in companies]
        if request.method == 'POST':
            if form.validate_on_submit():
                hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    company_id=form.company_id.data
                )
                db.session.add(user)
                db.session.commit()
                flash('Registration successful!')
                return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                flash('Login successful!')
                return redirect(url_for('upload'))
            flash('Invalid email or password.')
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('You have been logged out.')
        return redirect(url_for('home'))

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        form = UploadForm()
        companies = Company.query.all()
        form.company_id.choices = [(company.id, company.name) for company in companies]

        if form.validate_on_submit():
            file = form.document_file.data
            filename = secure_filename(file.filename)
            company = Company.query.get_or_404(form.company_id.data)
            user_id = session.get('user_id')

            if user_id is None:
                flash('User not logged in.')
                return redirect(url_for('login'))

            user = User.query.get_or_404(user_id)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], company.name)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file.save(os.path.join(file_path, filename))
            document = Document(filename=filename, user_id=user.id, company_id=company.id)
            db.session.add(document)
            db.session.commit()
            flash('Document uploaded successfully!')
            return redirect(url_for('upload'))

        return render_template('upload.html', form=form)

