# Proyecto Chatbot para Elecciones Bolivia 2025 con AWS CDK

Este proyecto implementa un agente de IA conversacional para responder preguntas frecuentes sobre las propuestas de los candidatos a las elecciones presidenciales de Bolivia 2025.

## Arquitectura

El sistema utiliza una arquitectura serverless en AWS, orquestada con AWS CDK v2 en Python.

- **Entrada**: Webhook de WhatsApp Business (API Gateway + Lambda).
- **Procesamiento**: RAG (Retrieval-Augmented Generation) con Amazon Bedrock y Amazon OpenSearch Serverless.
- **Base de Conocimiento**: PDFs en S3, procesados con AWS Textract.

## Despliegue

### Prerrequisitos

- Cuenta de AWS
- AWS CLI configurado
- Node.js y npm
- Python 3.12
- Docker (para empaquetado de Lambdas)

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd ...
   ```

2. **Configurar el entorno virtual y las dependencias:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Bootstrap de CDK (si es la primera vez en la cuenta/región):**
   ```bash
   export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
   export AWS_REGION=<TU_REGION_AWS>
   cdk bootstrap aws://$AWS_ACCOUNT_ID/$AWS_REGION
   ```

4. **Configurar secretos:**
   - Crea un secreto en AWS Secrets Manager para el token de WhatsApp Business.

5. **Desplegar los stacks:**
   ```bash
   cdk deploy --all --require-approval never
   ```

## Uso

Para enviar un mensaje de prueba, utiliza el script `scripts/send_demo_message.py` después de configurar las variables de entorno necesarias.