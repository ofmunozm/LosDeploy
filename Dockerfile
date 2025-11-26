FROM python:3.8-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias incluyendo New Relic
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Configuración de New Relic mediante variables de entorno
# NEW_RELIC_APP_NAME se pasa como variable de entorno (diferente por ambiente)
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG_LEVEL=info

# Nota: NEW_RELIC_LICENSE_KEY se pasa en docker run con -e

EXPOSE 5000

# Ejecutar con New Relic wrapper
ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "application:application"]
