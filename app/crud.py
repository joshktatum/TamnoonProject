import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from fastapi import HTTPException

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name ="us-east-1", aws_access_key_id ="test", aws_secret_access_key ="test")
table = dynamodb.Table('Assets')

def create_asset(asset):
    existing_asset = get_asset(asset['id'])
    if existing_asset:
         raise HTTPException(status_code=400, detail="asset already exists")
    try:
        response = table.put_item(Item=asset)
        return asset # Return the created asset itself
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_assets():
    response = table.scan()
    return response.get('Items', [])

def get_asset(id):
    response = table.get_item(Key={'id': id})
    return response.get('Item', None)
    
def delete_asset(id):
    try:
        response = table.delete_item(Key={'id': id})
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return response

def create_group(group_name, type, tags, cloud_account, owner_id, region):
    response = []
    assets = get_assets()
    for asset in assets:
        asset_tags = {}
        tags_match = True
        for tag in asset['tags']:
            asset_tags[tag['key']] = tag['value']
        for tag in tags:
            if tag.key not in asset_tags.keys() or tag.value != asset_tags[tag.key]:
                tags_match = False
        if( (type is None or asset['type'] == type ) and (owner_id is None or asset['owner_id'] == owner_id) and (region is None or asset['region'] == region)
            and (region is None or asset['region'] == region) and (cloud_account is None or asset['cloud_account'] == cloud_account)
                and tags_match):
            grouped_asset = table.update_item(
                Key={"id": asset['id'],},
                UpdateExpression="set group_name=:g",
                ExpressionAttributeValues={":g": group_name},
                ReturnValues="ALL_NEW",
            )
            response.append(asset)
    return response

def get_assets_by_group(group_name):
    return table.scan(FilterExpression=Attr("group_name").eq(group_name))['Items']
