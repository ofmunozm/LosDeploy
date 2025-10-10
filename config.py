import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///local.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-secret'
    
    # Token estático para autenticación
    STATIC_TOKEN = os.environ.get('STATIC_TOKEN') or 'Bearer token-estatico-123'