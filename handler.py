import boto3
import logging
import os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def load_csv(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    logger.info('Loading file {} from {}'.format(file_name, bucket))
    csv_file = s3.get_object(Bucket=bucket, Key=file_name)
    rows = csv_file['Body'].read().decode("utf-8").split('\n')

    for index in range(1, len(rows)):
        values = rows[index].split(',')
        table.put_item(Item={
            'player_ref': values[6],
            'punter_category': values[1],
            'risk_exposure_prematch': values[2],
            'risk_exposure_live': values[3],
            'created_date': values[4],
            'updated_date': values[5],
            'risk_exposure_racing': values[7]
        })
