# smart-callcenter
smart-callcenter

## 🔘 소개
### 👍 클라우드 AI 서비스 기반으로 고객의 콜센터 상담분석을 자동화합니다.
![소개_1 0 0](https://github.com/user-attachments/assets/b1687fc3-333e-4749-9456-9f6cccdde68d)

### 👍 이벤트기반 서버리스 아키텍처로, 서버를 프로비저닝할 필요가 없으며 실행한 만큼만 비용을 지불합니다.

![소개_2 0 0](https://github.com/user-attachments/assets/ee6e9996-04d0-4312-8f71-4bf5f60eeb0f)


## 🔘 사용 기술
### 프로그래밍 언어
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=black"> 
### 애플리케이션 및 인프라
<img src="https://img.shields.io/badge/amazon apigateway-FF4F8B?style=for-the-badge&logo=amazonapigateway&logoColor=black"> <img src="https://img.shields.io/badge/amazon cloudfront-EC1C24?style=for-the-badge&logo=cloudfront&logoColor=black"> <img src="https://img.shields.io/badge/amazon s3-569A31?style=for-the-badge&logo=amazons3&logoColor=black"> <img src="https://img.shields.io/badge/aws lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=black"> <img src="https://img.shields.io/badge/amazon transcribe-68BC71?style=for-the-badge&logo=amazontranscribe&logoColor=black"> <img src="https://img.shields.io/badge/amazon bedrock-68BC71?style=for-the-badge&logo=amazon bedrock&logoColor=black"> <img src="https://img.shields.io/badge/amazon dynamodb-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=black"> 

## 🔘 인프라 아키텍처
<img src="https://github.com/user-attachments/assets/b66865df-263e-44cf-ae02-6ef27796525f" width=1200 height=550 />


## 🔘 트러블슈팅 및 배운점
<details>
  <summary>📒 multipart/form-data 요청시 API Gateway에서 발생하는 CORS 문제 </summary>
  <br> 
   o <strong>현상</strong> : 로컬 or S3에서 호스팅되는 HTML에서 API-Gateway로 multipart/form-data 요청을 보낼시, 403-CORS 발생<br><br>
   o <strong>원인</strong> : 이진파일 업로드를 위해, multipart/form-data 요청을 API-Gateway로 보내는 경우 [통합 요청]의 매핑템플릿을 추가해야 하며, [API 설정]의 이진 미디어 형식에 multipart/form-data를 추가해야 한다.<br><br>
   o <strong>해결안</strong> : [통합 요청]의 매핑템플릿을 추가, [API 설정]의 이진 미디어 형식에 multipart/form-data를 추가. <br><br>
</details>

<details>
  <summary>📒 RDB에 비해 통계적 연산이 비교적 취약한 DynamoDB  </summary>
  <br> 
   o <strong>현상</strong> : <br><br>
   o <strong>원인</strong> : <br><br>
   o <strong>해결안</strong> :  <br><br>
</details>
