# Terraform - Infraestructura AWS

Esta carpeta contiene la configuración de Terraform para desplegar la infraestructura completa del proyecto Blacklist en AWS.

## Prerequisitos

1. **AWS CLI configurado:**
   ```bash
   aws configure
   ```

2. **Terraform instalado:**
   ```bash
   # macOS
   brew install terraform

   # Verificar instalación
   terraform version
   ```

3. **Credenciales AWS activas:**
   ```bash
   aws sts get-caller-identity
   ```

## Configuración Inicial

1. **Crear archivo de variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Editar `terraform.tfvars`** con tus valores reales:
   - `db_password`: Password seguro para PostgreSQL
   - `secret_key`: Flask SECRET_KEY
   - `jwt_secret_key`: JWT secret
   - `static_token`: Bearer token

3. **Verificar que terraform.tfvars está en .gitignore** (ya está configurado)

## Desplegar Infraestructura

### Paso 1: Inicializar Terraform
```bash
cd terraform/
terraform init
```

### Paso 2: Validar configuración
```bash
terraform validate
```

### Paso 3: Ver plan de ejecución
```bash
terraform plan
```

### Paso 4: Aplicar infraestructura
```bash
terraform apply
```

Terraform te mostrará qué recursos creará. Escribe `yes` para confirmar.

**Tiempo estimado:** 10-15 minutos (RDS tarda más)

### Paso 5: Obtener outputs
```bash
terraform output
```

Guarda estos valores:
- `alb_url`: URL pública de tu API
- `ecr_repository_url`: Para hacer push de imágenes Docker

## Recursos Creados

- **ECR Repository**: Para imágenes Docker
- **RDS PostgreSQL**: Base de datos (db.t3.micro)
- **ECS Fargate**: Cluster + Service + Task Definition
- **ALB**: Application Load Balancer (acceso público)
- **Security Groups**: Firewall rules
- **SSM Parameters**: Variables de entorno encriptadas
- **CloudWatch Logs**: Logs de ECS tasks
- **IAM Roles**: Permisos para ECS

## Comandos Útiles

### Ver estado actual
```bash
terraform show
```

### Ver outputs
```bash
terraform output
terraform output -json
```

### Ver logs de ECS
```bash
aws logs tail /ecs/blacklist --follow --region us-east-2
```

### Actualizar infraestructura
```bash
# Después de modificar archivos .tf
terraform plan
terraform apply
```

### Destruir toda la infraestructura
```bash
terraform destroy
```
⚠️ **CUIDADO:** Esto elimina TODOS los recursos, incluyendo la base de datos.

## Siguientes Pasos

Después de `terraform apply` exitoso:

1. **Push imagen inicial a ECR:**
   ```bash
   # Login a ECR
   aws ecr get-login-password --region us-east-2 | \
     docker login --username AWS --password-stdin $(terraform output -raw ecr_repository_url)

   # Build y push
   cd ..  # volver a raíz del proyecto
   docker build -t blacklist-docker .
   docker tag blacklist-docker:latest $(cd terraform && terraform output -raw ecr_repository_url):latest
   docker push $(cd terraform && terraform output -raw ecr_repository_url):latest
   ```

2. **Verificar deployment:**
   ```bash
   # Ver URL del API
   terraform output alb_url

   # Probar health check
   curl $(terraform output -raw alb_url)/health
   ```

3. **Configurar CodePipeline** (manual, ~15 minutos en AWS Console)

## Troubleshooting

### Error: AWS credentials
```bash
aws configure
aws sts get-caller-identity
```

### Error: Region incorrecta
Verificar que `aws_region = "us-east-2"` en terraform.tfvars

### RDS tarda mucho
Es normal, RDS puede tardar 10-15 minutos en crear

### ECS tasks no inician
```bash
# Ver logs
aws logs tail /ecs/blacklist --follow --region us-east-2

# Verificar task definition
aws ecs describe-task-definition --task-definition blacklist --region us-east-2
```

### Health checks fallan
- Verificar que la imagen Docker expone puerto 5000
- Verificar que `/health` endpoint retorna HTTP 200

## Estructura de Archivos

```
terraform/
├── main.tf           # Provider AWS + data sources
├── variables.tf      # Variables de entrada
├── outputs.tf        # Outputs (URLs, endpoints)
├── ecr.tf           # ECR Repository
├── rds.tf           # PostgreSQL RDS
├── ecs.tf           # ECS Cluster + Service + Task
├── alb.tf           # Application Load Balancer
├── security.tf      # Security Groups
├── ssm.tf           # SSM Parameters (secrets)
├── .gitignore       # Archivos a ignorar en Git
├── terraform.tfvars.example  # Ejemplo de variables
└── README.md        # Este archivo
```

## Costos Estimados

Dentro de **AWS Free Tier**:
- ECS Fargate: Primeros 25 GB/mes gratis
- RDS db.t3.micro: 750 horas/mes gratis
- ALB: 750 horas/mes + 15 GB tráfico gratis
- ECR: 500 MB storage gratis
- CloudWatch Logs: 5 GB ingesta gratis

**Total estimado fuera de free tier:** $0-15/mes (depende de uso)

## Soporte

Para más información, consulta:
- Plan completo: `~/.claude/plans/shiny-snacking-pudding.md`
- Documentación del proyecto: `../CLAUDE.md`