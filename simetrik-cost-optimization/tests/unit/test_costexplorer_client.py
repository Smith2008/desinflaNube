import boto3
from botocore.stub import Stubber
import pytest
from costexplorer_client import fetch_cost_data

@pytest.fixture
def costexplorer_stub():
    client = boto3.client('ce', region_name='us-east-1')
    with Stubber(client) as stub:
        yield client, stub

def test_fetch_cost_data(costexplorer_stub):
    client, stub = costexplorer_stub
    expected_params = {
        'TimePeriod': {'Start': '2025-04-01', 'End': '2025-05-01'},
        'Granularity': 'DAILY',
        'Metrics': ['UnblendedCost']
    }
    stub.add_response('GetCostAndUsage', {'ResultsByTime': []}, expected_params)
    data = fetch_cost_data(client, '2025-04-01', '2025-05-01')
    assert isinstance(data, list)
