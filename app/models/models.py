from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    usuario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_login = db.Column(db.String(150), nullable=False)
    usuario_senha = db.Column(db.Text)
    usuario_saldo = db.Column(db.Numeric(10,2), default=0.00)
    usuario_binanceApiKey = db.Column(db.Text)
    usuario_binanceSecretKey = db.Column(db.Text)
    
    # Relationships
    moedas_ativas = db.relationship('MoedasAtivas', backref='usuario', lazy=True)
    config = db.relationship('UsuarioConfig', backref='usuario', lazy=True, uselist=False)

class MoedasAtivas(db.Model):
    __tablename__ = 'moedas_ativas'
    
    moedas_ativas_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    moedas_ativas_simbolo = db.Column(db.String(45), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)

class UsuarioConfig(db.Model):
    __tablename__ = 'usuario_config'
    
    usuario_config_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    usuario_config_valorCompra = db.Column(db.Numeric(10,2), default=5.00)
    usuario_config_pctGanho = db.Column(db.Numeric(5,2), default=10.00)
    usuario_config_pctPerda = db.Column(db.Numeric(5,2), default=10.00) 