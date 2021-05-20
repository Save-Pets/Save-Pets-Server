# SAVEPETS
딥러닝을 이용한 강아지 조회 및 등록 비문인식 캡스톤 프로젝트

<h2>주요 기능</h2>

- 강아지 비문 등록  
[등록 api]   
Client에서 비문 사진 5장 전송 -> 서버에서 preprocess 실행 -> 내부적으로 이미 등록된 강아지인지 classification 실행 -> (미등록 강아지일 경우) database에 사용자 및 강아지 정보 등록 client에 성공 message 전달 or (등록되어있는 강아지일경우) client에 이미 등록된 강아지 message 전달

- 강아지 비문 조회  
[조회 api]    
Client에서 비문 사진 1장 전송 -> 서버에서 classification 실행 -> (등록되어있는 강아지 일 경우) database에서 classification 결과값 조회 후 사용자 및 강아지 정보 전달 or (등록되어있지 않은 강아지 일 경우) client에 실패 message 전달

<h2>시연 영상</h2>

<h2>Requirements</h2>
   
Flask 2.0.0  
opencv-contrib-python 3.4.2.16  
opencv-python 3.4.2.16  
scikit-learn 0.24.2  
scipy 1.6.3  
python 3.7.2

<h2>Project Architecture</h2>

<h2>Screenshot</h2>

<h2>Role</h2> 
Name | Main Role
---|---
문수림 | flask 기반 서버,db 개발 및 AWS 배포, 데이터 학습
이해석 | IOS 기반 Swift 앱 개발, 데이터 학습
김종훈 | preprocess ,Classifier modle 개발, 데이터 학습

|이름|role|
|------|---|
|문수림|flask 기반 서버,db 개발 및 AWS 배포,데이터 학습|
|이해석|IOS 기반 Swift 앱 개발, 데이터 학습|
|김종훈|preprocess,Classifier modle 개발,데이터 학습|

