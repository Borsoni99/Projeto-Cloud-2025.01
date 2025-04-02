from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.controller.usuario_controller import usuario_bp
from app.controller.moedas_ativas_controller import moedas_ativas_bp
from app.controller.ordem_controller import ordem_bp
from app.database import db
import pymysql
pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Carregar configurações
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(usuario_bp, url_prefix="/usuario")
    app.register_blueprint(moedas_ativas_bp, url_prefix="/moedas_ativas")
    app.register_blueprint(ordem_bp, url_prefix="/ordem")
    
    return app 