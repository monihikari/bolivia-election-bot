# Chatbot para Elecciones Presidenciales de Bolivia 2025

Este proyecto implementa un agente de IA conversacional diseñado para responder a preguntas frecuentes sobre las propuestas de los candidatos a las elecciones presidenciales de Bolivia 2025.

## Arquitectura

El sistema se basa en una arquitectura serverless en AWS, orquestada con AWS CDK v2 en Python. La arquitectura sigue un enfoque de RAG (Retrieval-Augmented Generation) para proporcionar respuestas precisas y contextualizadas.

- **Entrada de Usuario**: La interacción con el usuario se gestiona a través de un webhook de WhatsApp Business, que se integra con el sistema mediante Amazon API Gateway y una función AWS Lambda.
- **Procesamiento de Lenguaje Natural**: El núcleo del chatbot utiliza Amazon Bedrock para el procesamiento de lenguaje natural y la generación de respuestas.
- **Base de Conocimiento**: Las propuestas de los candidatos, en formato PDF, se almacenan en un bucket de Amazon S3. AWS Textract se utiliza para extraer el texto de estos documentos.
- **Búsqueda y Recuperación**: Amazon OpenSearch Serverless se emplea para indexar y buscar en la información extraída de las propuestas, permitiendo una recuperación eficiente de la información relevante.

## Estructura del Proyecto

El proyecto está organizado en los siguientes directorios principales:

- `app.py`: Archivo principal de la aplicación CDK.
- `cdk.json`: Archivo de configuración de CDK.
- `requirements.txt`: Dependencias de Python para el proyecto.
- `src/`: Contiene el código fuente de la aplicación.
  - `api/`: Stack de la API y función Lambda para la integración con WhatsApp.
  - `auth/`: Stack de autenticación.
  - `chat/`: Stack del chatbot y función Lambda para el procesamiento de mensajes.
  - `common/`: Recursos comunes compartidos entre los stacks.
  - `ingestion/`: Stack de ingesta y función Lambda para el procesamiento de documentos.
  - `networking/`: Stack de configuración de red.
  - `storage/`: Stack de almacenamiento para los buckets de S3.
- `tests/`: Contiene los tests unitarios del proyecto.
- `propuestas/`: Contiene los programas de gobierno de los partidos políticos en formato PDF.
- `scripts/`: Contiene scripts para enviar mensajes de prueba y probar la funcionalidad de búsqueda.

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
   cd bolivia-election-bot
   ```

2. **Configurar el entorno virtual y las dependencias:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
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

## Testing

Para ejecutar los tests unitarios, utiliza el siguiente comando:

```bash
pytest
```
