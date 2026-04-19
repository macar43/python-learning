import os

class Config:
    """Flask-Konfiguration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = True
    TESTING = False
