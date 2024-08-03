import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://example_user:example_password@localhost:5432/example_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

