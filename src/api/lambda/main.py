import os
import json
import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

secrets_manager = boto3.client("secretsmanager")
lambda_client = boto3.client("lambda")

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    # Validate WhatsApp signature (omitted for brevity, but required in production)
    logger.info("Received message from WhatsApp")

    # Invoke the QA agent lambda
    lambda_client.invoke(
        FunctionName=os.environ["QA_AGENT_LAMBDA_ARN"],
        InvocationType="Event",
        Payload=json.dumps(event)
    )

    return {"statusCode": 200, "body": "Message received"}
