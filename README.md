# SAVEPETS
딥러닝을 이용한 강아지 조회 및 등록 비문인식 캡스톤 프로젝트


### 1. 데모 영상
[데모 영상 보러가기](https://user-images.githubusercontent.com/20268101/120226192-b0571980-c281-11eb-9c59-8288b7d655c1.mp4)

### 2. 서비스 소개

![savepets_main](https://user-images.githubusercontent.com/20268101/120218227-60258a80-c274-11eb-8f81-2abcfc561f43.png)

### 3. 주요 기술 및 설명

#### [Client]
</br>

* **iOS**
  * UIKit
  * GCD (DispatchSemaphore)
  * AVFoundation
  * Vision
  * CoreML

</br>

#### [Backend]
</br>

* **Server**
  * Flask 2.0.0
  * python 3.7.2
  * AWS EC2 - t2.medium
  * Database(MySQL,radis)
  * Celery
* **Machine Learning**
  * opencv-python 3.4.2.16  
  * scikit-learn 0.24.2
  * Pytorch

</br>

#### 1) Backend API 구현 로직 - 등록 
 
- Client에서 비문사진(5장) 전송 -> 서버에서 preprocess 과정-> 5장 중 1장으로 이미 등록된 강아지인지 classification 실행 -> (미등록 강아지일 경우) database에 사용자 및 강아지정보 등록 & client에 "등록 성공" message 전달 or (등록된 강아지일경우) client에 "이미 등록된 강아지" message 전달

- Frontend로 부터 받은 5장의 사진을 EC2 서버에 저장한 후에 classification을 실행하는 로직은 결과값이 Database에 저장되어 있지 않기 때문에 예외가 발생합니다. 따라서 조회를 위한 사진은 따로 미리 저장해놓는 방식을 택했습니다.   

- 이외에도 사용자(부모테이블)가 여러마리의 강아지(자식테이블)를 등록할 수 있기 때문에 사용자의 핸드폰 번호가 database에 등록되어 있는 경우엔 사용자가 이중 등록 되지 않으며 두 테이블은 Foreign key로 연결되어 있습니다.   



 #### 2) Backend API 구현 로직 - 조회

Client에서 비문사진(1장) 전송 -> 서버에서 classification 과정 -> (등록된 강아지일 경우)database에서 고유값 select & client에 사용자 및 강아지정보 전달 or (미등록 강아지일 경우) client에 "미등록 강아지" message 전달
 
- 조회가 성공한 경우엔 uniqueue number를 반환하고 uniqueue number는 "등록된서버시간+등록된강아지이름초성+사용자핸드폰번호뒷자리" 로 만들어지기 때문에 중복되지 않습니다.  

<img width="1214" alt="스크린샷 2021-06-03 오전 12 08 53" src="https://user-images.githubusercontent.com/42709887/120505687-2da89880-c400-11eb-8277-e2dcf05ce060.png">

<img width="1216" alt="스크린샷 2021-06-03 오전 12 11 18" src="https://user-images.githubusercontent.com/42709887/120505767-3f8a3b80-c400-11eb-8f22-6d12c4098891.png">



#### 3) Backend API 구현 로직 - 동시성 프로그래밍 & 비동기 작업 큐

Flask는 프로세스를 동기적(Synchronous)으로 처리하기 때문에 사용자 요청(HTTP)에 무거운 연산(머신러닝 classification)이 포함되어있는 경우 웹 서버의 처리가 모두 마무리될 때까지 기다려야 합니다. 
등록, 조회 API가 동시 호출 되는 경우를 처리하기 위해 비동기 작업 큐 라이브러리 celery 사용했습니다. 

[Flask + Celery + redis]의 전반적인 아키텍처
- Celery Client : 백그라운드 작업을 요청하는데 사용합니다
- Celery Workers : Flask와 동일한 서버에서 백그라운드 작업을 실행하는데 사용합니다
- Message Broker :in-memory 데이터 저장 장치인 redis를 메시지 브로커 용도로 사용합니다

<img width="839" alt="스크린샷 2021-06-03 오전 12 10 10" src="https://user-images.githubusercontent.com/42709887/120505637-208ba980-c400-11eb-81b3-33a9e59952e4.png">


### 4. UI/UX

#### 1) 비문 등록하기 (카메라/앨범선택)

|                                                              |                                                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![120216339-dbd20800-c271-11eb-80ee-12759a44ca35](https://user-images.githubusercontent.com/20268101/120216339-dbd20800-c271-11eb-80ee-12759a44ca35.png) | ![120221033-aaa90600-c278-11eb-8faa-5c04c2d6423c](https://user-images.githubusercontent.com/20268101/120221033-aaa90600-c278-11eb-8faa-5c04c2d6423c.png) | ![120216337-db397180-c271-11eb-9bba-159e554b4b57](https://user-images.githubusercontent.com/20268101/120216337-db397180-c271-11eb-9bba-159e554b4b57.png) |
| ![120222169-7cc4c100-c27a-11eb-8829-cb0041a7523e](https://user-images.githubusercontent.com/20268101/120222169-7cc4c100-c27a-11eb-8829-cb0041a7523e.png) | ![120216333-daa0db00-c271-11eb-8731-f9aac8700b00](https://user-images.githubusercontent.com/20268101/120216333-daa0db00-c271-11eb-8731-f9aac8700b00.png) |                                                              |
| ![120221032-a977d900-c278-11eb-90d1-5e506d9698e2](https://user-images.githubusercontent.com/20268101/120221032-a977d900-c278-11eb-90d1-5e506d9698e2.png) | ![120221031-a8df4280-c278-11eb-9006-e3f1b7b130b9](https://user-images.githubusercontent.com/20268101/120221031-a8df4280-c278-11eb-9006-e3f1b7b130b9.png) | ![120221025-a7ae1580-c278-11eb-9304-5273ac9b0523](https://user-images.githubusercontent.com/20268101/120221025-a7ae1580-c278-11eb-9304-5273ac9b0523.png) |
| ![120221008-a2e96180-c278-11eb-8ee0-fdcbd3a0805c](https://user-images.githubusercontent.com/20268101/120221008-a2e96180-c278-11eb-8ee0-fdcbd3a0805c.png) | ![120216326-da084480-c271-11eb-86f6-ea12f123956b](https://user-images.githubusercontent.com/20268101/120216326-da084480-c271-11eb-86f6-ea12f123956b.png) | ![120216323-d83e8100-c271-11eb-91b8-5e93db02a112](https://user-images.githubusercontent.com/20268101/120216323-d83e8100-c271-11eb-91b8-5e93db02a112.png) |
| ![120216311-d379cd00-c271-11eb-8aad-ccb193881ea1](https://user-images.githubusercontent.com/20268101/120216311-d379cd00-c271-11eb-8aad-ccb193881ea1.png) | ![120216353-deccf880-c271-11eb-8170-25b6087b977d](https://user-images.githubusercontent.com/20268101/120216353-deccf880-c271-11eb-8170-25b6087b977d.png) | ![120221828-058f2d00-c27a-11eb-8db7-3517c4f582b6](https://user-images.githubusercontent.com/20268101/120221828-058f2d00-c27a-11eb-8db7-3517c4f582b6.png) |



#### 2) 비문 조회하기 (카메라/앨범선택)

|                                                              |                                                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![120216339-dbd20800-c271-11eb-80ee-12759a44ca35](https://user-images.githubusercontent.com/20268101/120216339-dbd20800-c271-11eb-80ee-12759a44ca35.png) | ![120221926-29eb0980-c27a-11eb-8ac1-adf1483d1f54](https://user-images.githubusercontent.com/20268101/120221926-29eb0980-c27a-11eb-8ac1-adf1483d1f54.png) | ![120222169-7cc4c100-c27a-11eb-8829-cb0041a7523e](https://user-images.githubusercontent.com/20268101/120222169-7cc4c100-c27a-11eb-8829-cb0041a7523e.png) |
| ![120216325-d96fae00-c271-11eb-987d-d46f2f4755d6](https://user-images.githubusercontent.com/20268101/120216325-d96fae00-c271-11eb-987d-d46f2f4755d6.png) | ![120221937-2eafbd80-c27a-11eb-83df-81017923a218](https://user-images.githubusercontent.com/20268101/120221937-2eafbd80-c27a-11eb-83df-81017923a218.png) |                                                              |
| ![120216334-db397180-c271-11eb-94e2-da8e3977df19](https://user-images.githubusercontent.com/20268101/120216334-db397180-c271-11eb-94e2-da8e3977df19.png) | ![120216330-da084480-c271-11eb-926e-e55d350b4a5e](https://user-images.githubusercontent.com/20268101/120216330-da084480-c271-11eb-926e-e55d350b4a5e.png) | ![120222091-60288900-c27a-11eb-9ea8-89e6f25641db](https://user-images.githubusercontent.com/20268101/120222091-60288900-c27a-11eb-9ea8-89e6f25641db.png) |




### 5. ROLE

|이름|role|
|------|---|
|문수림|flask 기반 서버,db 개발 및 AWS 배포,데이터 학습|
|이해석|IOS 기반 Swift 앱 개발, 데이터 학습|
|김종훈|preprocess,Classifier model 개발,데이터 학습|

