from flask import Blueprint, request, jsonify
from models import db, Blacklist
from config import Config
from functools import wraps

api_bp = Blueprint('api', __name__)

# Verificación de token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 401
        
        # Verificar token estático
        expected_token = f"Bearer {Config.STATIC_TOKEN}"
        if token != expected_token:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated_function


# Endpoint para health check AWS
@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'unhealthy'}), 500  # ❌ ESCENARIO 3: Health check fallido para probar CD fallido

# POST /blacklists - Agregar email a lista negra
@api_bp.route('/blacklists', methods=['POST'])
@token_required
def add_to_blacklist():
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data or 'email' not in data or 'app_uuid' not in data:
            return jsonify({
                'error': 'Faltan campos requeridos: email y app_uuid'
            }), 400
        
        email = data.get('email')
        app_uuid = data.get('app_uuid')
        blocked_reason = data.get('blocked_reason', '')
        
        # Validar longitud del motivo
        if blocked_reason and len(blocked_reason) > 255:
            return jsonify({
                'error': 'blocked_reason no puede exceder 255 caracteres'
            }), 400
        
        # Obtener IP del cliente
        ip_address = request.remote_addr or request.environ.get('HTTP_X_FORWARDED_FOR', 'unknown')
        
        # Verificar si el email ya está en la lista negra
        existing = Blacklist.query.filter_by(email=email).first()
        if existing:
            return jsonify({
                'message': 'El email ya está en la lista negra',
            }), 200
        
        # Crear nuevo registro
        new_blacklist = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip_address=ip_address
        )
        
        db.session.add(new_blacklist)
        db.session.commit()
        
        return jsonify({
            'message': 'Email agregado a la lista negra exitosamente',
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# GET /blacklists/<email> - Consultar si email está en lista negra
@api_bp.route('/blacklists/<string:email>', methods=['GET'])
@token_required
def check_blacklist(email):
    try:
        blacklist_entry = Blacklist.query.filter_by(email=email).first()
        
        if blacklist_entry:
            return jsonify({
                'in_blacklist': True,
                'blocked_reason': blacklist_entry.blocked_reason,
            }), 200
        else:
            return jsonify({
                'in_blacklist': False,
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500