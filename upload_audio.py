import os
import boto3
import json
import base64

DST_BUCKET_NAME = os.environ.get('DST_BUCKET_NAME')
s3 = boto3.client('s3')

def lambda_handler(event, context):

    print("↓↓ event ↓↓")
    print(event)
    print("↑↑ event ↑↑")
    
    # (1) Get file name
    headers = event.get('headers', {})
    file_name = headers.get('file-name', 'No File Name')
    print("↓↓ file_name ↓↓")
    print(file_name)
    print("↑↑ file_name ↑↑")
    
    # (2) Get file body
    file_body = base64.b64decode(event['body-json'])
    print("↓↓ file_body ↓↓")
    print(file_body)
    print("↑↑ file_body ↑↑")
    
    # (3) Put File to S3
    s3.put_object(Bucket=DST_BUCKET_NAME, Key=file_name, Body=file_body)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Upload Audio successful!')
    }
