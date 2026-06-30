# 🔍 다이소-Beauty 탐사대
> **오프라인 다이소 매대에서 스마트폰 링크를 통해 이용 가능한 AI 구매 도우미 시스템**
>  : 소비자가 별도의 프로그램 설치 없이 ¹제품의 품번을 입력하면 실시간 리뷰 분석을 확인할 수 있으며, ²카테고리별 인기 제품을 추천받을 수 있는 모바일 최적화 웹 서비스입니다.

<br>

## 🌐 웹 서비스 바로가기
 하단 링크를 통해 파이썬이 없는 모바일 환경에서도 서비스 체험이 가능합니다.
- **https://daiso-beauty-explorers.streamlit.app/**

<br>

## 📂 파일 구조 및 설명

본 프로젝트는 '사전 구축 데이터(CSV)'와 사용자가 요청할 때 작동하는 '실시간 수집 엔진'이 투트랙으로 연동되는 구조입니다. 

- **`streamlit.py`** : 소비자가 스마트폰으로 접속하는 메인 대시보드 코드
- **`crawling.py`** : 메인 화면의 카테고리별(스킨케어, 선케어, 클렌징, 메이크업) 추천 제품 리스트를 보여주기 위해, 다이소몰의 인기 뷰티 제품 정보를 수집한 사전 데이터 수집 코드
- **`daiso_recommend_data.csv`** : `crawling.py`를 통해 사전에 수집한 다이소 뷰티 제품 정보와 실제 고객 리뷰들이 저장되어 있는 원본 데이터 파일
- **`requirements.txt`** : 웹 서비스 구동에 필요한 파이썬 라이브러리(Streamlit, Selenium, BeautifulSoup4 등) 버전을 정리해 둔 설정 파일
- **`packages.txt`** : 웹 배포 서버에서 크롤링이 에러 없이 작동할 수 있도록, 크롬(Chromium) 브라우저를 자동으로 설치해 주는 설정 파일

<br>

## ⚙️ 시스템 실행 및 분석 과정

### 1. 사전 데이터 구축 단계
- `crawling.py`를 실행하여 다이소몰의 뷰티 카테고리별 주요 제품 정보와 원본 리뷰 데이터를 대량 수집합니다.
- 수집된 데이터는 가공 및 정제 단계를 거쳐 `daiso_recommend_data.csv` 파일로 저장됩니다.

### 2. 사용자 서비스 및 실시간 분석 단계
- 소비자가 웹 링크에 접속하여 오프라인 매대에 있는 제품의 **7자리 품번**을 입력합니다.
- **[경로 A - 기존 데이터 활용]:** 입력된 품번이 사전에 구축된 CSV 데이터셋에 존재할 경우, 즉시 평점 및 카테고리 추천 화면을 띄워줍니다.
- **[경로 B - 실시간 크롤링 엔진 가동]:** 만약 데이터셋에 없는 새로운 품번이 입력되면, 서버 내부의 셀레니움(Selenium)이 실시간으로 해당 다이소몰 상품 페이지에 원격 접속하여 최신 리뷰를 크롤링 합니다.
- 수집된 리뷰는 텍스트 마이닝 알고리즘을 거쳐 규칙 기반(Rule-based) 분석 방식으로 소비자가 한눈에 보기 쉽게 `😊 긍정 키워드`와 `😡 부정 키워드` 순위로 요약 및 시각화되어 화면에 표출됩니다.
  
<br>

## 🛠️ 개발 환경
- **Language:** Python 3.x
- **Libraries:** Streamlit, Pandas, Selenium, BeautifulSoup4, WebDriver Manager, Matplotlib
- **Infrastructure:** GitHub, Streamlit Community Cloud (Linux Server Environments)
- **Libraries:** Streamlit, Pandas, Selenium, BeautifulSoup4, WebDriver Manager, Matplotlib
- **Infrastructure:** GitHub, Streamlit Community Cloud (Linux Server Environments)
