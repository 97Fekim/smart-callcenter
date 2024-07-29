import json
import boto3
import os
import uuid

s3 = boto3.resource('s3')
BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'
BEDROCK_REGION_NAME=os.environ.get('BEDROCK_REGION_NAME', 'us-west-2')
SRC_BUCKET_NAME = os.environ.get('SRC_BUCKET_NAME')

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=BEDROCK_REGION_NAME
)

system_prompt = """
당신은 은행 콜센터의 상담내역을 분석하고, 몇가지 주요 정보를 도출해내는 임무를 맡았습니다. 
아래에 적혀있는 (1)Input에 관한 설명과 (2)Output에 관한 요구사항 대로 주요 정보를 도출해주세요.
 - (1) Input: AGENT는 은행상담원이며, CUSTOMER는 고객입니다. 두 사람이 번갈아가며 나눈 대화이며, 각 문장의 맨 앞에는 누가 말을 했는지 명시되어 있습니다. (EX = "AGENT: 안녕하세요")
 - (2) Output: 아래에 있는 JSON의 value 부분을 설명에 맞는 단어로 채워서 반환해주세요.
     JSON : {
         SUBJECT : "상담의 주제",
         EXIT_REASON : "상담이 종료된 이유",
         SUMMARY : "상담 요약",
         INTEREST : "고객의 관심사"
     }
"""

def lambda_handler(event, context):

    for record in event['Records']:
    
        # (1) Get Transcribe Text from S3
        KEY = record['s3']['object']['key']
        print("↓↓↓ S3 KEY ↓↓↓")
        print(KEY)
        print("↑↑↑ S3 KEY ↑↑↑")
        
        object = s3.Object(SRC_BUCKET_NAME, KEY)
        file_content = object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        
        # (2) Make Speech Prompt Completely 
        speech_prompt = ""
        for speech in json_content['Transcript']:
            print(speech['ParticipantRole'] + ": " + speech['Content'])
            print()
            
            speech_prompt = speech_prompt + speech['ParticipantRole'] + ": " + speech['Content'] + "\n"
        
        print("↓↓↓ system_prompt ↓↓↓")
        print(system_prompt)
        print("↑↑↑ system_prompt ↑↑↑")
        print("↓↓↓ speech_prompt ↓↓↓")
        print(speech_prompt)
        print("↑↑↑ speech_prompt ↑↑↑")
        
        # (3) Call Bedrock Model
        body = {
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": speech_prompt
    
                        }
                    ]
                }
            ],
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096
        }
        
        response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=json.dumps(body)
        )
        
        # (4) Data Formatting
        response_body = json.loads(response.get('body').read())
        analyzed_raw = response_body['content'][0]['text']
        analyzed_json = json.loads(analyzed_raw)
        
        print("↓↓↓ Analyzed Output (raw) ↓↓↓")
        print(analyzed_raw)
        print("↑↑↑ Analyzed Output (raw) ↑↑↑")
        print("↓↓↓ Analyzed Output (json) ↓↓↓")
        print(analyzed_json)
        print("↑↑↑ Analyzed Output (json) ↑↑↑")
            
    # TODO implement
    return {
        'statusCode': 200,
        'body': 'Analyzed Completely!'
    }
