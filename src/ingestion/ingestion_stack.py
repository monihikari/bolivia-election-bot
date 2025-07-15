from aws_cdk import (aws_s3 as s3, aws_lambda as _lambda, aws_s3_notifications as s3n, aws_iam as iam, Stack, aws_events as events, aws_events_targets as targets)
from constructs import Construct

class IngestionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, pdf_bucket, opensearch_collection, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ingestor_lambda = _lambda.Function(self, "PdfIngestor",
                                           runtime=_lambda.Runtime.PYTHON_3_12,
                                           handler="main.handler",
                                           code=_lambda.Code.from_asset("src/ingestion/lambda"),
                                           vpc=vpc,
                                           environment={
                                               "OPENSEARCH_ENDPOINT": opensearch_collection.attr_collection_endpoint
                                           })

        rule = events.Rule(self, "PdfUploadRule",
                             event_pattern={
                                 "source": ["aws.s3"],
                                 "detail_type": ["Object Created"],
                                 "detail": {
                                     "bucket": {
                                         "name": [pdf_bucket.bucket_name]
                                     }
                                 }
                             })
        rule.add_target(targets.LambdaFunction(ingestor_lambda))

        ingestor_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["es:ESHttpPost"],
            resources=[opensearch_collection.attr_arn]
        ))
        ingestor_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["textract:DetectDocumentText"],
            resources=["*"]
        ))