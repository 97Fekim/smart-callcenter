# smart-callcenter
smart-callcenter

## 🔘 소개
### 👍 생성형 AI 모델을 기반으로 고객의 콜센터 상담내역을 분석합니다.
(Amazon Transcribe CallAnayliticsJob 번역작업) -> (Amazon Bedrock 프롬프트작업) -> (DynamoDB)

### 👍 이벤트기반 서버리스 아키텍처로, 서버를 프로비저닝할 필요가 없으며 실행한 만큼만 비용을 지불합니다.
(업로드) -> (S3 Event Notification) -> (Lambda) -> (S3 Even....) ..... -> (DynamoDB)

## 🔘 사용 기술
### 프로그래밍 언어
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=black"> 
### 애플리케이션 및 인프라
<img src="https://img.shields.io/badge/amazon cloudfront-EC1C24?style=for-the-badge&logo=cloudfront&logoColor=black"> <img src="https://img.shields.io/badge/amazon s3-569A31?style=for-the-badge&logo=amazons3&logoColor=black"> <img src="https://img.shields.io/badge/aws lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=black"> <img src="https://img.shields.io/badge/amazon transcribe-68BC71?style=for-the-badge&logo=amazontranscribe&logoColor=black"> <img src="https://img.shields.io/badge/amazon bedrock-68BC71?style=for-the-badge&logo=amazon bedrock&logoColor=black"> <img src="https://img.shields.io/badge/amazon dynamodb-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=black"> 

## 🔘 인프라 아키텍처
<img src="https://github.com/user-attachments/assets/924f0b47-1dd2-4497-8a48-f4a28f5f539f" width=700 height=850 />
