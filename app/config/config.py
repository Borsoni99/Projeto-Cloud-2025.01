from os import environ
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://grupo:administrador99*@trading-bot.mysql.database.azure.com/trading-bot?ssl_verify_cert=false')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Environment
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = ENV == 'development'
    
    # Azure App Service typically uses port 8000
    PORT = int(os.getenv('PORT', 8000))
    
    # Streamlit configuration
    STREAMLIT_SERVER_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
    
    # Base URLs
    CLOUD_API_URL = 'https://ibmec-trading-bot-bfg3gngbgre4ambh.centralus-01.azurewebsites.net'
    LOCAL_API_URL = 'http://localhost:8000'
    
    # API URL - use Azure URL in production, localhost in development
    API_BASE_URL = os.getenv('API_BASE_URL', CLOUD_API_URL if ENV == 'production' else LOCAL_API_URL)
    
    # Streamlit specific configuration
    STREAMLIT_SERVER_URL = os.getenv('STREAMLIT_SERVER_URL', 'http://localhost:8501')
    
    @staticmethod
    def is_cloud_environment():
        """Check if we're running in Azure Cloud"""
        return bool(os.getenv('WEBSITE_SITE_NAME'))  # Azure App Service sets this
