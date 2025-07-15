import os
import boto3
import time
import json
from aws_lambda_powertools import Logger, Tracer
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

logger = Logger()
tracer = Tracer()

textract = boto3.client("textract")
s3 = boto3.client("s3")

opensearch_endpoint = os.environ["OPENSEARCH_ENDPOINT"]
region = os.environ["AWS_REGION"]

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'aoss', session_token=credentials.token)

opensearch = OpenSearch(
    hosts=[{'host': opensearch_endpoint, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def get_textract_results(job_id):
    pages = []
    next_token = None
    while True:
        kwargs = {"JobId": job_id}
        if next_token:
            kwargs["NextToken"] = next_token
        
        response = textract.get_document_text_detection(**kwargs)
        pages.append(response)
        next_token = response.get("NextToken")
        if not next_token:
            break
    return pages

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']

    logger.info(f"Starting Textract job for {key} from bucket {bucket}")

    response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
    )
    job_id = response["JobId"]

    while True:
        status = textract.get_document_text_detection(JobId=job_id)["JobStatus"]
        if status in ["SUCCEEDED", "FAILED"]:
            break
        time.sleep(5)

    if status == "FAILED":
        logger.error(f"Textract job {job_id} failed.")
        return {"status": "failed"}

    logger.info(f"Textract job {job_id} succeeded. Extracting text.")
    pages = get_textract_results(job_id)
    text = "".join([item['Text'] for page in pages for item in page['Blocks'] if item['BlockType'] == 'LINE'])

    logger.info(f"Indexing document {key} in OpenSearch.")
    chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
    for i, chunk in enumerate(chunks):
        document = {
            "text": chunk,
            "source": key,
            "page": i
        }
        opensearch.index(
            index="proposals",
            body=document,
            id=f"{key}-{i}"
        )

    logger.info(f"Successfully indexed {len(chunks)} chunks for document {key}.")
    return {"status": "success"}