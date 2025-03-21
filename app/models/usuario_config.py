from app.database import db

class UsuarioConfig(db.Model):
    __tablename__ = 'usuario_config'
    
    usuario_config_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    usuario_config_valorCompra = db.Column(db.Numeric(10,2), default=5.00)
    usuario_config_pctGanho = db.Column(db.Numeric(5,2), default=10.00)
    usuario_config_pctPerda = db.Column(db.Numeric(5,2), default=10.00) 