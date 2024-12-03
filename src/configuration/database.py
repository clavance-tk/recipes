# Dependencies
import boto3

# From apps
from configuration import settings
from configuration.constants import ENDPOINT_URL, TABLE_NAME, Environment


def get_resource(endpoint_url):
    endpoint_url = endpoint_url or ENDPOINT_URL
    return boto3.resource(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name="us-east-1",  # hardcoded for this exercise - use env var e.g. AWS_REGION instead
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )


def resolve_table_name():
    if settings.env == str(Environment.TEST):
        return f"{TABLE_NAME}.test"
    return TABLE_NAME
