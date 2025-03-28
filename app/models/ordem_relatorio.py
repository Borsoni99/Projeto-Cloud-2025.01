from app.database import db

class OrdemRelatorio(db.Model):
    __tablename__ = 'ordem_relatorio'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    preco_compra = db.Column(db.Numeric(10,2), default=0.00)
    preco_venda = db.Column(db.Numeric(10,2), default=0.00)
    qtd = db.Column(db.Numeric(10,2), default=0.00)
    moeda = db.Column(db.String(20), nullable=False)
    data_operacao = db.Column(db.DateTime, nullable=False)