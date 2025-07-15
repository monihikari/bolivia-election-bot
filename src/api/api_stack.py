from aws_cdk import (aws_apigatewayv2 as apigw, aws_lambda as _lambda, Stack)
from constructs import Construct

class ApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, whatsapp_token_secret, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        whatsapp_handler = _lambda.Function(self, "WhatsappHandler",
                                            runtime=_lambda.Runtime.PYTHON_3_12,
                                            handler="main.handler",
                                            code=_lambda.Code.from_asset("src/api/lambda"),
                                            vpc=vpc,
                                            environment={
                                                "WHATSAPP_TOKEN_SECRET_ARN": whatsapp_token_secret.secret_arn
                                            })

        http_api = apigw.CfnApi(self, "WhatsappWebhookApi",
                                name="WhatsappWebhook",
                                protocol_type="HTTP")

        apigw.CfnIntegration(self, "WhatsappIntegration",
                             api_id=http_api.ref,
                             integration_type="AWS_PROXY",
                             integration_uri=whatsapp_handler.function_arn,
                             payload_format_version="2.0")