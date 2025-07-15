import os
import json
import boto3

def invoke_qa_agent():
    lambda_client = boto3.client("lambda")

    payload = {
        "body": json.dumps({
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "text": {
                                            "body": "¿Cuál es la propuesta sobre la economía?"
                                        },
                                        "from": "1234567890"
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        })
    }

    response = lambda_client.invoke(
        FunctionName="ChatbotStack-QaAgentD0E95E07-QR8zpFzWH5lG", # Replace with your function name
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )

    print(response["Payload"].read().decode("utf-8"))

if __name__ == "__main__":
    invoke_qa_agent()