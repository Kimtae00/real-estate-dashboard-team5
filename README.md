##  real-estate-dashboard

### 프로젝트 소개
- 본 프로젝트는 서울시의 2022년과 2023년 부동산 거래 데이터와 법정동 좌표를 활용하여 재개발이 예상되는 지역을 식별합니다. 이를 통해 식별된 지역을 분석하고 Naver Open Search API를 활용하여 관련된 뉴스 기사를 수집하여 예측 결과를 더 깊이 분석할 수 있도록 구현해보았습니다.
---
### 프로젝트 기간
- 2024년02월02일 ~ 2024년2월08일까지 진행한 미니 프로젝트 입니다 !
<img src="https://github.com/Kimtae00/real-estate-dashboard-team5/blob/main/images/WBS.png"/>

---
### Streamlit Web Application
- 아래는 배포한 **Interactive Real Estate Dashboard** 입니다.
  - [https://real-estate-dashboard-team-5.streamlit.app/](https://real-estate-dashboard-team-5.streamlit.app/)
---
### 팀원 소개
1. [hyelin606](https://github.com/hyelin606)
2. [jianteow](https://github.com/jianteow)
3. [JiHoonYoon00](https://github.com/JiHoonYoon00)
4. [SSUMINIs](https://github.com/SSUMINIs)
5. [Vamos00](https://github.com/Kimtae00)
---
### 데이터셋 출처
- Seoul_data.csv : [서울시 부동산 실거래가 정보](https://data.seoul.go.kr/dataList/OA-21275/S/1/datasetView.do)
- seoul_sig_cd.geojson : [SVG 지리정보](http://www.gisdeveloper.co.kr/?p=2332)
- [전국 법정동 좌표](https://herjh0405.tistory.com/156)
####
      위 데이터셋을 바탕으로 데이터 전처리를 하여 분석에 필요한 추가적인 파일을 생성하여 데이터를 사용하였습니다.
---
### Seoul_data.csv 주요 칼럼
- ACC_YEAR: 접수년도
- SSG_CD: 자치구코드
- SGG_NM: 자치구명
- BJDONG_CD: 법정동코드
- BJDONG_CD: 법정동명
- BLDG_NM: 건물명
- DEAL_YMD: 계약일
- OBJ_AMT: 물건금액
- BLDG_AREA: 건물면적 (m²)
- BUILD_YEAR: 건축년도
- HOUSE_TYPE: 건물용도
- CENTER_LONG: 법정동 기준 경도
- CENTER_LATI: 법정동 기준 위도
- PRICE_PER: 평당 가격 (만원)
---
### 구조
```
├── .devcontainer # 개발 환경 컨테이너 설정
├── .gitignore # Git에서 추적하지 않을 파일 목록 
├── .venv # 가상 환경 설정
│ 
├── data # 데이터 분석에 사용되는 데이터셋 폴더
│ ├── 단독다가구.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '단독다가구'인 데이터
│ ├── 아파트.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '아파트'인 데이터
│ ├── 연립다세대.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '연립다세대'인 데이터
│ ├── 오피스텔.csv # 법정동별 평균 평당가격이 포함된 건물유형(HOUSE_TYPE)이 '오피스텔'인 데이터
│ ├── Seoul_data.csv # 서울시 부동산 실거래 데이터(2022, 2023년)
│ ├── seoul_sig_cd.geojson # 서울시 구역별 지도 데이터
│ └── seoul.geojson # 서울시 지리 데이터
│ 
├── images # 이미지 폴더
│ ├── 재개발 선정 지역.png
│ ├── 서비스 다이어그램.png
│ ├── Open Search API.png
│ ├── API 호출.png
│ ├── WBS.png
│   
├── pages # 스트림릿 페이지 파일
│ ├── 1_1️⃣_노후 건물 분포도.py # 노후 건물 분포도 페이지
│ ├── 2_2️⃣_노후 건물 거래 동향.py # 노후 건물 거래 동향 페이지
│ ├── 3_3️⃣_노후 건물 평당 가격.py # 노후 건물 평당 가격 페이지
│ ├── 4_4️⃣_재개발 부지 선정.py # 재개발 부지 선정 및 선정된 지역의 재개발 관련 뉴스 정보를 가져오는 페이지
│ 
├── app.py # 스트림릿 앱 실행 파일
├── crawling.py # 크롤링 함수가 정의된 파일
│ 
├── requirements.txt # 필요한 파이썬 패키지 목록
└── README.md # 프로젝트 설명 파일
```
---
### 기술 스택
- **Streamlit** : 배포 및 대시보드 개발
- **Naver Open Search API** : 네이버 뉴스 정보 크롤링
- **QGIS** : 지리정보 활용 (v3.34.3)
---
### 라이브러리 소개(requirements.txt)
#### 대시보드 개발
- **streamlit==1.31.0**
#### 데이터 전처리      
- **pandas==2.2.0**
- **numpy==1.26.3**
#### 시각화
- **matplotlib==3.8.2**
- **plotly==5.18.0**
- **pydeck==0.8.1b**
- **geopandas==0.14.3**
#### 크롤링 환경변수 설정  
- **python-dotenv==1.0.1**
#### streamlit 페이지 처리
- **st_pages**
---
### 서비스 다이어그램
- 아래는 서비스 아키텍처를 보여주는 다이어그램입니다.
<img src="https://github.com/Kimtae00/real-estate-dashboard-team5/blob/main/images/%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%8B%A4%EC%9D%B4%EC%96%B4%EA%B7%B8%EB%9E%A8.png"/>

---
### Naver Open Search API
아래는 Open Search API가 호출되는 로직입니다.
#### Concise API Invocation Diagram
<img src="https://github.com/Kimtae00/real-estate-dashboard-team5/blob/main/images/API%20%ED%98%B8%EC%B6%9C.png"/>

---
<p align="center">
   <img src="https://img.shields.io/badge/language-python-blue?style"/>
   <img src="https://img.shields.io/badge/library-streamlit-red?style"/>
   <img src="https://img.shields.io/github/license/maxam2017/productive-box"/>
</p>
