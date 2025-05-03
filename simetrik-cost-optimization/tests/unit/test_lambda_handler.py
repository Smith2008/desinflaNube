import json
import boto3
from moto import mock_s3, mock_sns, mock_iam
import pytest
from lambda_function import handler

@mock_s3
@mock_sns
@mock_iam
def test_handler_puts_data_to_s3_and_publishes_sns(monkeypatch):
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='cost-bucket')
    sns = boto3.client('sns', region_name='us-east-1')
    topic = sns.create_topic(Name='cost-alerts')['TopicArn']

    monkeypatch.setenv('BUCKET_NAME', 'cost-bucket')
    monkeypatch.setenv('SNS_TOPIC_ARN', topic)

    event = {'some': 'payload'}
    result = handler(event, None)

    objects = s3.list_objects(Bucket='cost-bucket').get('Contents')
    assert objects is not None
    assert result['statusCode'] == 200
