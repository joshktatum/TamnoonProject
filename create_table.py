import boto3
import time
dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name ="us-east-1", aws_access_key_id ="test", aws_secret_access_key ="test")
try:
    try:
        table = dynamodb.delete_table(TableName='Assets')
    except Exception as e:
        pass
    time.sleep(2)
    table = dynamodb.create_table(
    TableName='Assets',
    KeySchema=[
    {
    'AttributeName': 'id',
    'KeyType': 'HASH'
    }
    ],
    AttributeDefinitions=[
    {
    'AttributeName': 'id',
    'AttributeType': 'S'
    }
    ],
    ProvisionedThroughput={
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits': 5
    }
    )
    print("Table status:", table["TableDescription"]['TableStatus'])
except Exception as e:
    print('error', e)