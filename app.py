#!/usr/bin/env python3
import os
import aws_cdk as cdk
from src.common.stack_tags import add_default_tags
from src.networking.networking_stack import NetworkingStack
from src.storage.storage_stack import StorageStack
from src.ingestion.ingestion_stack import IngestionStack
from src.api.api_stack import ApiStack
from src.chat.chatbot_stack import ChatbotStack
from src.auth.auth_stack import AuthStack

app = cdk.App()

# Stacks
networking_stack = NetworkingStack(app, "NetworkingStack")
storage_stack = StorageStack(app, "StorageStack", vpc=networking_stack.vpc)
auth_stack = AuthStack(app, "AuthStack")
ingestion_stack = IngestionStack(
    app, 
    "IngestionStack", 
    vpc=networking_stack.vpc, 
    pdf_bucket=storage_stack.pdf_bucket, 
    opensearch_collection=storage_stack.opensearch_collection,
)
api_stack = ApiStack(app, "ApiStack", vpc=networking_stack.vpc, whatsapp_token_secret=auth_stack.whatsapp_token_secret)
chatbot_stack = ChatbotStack(app, "ChatbotStack", vpc=networking_stack.vpc, opensearch_collection=storage_stack.opensearch_collection, whatsapp_token_secret=auth_stack.whatsapp_token_secret)

# Add tags to all stacks
for stack in [networking_stack, storage_stack, auth_stack, ingestion_stack, api_stack, chatbot_stack]:
    add_default_tags(stack)

app.synth()