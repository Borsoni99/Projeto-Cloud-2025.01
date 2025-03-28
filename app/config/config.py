from os import environ
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://grupo:administrador99*@trading-bot.mysql.database.azure.com/trading-bot?ssl_verify_cert=false')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
