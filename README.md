# Flask App - blacklist - LosDeploy

Microservicio Flask y Python diseñado para gestionar lista negra (blacklist) de correos electrónicos.

## Nota: 
correr con versión de python 3.9.6

## 🚀 Características

- Microservicio Flask
- Base de datos PostgreSQL con SQLAlchemy ORM
- API REST para añadir y consultar emails en la lista negra
- Autenticación con Token Estático para facilitar el uso del API en etapa de desarrollo

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

### 0. intalación base de datos PostgresSQL

  #### Parte 1: 
  - Instalar PostgreSQL
  - Abre PgAdmin. Clic derecho en Servers → Create → Server. 
  - En la pestaña General, ponle un nombre (por ejemplo, PostgresLocal).
  - En la pestaña Connection, usa estos valores:
      Host name/address: localhost
      Port: 5432
      Username: postgres
      Password: postgres
  - Guarda y conéctate.
  
  #### Parte 2:
  - Crear la base de datos
  - Clic derecho en Databases → Create → Database...
    - Nombre: blacklist_db
    - Guarda

  #### Parte 3:
  - Construir la URI de conexión
  - formato: postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_datos>
  - ejmeplo: postgresql://postgres:postgres@localhost:5432/blacklist_db


### 1. Clonar o descargar el proyecto
```bash
cd LosDeploy
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
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/blacklist_db
SECRET_KEY=mi_clave_ultra_secreta_123
JWT_SECRET_KEY=mi-jwt-secret-key
STATIC_TOKEN=token-estatico-123456
```

### 5. Ejecutar la aplicación
```bash
python application.py
```

La aplicación estará disponible en: `http://localhost:5001`


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
curl -X POST http://localhost:5001/blacklists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-estatico-123456" \
  -d '{"email": "test@example.com", "app_uuid": "app-123", "blocked_reason": "Spam"}'
```

#### 3. Consultar si un email está en la lista negra:
```bash
curl -X GET http://localhost:5001/blacklists/test@example.com \
  -H "Authorization: Bearer token-estatico-123456"
```

## 📘 Documentación del API REST

La documentación completa de los endpoints del proyecto se encuentra disponible en Postman.  
En esta colección se especifican los métodos, parámetros, cuerpos de solicitud y ejemplos de respuesta para cada uno de los servicios.

🔗 **Acceso a la colección en Postman:**  
[Ver documentación del API en Postman](https://www.postman.com/omar-253386/workspace/blacklist-api/collection/43599343-3e4639b5-90dc-4394-81da-56544d800cad?action=share&source=copy-link&creator=43599343)
