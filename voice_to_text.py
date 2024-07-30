import json
import boto3
import os
import uuid

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

SRC_BUCKET_NAME = os.environ.get('SRC_BUCKET_NAME')
DST_BUCKET_NAME = os.environ.get('DST_BUCKET_NAME')

def lambda_handler(event, context):
    print("▼▼▼ print event start ▼▼▼")
    print(event)
    print("▲▲▲ print event end ▲▲▲")
    
    print("▼▼▼ print context start ▼▼▼")
    print(context)
    print("▲▲▲ print context end ▲▲▲")
    
    for record in event['Records']:
    
        KEY = record['s3']['object']['key']
        print("▼▼▼ KEY start ▼▼▼")
        print(KEY)
        print("▲▲▲ KEY end ▲▲▲")
    
        job_name = str(uuid.uuid4())
        
        transcribe.start_call_analytics_job(
            CallAnalyticsJobName=job_name,
            Media={
                'MediaFileUri': f's3://{SRC_BUCKET_NAME}/{KEY}'
            },
            OutputLocation=f's3://{DST_BUCKET_NAME}/',
            Settings={
                'LanguageOptions': ['ko-KR', 'en-US']
            },
            ChannelDefinitions=[
                {
                    'ChannelId': 0,
                    'ParticipantRole': 'AGENT'
                },
                {
                    'ChannelId': 1,
                    'ParticipantRole': 'CUSTOMER'
                }
            ]
        )
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
