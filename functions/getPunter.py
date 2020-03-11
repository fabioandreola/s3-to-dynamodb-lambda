import boto3
import logging
import os
import json

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def handler(event, context):
    punter = event['pathParameters']['player_ref']
    result = table.get_item(Key={'player_ref': punter})
    item = result.get('Item', '')

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }

