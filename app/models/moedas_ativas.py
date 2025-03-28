from app.database import db

class MoedasAtivas(db.Model):
    __tablename__ = 'moedas_ativas'
    
    moedas_ativas_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    moedas_ativas_simbolo = db.Column(db.String(45), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)