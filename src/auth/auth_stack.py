from aws_cdk import (aws_secretsmanager as secretsmanager, Stack)
from constructs import Construct

class AuthStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.whatsapp_token_secret = secretsmanager.Secret(self, "WhatsappTokenSecret",
                                                               secret_name="WhatsappBusinessToken")