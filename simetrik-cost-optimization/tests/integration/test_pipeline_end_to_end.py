import subprocess
import boto3
from moto import mock_s3, mock_sns, mock_ce
import os
import pytest

@mock_s3
@mock_sns
@mock_ce
def test_full_pipeline(tmp_path, monkeypatch):
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='cost-bucket')
    sns = boto3.client('sns', region_name='us-east-1')
    topic = sns.create_topic(Name='cost-alerts')['TopicArn']
    ce = boto3.client('ce', region_name='us-east-1')

    monkeypatch.setenv('BUCKET_NAME', 'cost-bucket')
    monkeypatch.setenv('SNS_TOPIC_ARN', topic)

    result = subprocess.run(['python', 'lambda_function.py'], capture_output=True)
    assert result.returncode == 0

    objs = s3.list_objects(Bucket='cost-bucket').get('Contents')
    assert objs is not None
