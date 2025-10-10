from flask import Flask
from models import db
from routes import api_bp
from config import Config

application = Flask(__name__)
application.config.from_object(Config)

# Se inicializa la base de datos
db.init_app(application)

# Registrar blueprints (rutas)
application.register_blueprint(api_bp)

# Crear las tablas en la base de datos
with application.app_context():
    db.create_all()

# Ruta raíz
@application.route('/')
def index():
    return {
        'message': 'Blacklist Microservice API',
        'version': '1.0',
        'endpoints': {
            'add_to_blacklist': 'POST /blacklists',
            'check_blacklist': 'GET /blacklists/<email>'
        }
    }

# Para ejecutar localmente
if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5001)