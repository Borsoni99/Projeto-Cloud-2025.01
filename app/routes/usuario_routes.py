from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.database import db

bp = Blueprint('usuario', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('usuario_login') or not data.get('usuario_senha'):
        return jsonify({'error': 'Missing registration data'}), 400

    # Check if username already exists
    existing_user = Usuario.query.filter_by(usuario_login=data['usuario_login']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    try:
        new_user = Usuario(
            usuario_login=data['usuario_login'],
            usuario_senha=data['usuario_senha'],
            usuario_binanceApiKey=data.get('usuario_binanceApiKey'),
            usuario_binanceSecretKey=data.get('usuario_binanceSecretKey')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'usuario_id': new_user.usuario_id,
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('usuario_login') or not data.get('usuario_senha'):
        return jsonify({'error': 'Missing login credentials'}), 400

    try:
        usuario = Usuario.query.filter_by(usuario_login=data['usuario_login']).first()
        
        if usuario and usuario.usuario_senha == data['usuario_senha']:
            return jsonify({
                'success': True,
                'usuario_id': usuario.usuario_id,
                'message': 'Login successful'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ... rest of the existing code ... 