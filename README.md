# 🔍 다이소-Beauty 탐사대 (Daiso Beauty Explorers)

> **오프라인 다이소 매대에서 스마트폰 링크를 통해 이용 가능한 AI 구매 도우미 시스템**
> 소비자가 별도의 프로그램 설치 없이 웹 링크 접속만으로 화장품 품번을 입력하면, 실시간으로 리뷰를 수집하고 AI 기반의 긍정/부정 핵심 키워드 및 종합 평점을 분석해 주는 모바일 최적화 웹 서비스입니다.

<br>

## 🌐 서비스 바로가기 (Web Deployment)
 아래 링크를 클릭하시면 파이썬 환경이 없는 모바일 및 웹 환경에서도 즉시 서비스를 체험하실 수 있습니다.
- **[👉 다이소-Beauty 탐사대 웹 서비스 접속하기]- https://daiso-beauty-explorers.streamlit.app/**

<br>

## 📂 파일 구조 및 설명 (File Structure)

본 프로젝트는 데이터 수집(Back-end)과 데이터 시각화/서비스(Front-end)가 투트랙으로 연동되는 구조로 설계되었습니다.

- **`streamlit.py`** : 소비자가 스마트폰으로 접속하는 메인 대시보드 애플리케이션 소스 코드입니다. 로컬 데이터에 없는 품번이 입력될 경우, 백그라운드에서 실시간으로 다이소몰을 크롤링하여 분석하는 '실시간 수집 엔진'이 내장되어 있습니다.
- **`crawling.py`** : 서비스 초기 적재 및 카테고리별(스킨케어, 선케어, 클렌징, 메이크업) 추천 데이터를 구축하기 위해 다이소몰 베스트 화장품 데이터를 대량 수집한 초기 크롤러 코드입니다.
- **`daiso_recommend_data.csv`** : `crawling.py`를 통해 사전 수집된 다이소 뷰티 제품 및 실시간 리뷰 마스터 데이터셋입니다.
- **`requirements.txt`** : 서비스 구동에 필요한 파이썬 라이브러리(Streamlit, Selenium, BeautifulSoup4 등) 의존성 설정 파일입니다.
- **`packages.txt`** : 클라우드 가상 리눅스 서버 환경에서 크롤러가 작동할 수 있도록 크롬(Chromium) 브라우저 환경을 설치해 주는 시스템 패키지 설정 파일입니다.

<br>

## ⚙️ 시스템 실행 및 분석 과정 (Execution Flow)

### 1. 사전 데이터 적재 단계 (Data Scraping)
- 관리자가 `crawling.py`를 실행하여 다이소몰의 뷰티 카테고리별 주요 제품 정보와 원본 리뷰 데이터를 대량 수집합니다.
- 수집된 데이터는 가공 및 정제 단계를 거쳐 `daiso_recommend_data.csv` 파일로 저장됩니다.

### 2. 사용자 서비스 및 실시간 분석 단계 (On-Demand Service)
- 소비자가 웹 링크에 접속하여 오프라인 매대에 있는 제품의 **7자리 품번**을 입력합니다.
- **[경로 A - 기존 데이터 활용]:** 입력된 품번이 사전에 구축된 CSV 데이터셋에 존재할 경우, 즉시 평점 및 카테고리 추천 화면을 띄워줍니다.
- **[경로 B - 실시간 크롤링 엔진 가동]:** 만약 가이드에 없는 신상품이나 새로운 품번이 입력되면, 서버 내부의 셀레니움(Selenium)이 실시간으로 해당 다이소몰 상품 페이지에 원격 접속하여 최신 리뷰를 실시간 크롤링 합니다.
- 수집된 리뷰는 텍스트 마이닝 알고리즘을 거쳐 규칙 기반(Rule-based) 분석 방식으로 소비자가 한눈에 보기 쉽게 `😊 긍정 키워드`와 `😡 부정 키워드` 순위로 요약 및 시각화되어 화면에 표출됩니다.
- **Language:** Python 3.x
- **Libraries:** Streamlit, Pandas, Selenium, BeautifulSoup4, WebDriver Manager, Matplotlib
- **Infrastructure:** GitHub, Streamlit Community Cloud (Linux Server Environments)
