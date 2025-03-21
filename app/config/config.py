from os import environ
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:admin@localhost:3306/trading_bot')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
