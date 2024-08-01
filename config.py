import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_hard_to_guess_string')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ecommerce.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
