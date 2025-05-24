import json
import boto3
from urllib.parse import unquote_plus

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('rekognitionAnalysesDB')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        print(f"Processing: s3://{bucket}/{key}")

        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=10,
            MinConfidence=70
        )
        labels = response['Labels']

        table.put_item(
            Item={
                'ImageID': key,
                'Labels': labels
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Rekognition analysis complete.')
    }
