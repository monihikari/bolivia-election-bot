from aws_cdk import (aws_s3 as s3, aws_opensearchserverless as opensearch, Stack)
from constructs import Construct

class StorageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.pdf_bucket = s3.Bucket(self, "PdfPropuestasBucket",
                                     event_bridge_enabled=True)

        self.opensearch_collection = opensearch.CfnCollection(self, "ProposalCollection",
                                                               name="proposals",
                                                               type="VECTORSEARCH",
                                                               description="Stores vector embeddings of presidential proposals.")

        security_policy = opensearch.CfnSecurityPolicy(self, "ProposalCollectionSecurityPolicy",
                                     name="proposals-security-policy",
                                     type="encryption",
                                     policy="{\"Rules\":[{\"ResourceType\":\"collection\",\"Resource\":[\"collection/proposals\"]}],\"AWSOwnedKey\":true}")

        self.opensearch_collection.add_dependency(security_policy)