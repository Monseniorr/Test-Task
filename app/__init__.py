from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://example_user:example_password@localhost/example_db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config.from_pyfile('config.py')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import routes, models, forms
        routes.configure_routes(app)

    return app
