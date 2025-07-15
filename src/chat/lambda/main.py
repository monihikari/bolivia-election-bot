import os
import json
import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    body = json.loads(event["body"])
    question = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
    sender = body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

    logger.info(f"Received question: '{question}' from {sender}")

    # --- Bedrock and OpenSearch logic is temporarily disabled ---
    # Simulating a successful response for testing purposes.
    answer = f"Respuesta de prueba para la pregunta: '{question}'. El sistema está funcionando, pero el acceso a Bedrock está pendiente."

    logger.info(f"Generated mock answer: {answer}")

    # The WhatsApp sending logic is also disabled for this test.
    # whatsapp_token = secrets_manager.get_secret_value(SecretId=whatsapp_token_secret_arn)["SecretString"]
    # ... (rest of the sending logic)

    return {
        "statusCode": 200, 
        "body": json.dumps({"answer": answer})
    }
