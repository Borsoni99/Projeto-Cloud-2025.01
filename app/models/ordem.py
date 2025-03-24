from app.database import db
from decimal import Decimal

class Ordem(db.Model):
    __tablename__ = 'ordem'
    
    ordem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    simbolo = db.Column(db.String(20), nullable=False)
    tp_operacao = db.Column(db.String(10), nullable=False)  # 'COMPRA' ou 'VENDA'
    quantidade = db.Column(db.Numeric(20,8), nullable=False)
    preco = db.Column(db.Numeric(20,8), nullable=False)
    qtd_executada = db.Column(db.Numeric(20,8), default=0)
    tipo = db.Column(db.String(20), nullable=False)  # 'LIMITE' ou 'MERCADO'
    status = db.Column(db.String(20), nullable=False, default='PENDENTE')  # 'PENDENTE', 'EXECUTADA', 'CANCELADA'
    
    # Relacionamento com o usuário
    usuario = db.relationship('Usuario', backref=db.backref('ordens', lazy=True))
    
    # Relacionamento com os fills da ordem
    fills = db.relationship('OrdemFill', backref='ordem', lazy=True, cascade='all, delete-orphan')

class OrdemFill(db.Model):
    __tablename__ = 'ordem_fill'
    
    ordem_fill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordem_id = db.Column(db.Integer, db.ForeignKey('ordem.ordem_id'), nullable=False)
    quantidade = db.Column(db.Numeric(20,8), nullable=False)
    preco = db.Column(db.Numeric(20,8), nullable=False) 