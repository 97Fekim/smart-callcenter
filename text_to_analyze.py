import datetime
import json
import boto3
import os
import uuid

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'
BEDROCK_REGION_NAME=os.environ.get('BEDROCK_REGION_NAME', 'us-west-2')
SRC_BUCKET_NAME = os.environ.get('SRC_BUCKET_NAME')
TABLE_NAME = os.environ.get('TABLE_NAME')

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=BEDROCK_REGION_NAME
)

table = dynamodb.Table(TABLE_NAME)

system_prompt = """
당신은 은행 콜센터의 상담내역을 분석하고, 몇가지 주요 정보를 도출해내는 임무를 맡았습니다. 
아래에 적혀있는 (1)Input에 관한 설명과 (2)Output에 관한 요구사항 대로 주요 정보를 도출해주세요.
 - (1) Input: AGENT는 은행상담원이며, CUSTOMER는 고객입니다. 두 사람이 번갈아가며 나눈 대화이며, 각 문장의 맨 앞에는 누가 말을 했는지 명시되어 있습니다. (EX = "AGENT: 안녕하세요")
 - (2) Output: 아래에 있는 JSON의 value 부분을 설명에 맞는 단어로 채워서 반환해주세요.
     JSON : {
         "subject" : "상담의 주제 (한 단어)",
         "call_type": "통화 유형 (예: 문의, 불만, 기술 지원 등)",
         "exit_reason" : "상담이 종료된 이유 (한 단어 혹은 간략한 문장)",
         "summary" : "상담 요약 (한 문장)",
         "interest" : "고객의 관심사 (한 단어)",
         "interest_product" : "고객의 관심 상품 (예: 수신, 대출 등)",
         "interest_product_detail" : "고객의 관심 상품 상세 (예: 정기예금, 주택담보대출 등)",
         "keyword" : "통화 중 언급된 주요 키워드 (한 단어)",
         "language" : "사용된 언어(예: ko-KR, en-US 등)",
         "issue_resolved" : "문제 해결 여부 (예: Y or N)",
         "follow_up_required" : "추가 조치 필요 여부 (예: Y or N)",
         "call_transfer_count" : "다른 부서로의 통화 전환 횟수",
         "sentiment_score" : "감정 분석 점수 (예: 긍정적, 중립적, 부정적)"
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
        
        # (5) Put to DynamoDB
        item = {
            'create_date': datetime.datetime.now().strftime('%Y%m%d'),
            'uuid': str(uuid.uuid4()),
            'subject' : analyzed_json['subject'],
            'call_type': analyzed_json['call_type'],
            'exit_reason' : analyzed_json['exit_reason'],
            'summary' : analyzed_json['summary'],
            'interest' : analyzed_json['interest'],
            'interest_product' : analyzed_json['interest_product'],
            'interest_product_detail' : analyzed_json['interest_product_detail'],
            'keyword' : analyzed_json['keyword'],
            'language' : analyzed_json['language'],
            'issue_resolved' : analyzed_json['issue_resolved'],
            'follow_up_required' : analyzed_json['follow_up_required'],
            'call_transfer_count' : analyzed_json['call_transfer_count'],
            'sentiment_score' : analyzed_json['sentiment_score']
        }
        
        try:
            response = table.put_item(Item=item)
            print("PutItem succeeded:")
            print(response)
        except Exception as e:
            print(f"An error occurred: {e}")

            
    # TODO implement
    return {
        'statusCode': 200,
        'body': 'Analyzed Completely!'
    }
