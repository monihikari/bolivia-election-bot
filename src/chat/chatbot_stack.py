from aws_cdk import (aws_lambda as _lambda, aws_iam as iam, Stack, CfnOutput, Duration)
from constructs import Construct

class ChatbotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, opensearch_collection, whatsapp_token_secret, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        qa_agent_lambda = _lambda.Function(self, "QaAgent",
                                           runtime=_lambda.Runtime.PYTHON_3_12,
                                           handler="main.handler",
                                           code=_lambda.Code.from_asset("src/chat/lambda",
                                                                       bundling={
                                                                           "image": _lambda.Runtime.PYTHON_3_12.bundling_image,
                                                                           "command": [
                                                                               "bash", "-c",
                                                                               "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                                                                           ]
                                                                       }),
                                           vpc=vpc,
                                           timeout=Duration.seconds(30),
                                           environment={
                                               "OPENSEARCH_ENDPOINT": opensearch_collection.attr_collection_endpoint,
                                               "BEDROCK_MODEL_ID": "amazon.titan-text-express-v1",
                                               "WHATSAPP_TOKEN_SECRET_ARN": whatsapp_token_secret.secret_arn,
                                               "WHATSAPP_PHONE_NUMBER_ID": "YOUR_WHATSAPP_PHONE_NUMBER_ID" # Replace with your WhatsApp Phone Number ID
                                           })

        qa_agent_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["es:ESHttpGet"],
            resources=[opensearch_collection.attr_arn]
        ))
        qa_agent_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        ))
        qa_agent_lambda.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess"))

        self.qa_agent_lambda_name = CfnOutput(self, "QaAgentLambdaFunctionName", value=qa_agent_lambda.function_name)