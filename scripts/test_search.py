import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

opensearch_endpoint = os.environ["OPENSEARCH_ENDPOINT"]
region = os.environ.get("AWS_REGION", "us-east-1")

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'aoss', session_token=credentials.token)

opensearch = OpenSearch(
    hosts=[{'host': opensearch_endpoint, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def test_search():
    query = {
        'query': {
            'match_all': {}
        }
    }
    response = opensearch.search(
        body=query,
        index='proposals'
    )
    print(f"Found {response['hits']['total']['value']} documents in the index.")
    print("Sample document:")
    if response['hits']['hits']:
        print(response['hits']['hits'][0]['_source'])

if __name__ == "__main__":
    test_search()