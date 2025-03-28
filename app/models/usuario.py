from app.database import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    usuario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_login = db.Column(db.String(150), nullable=False)
    usuario_senha = db.Column(db.Text)
    usuario_saldo = db.Column(db.Numeric(10,2), default=0.00)
    usuario_binanceApiKey = db.Column(db.Text)
    usuario_binanceSecretKey = db.Column(db.Text)
    
    moedas_ativas = db.relationship('MoedasAtivas', backref='usuario', lazy=True)
    config = db.relationship('UsuarioConfig', backref='usuario', lazy=True, uselist=False)