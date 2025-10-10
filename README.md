# Flask App - blacklist - LosDeploy

Un microservicio Flask y Python diseñado para gestionar una lista negra (blacklist) de correos electrónicos, con una API RESTful.

## 🚀 Características

- **Microservicio Flask** para una API RESTful rápida y eficiente
- **Base de datos SQLite/PostgreSQL** con SQLAlchemy ORM
- **API REST completa** para añadir y consultar emails en la lista negra
- **Autenticación con Token Estático** para facilitar el uso del API en etapa de desarrollo

## 📁 Estructura del Proyecto

```
LosDeploy/
├── .env                # Variables de entorno
├── .gitignore          # Archivos a ignorar en Git
├── application.py      # Punto de entrada de la aplicación Flask
├── config.py           # Configuraciones de la aplicación
├── models.py           # Modelos de base de datos con SQLAlchemy
├── requirements.txt    # Dependencias de Python
└── routes.py           # Rutas (endpoints) de la API
```

## 🛠️ Instalación y Configuración

### 1. Clonar o descargar el proyecto
```bash
cd /Users/omarfernando/Desktop/DevOps/LosDeploy
```

### 2. Crear entorno virtual (recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate     # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=sqlite:///local.db
SECRET_KEY=mi_clave_ultra_secreta_123
JWT_SECRET_KEY=mi-jwt-secret-key
STATIC_TOKEN=token-estatico-123456
```

### 5. Ejecutar la aplicación
```bash
python application.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📡 API Endpoints

Todos los endpoints requieren autenticación mediante un **Token Estático** enviado en la cabecera `Authorization` como `Bearer <tu_static_token>`.

### Lista Negra (Blacklist)
- `POST /blacklists` - Agrega un email a la lista negra. Requiere `email` y `app_uuid` en el cuerpo JSON.
- `GET /blacklists/<email>` - Consulta si un email está en la lista negra.

### Ejemplo de uso de la API

#### 1. Obtener un token estático (desde tu `.env`)
```
Bearer token-estatico-123456
```

#### 2. Agregar un email a la lista negra:
```bash
curl -X POST http://localhost:5000/blacklists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mi-token-estatico-123456" \
  -d '{"email": "test@example.com", "app_uuid": "app-123", "blocked_reason": "Spamming"}'
```

#### 3. Consultar si un email está en la lista negra:
```bash
curl -X GET http://localhost:5000/blacklists/test@example.com \
  -H "Authorization: Bearer mi-token-estatico-123456"
```

## 🗄️ Modelos de Base de Datos

### Blacklist
- `id`: Identificador único (entero)
- `email`: Dirección de correo electrónico (cadena, única, indexada)
- `app_uuid`: UUID de la aplicación que bloqueó el email (cadena)
- `blocked_reason`: Motivo del bloqueo (cadena, opcional)
- `created_at`: Fecha y hora de creación del registro

## 🔧 Configuración

El archivo `config.py` centraliza las configuraciones clave de la aplicación, incluyendo:
-   `SECRET_KEY`: Clave secreta de Flask para seguridad general.
-   `DATABASE_URL`: URI de conexión a la base de datos (SQLite o PostgreSQL).
-   `JWT_SECRET_KEY`: Clave secreta para la firma y verificación de JSON Web Tokens (JWT).
-   `STATIC_TOKEN`: Token estático para la autenticación básica de la API.

Estas variables se cargan desde el archivo `.env` o usan valores por defecto para desarrollo.

## 📝 Tecnologías Utilizadas

-   **Backend**: Python 3.x, Flask, SQLAlchemy
-   **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
-   **Autenticación**: Token Estático, Flask-JWT-Extended (preparado)
-   **Herramientas**: python-dotenv, psycopg2-binary, gunicorn, Flask-RESTful, Flask-Marshmallow