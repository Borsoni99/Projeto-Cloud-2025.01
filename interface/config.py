from os import environ
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Environment
    ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = ENV == 'development'
    
    # Streamlit configuration
    STREAMLIT_SERVER_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
    
    # Base URLs
    CLOUD_API_URL = 'https://ibmec-trading-bot-docker-ceamc9enbnhzbjf9.centralus-01.azurewebsites.net'
    LOCAL_API_URL = 'http://api:8000'  # Usando o nome do serviço do Docker
    
    # API URL - use Azure URL in production, localhost in development
    API_BASE_URL = os.getenv('API_BASE_URL', CLOUD_API_URL if ENV == 'production' else LOCAL_API_URL)
    
    @staticmethod
    def is_cloud_environment():
        """Check if we're running in Azure Cloud"""
        return bool(os.getenv('WEBSITE_SITE_NAME'))  # Azure App Service sets this 