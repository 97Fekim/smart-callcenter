import json
import boto3
import os
import uuid

s3 = boto3.resource('s3')
MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'
BEDROCK_REGION_NAME=os.environ.get('BEDROCK_REGION_NAME', 'us-west-2')
SRC_BUCKET_NAME = os.environ.get('SRC_BUCKET_NAME')

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=BEDROCK_REGION_NAME
)

def lambda_handler(event, context):

    for record in event['Records']:
    
        KEY = record['s3']['object']['key']
        print("================KEY start================")
        print(KEY)
        print("================KEY end================")
        
        object = s3.Object(SRC_BUCKET_NAME, KEY)
        file_content = object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        
        for speech in json_content['Transcript']:
            print(speech['ParticipantRole'] + ": " + speech['Content'])
            print()
            
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
