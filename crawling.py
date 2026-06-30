# crawling.py
# 실행: python crawling.py

import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

PRODUCTS = [
    # ── 스킨케어 (원하는 제품 4개 입력) ──
    {"카테고리": "스킨케어", "세부항목": "None", "제품명": "VT 리들샷 100 페이셜 부스팅 퍼스트 앰플 2 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1049275&recmYn=N"},
    {"카테고리": "스킨케어", "세부항목": "None", "제품명": "마데카21 테카 솔루션 수딩 미스트 토너 200 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1044553&recmYn=N"},
    {"카테고리": "스킨케어", "세부항목": "None", "제품명": "본셉 비타씨 동결 건조 더블샷 앰플 키트", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1061918&recmYn=N"},
    {"카테고리": "스킨케어", "세부항목": "None", "제품명": "VT PDRN 광채 토너 200 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1067495&recmYn=N"},

    # ── 선케어 (원하는 제품 4개 입력) ──
    {"카테고리": "선케어", "세부항목": "None", "제품명": "더마블록 마일드 선스틱 16 g", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1055374&recmYn=N"},
    {"카테고리": "선케어", "세부항목": "None", "제품명": "VT PDRN 광채 선 에센스 50 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1067497&recmYn=N"},
    {"카테고리": "선케어", "세부항목": "None", "제품명": "과일나라 알로에베라 모이스처 아쿠아 수딩 선 에센스 50 g", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1046401&recmYn=N"},
    {"카테고리": "선케어", "세부항목": "None", "제품명": "비프루프 마린 무기자차 마일드 선크림 50 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1045146&recmYn=N"},

    # ── 클렌징 (원하는 제품 4개 입력) ──
    {"카테고리": "클렌징", "세부항목": "None", "제품명": "메디필 엑스트라 슈퍼 9 플러스 아크네 클렌징 폼 100 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1053481&recmYn=N"},
    {"카테고리": "클렌징", "세부항목": "None", "제품명": "바세린 모이스처라이징 클렌징 밀크 140 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1060211&recmYn=N"},
    {"카테고리": "클렌징", "세부항목": "None", "제품명": "약산성 ph클렌징 폼 150 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1035081&recmYn=N"},
    {"카테고리": "클렌징", "세부항목": "None", "제품명": "BRTC 스킨 랩 퓨리파잉 클렌징 오일 100 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1051352&recmYn=N"},

    # ── 메이크업 - 베이스(쿠션/파우더) ──
    {"카테고리": "메이크업", "세부항목": "베이스(쿠션/파우더)", "제품명": "입큰 퍼스널 톤 코렉팅 블러 팩트 5.5 g(라벤더)", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1061379&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "베이스(쿠션/파우더)", "제품명": "태그 벨벳 커버 쿠션 15 g 페일 라이트", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1045418&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "베이스(쿠션/파우더)", "제품명": "줌 바이 정샘물 세범다운 쿠션", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1072800&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "베이스(쿠션/파우더)", "제품명": "[21호 엔라이트]줌 바이 정샘물 새틴핏 스파츌라 파운데이션 25 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1072797&recmYn=N"},

    # ── 메이크업 - 아이(라이너/브로우/섀도우) ──
    {"카테고리": "메이크업", "세부항목": "아이(라이너/브로우/섀도우)", "제품명": "태그 슬림브로우펜슬(2호_애쉬브라운)", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1045431&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "아이(라이너/브로우/섀도우)", "제품명": "머지 렛츠 픽싱 펜 아이라이너 브라우니", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1060128&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "아이(라이너/브로우/섀도우)", "제품명": "[72 리틀 오스틴]프릴루드 딘토 노스탈지아 아이 팔레트", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1061139&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "아이(라이너/브로우/섀도우)", "제품명": "플레이 101 바이 에뛰드 엣지 컬 틴트 마스카라 블랙", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1061829&recmYn=N"},

    # ── 메이크업 - 립(틴트/립밤) ──
    {"카테고리": "메이크업", "세부항목": "립(틴트/립밤)", "제품명": "오릭스 모이스처 립밤 4.8 g 무향", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1035214&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "립(틴트/립밤)", "제품명": "손앤박 아티 스프레드 컬러 밤(03 멜로우)", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1048918&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "립(틴트/립밤)", "제품명": "[03 로즈티커] 본셉 립 타투 스티커", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1065359&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "립(틴트/립밤)", "제품명": "[21 이브닝 로즈]프릴루드 딘토 라벨르 로즈 플럼핑 립틴트", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1061152&recmYn=N"},

    # ── 메이크업 - 블러셔 ──
    {"카테고리": "메이크업", "세부항목": "블러셔", "제품명": "입큰 퍼스널 톤 쿠션 블러셔 핑크 슈", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1062774&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "블러셔", "제품명": "태그 무드블러쉬빔(2호_페어모브) 9 g", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1045425&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "블러셔", "제품명": "[솔티드 베리]입큰 퍼스널 누베어 파우더 블러셔", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1078727&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "블러셔", "제품명": "[61 베이비 로즈]프릴루드 딘토 라벨르로즈 리퀴드치크 10 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1071673&recmYn=N"},

    # ── 메이크업 - 기타 ──
    {"카테고리": "메이크업", "세부항목": "기타", "제품명": "줌 바이 정샘물 메이크업 픽서 50 ml", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1072801&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "기타", "제품명": "그로우어스 롱래스팅 클리어 앤 틴팅 2IN1 래쉬세럼", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1062738&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "기타", "제품명": "립 슬리핑 마스크 베리", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1050179&recmYn=N"},
    {"카테고리": "메이크업", "세부항목": "기타", "제품명": "투에딧 바이 루나 컨투어링 쉐딩 멀티 스틱(02 쿨스텝)", "url": "https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo=1060660&recmYn=N"},
]

MAX_REVIEWS = 30


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,1000")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def extract_product_id(url):
    match = re.search(r"pdNo=(\d+)", url)
    return match.group(1) if match else "Unknown"


def crawl_product(prod, driver):
    url = prod["url"]
    if "실제URL입력" in url or not url.strip():
        print(f"[건너뜀] {prod['제품명']} - URL 없음")
        return []

    product_id = extract_product_id(url)
    print(f"[수집 중] {prod['제품명']} (품번: {product_id})")

    reviews = []
    try:
        driver.get(url)
        time.sleep(3.0)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 1. 가격 추출 보완
        price_el = soup.select_one(".price .num") or soup.select_one(".price_box .num") or soup.select_one(
            "[class*='price'] .num")
        price = price_el.get_text(strip=True) + "원" if price_el else "3,000원"

        # 2. 이미지 주소 추출 보완 (대표 썸네일 매칭)
        img_el = soup.select_one(".product-img img") or soup.select_one(".swiper-slide-active img") or soup.select_one(
            ".view-thumb img")
        img_url = ""
        if img_el and img_el.has_attr("src"):
            img_url = img_el["src"]
        elif img_el and img_el.has_attr("data-src"):
            img_url = img_el["data-src"]

        if img_url.startswith("//"):
            img_url = "https:" + img_url

        # 리뷰 탭 전환
        for xp in ['//button[contains(text(),"리뷰")]', '//button[contains(text(),"후기")]', '//*[@id="tabReview"]']:
            try:
                el = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].click();", el)
                time.sleep(1.5)
                break
            except:
                continue

        page = 1
        while len(reviews) < MAX_REVIEWS:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.select("li.review-detail")
            if not items: break

            for item in items:
                if len(reviews) >= MAX_REVIEWS: break
                text_el = item.select_one(".review-desc .cont span") or item.select_one(".cont")
                text = text_el.get_text(strip=True) if text_el else ""

                score_el = item.select_one(".hiddenText") or item.select_one(".score")
                score_raw = score_el.get_text(strip=True) if score_el else ""
                score_num = int(re.findall(r"\d+", score_raw)[0]) if re.findall(r"\d+", score_raw) else 5

                if text.strip():
                    reviews.append({
                        "품번": str(product_id),
                        "카테고리": prod["카테고리"],
                        "세부항목": prod["세부항목"],
                        "제품명": prod["제품명"],
                        "리뷰내용": text,
                        "별점": score_num,
                        "가격": price,
                        "이미지": img_url,
                        "링크": url
                    })

            try:
                btn = driver.find_element(By.XPATH,
                                          f'//ul[contains(@class,"el-pager")]//li[contains(@class,"number") and normalize-space(text())="{page + 1}"]')
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.2)
                page += 1
            except:
                break
    except Exception as e:
        print(f"[에러] {prod['제품명']} 수집 실패: {e}")

    return reviews


if __name__ == "__main__":
    driver = get_driver()
    all_data = []
    try:
        for p in PRODUCTS:
            all_data.extend(crawl_product(p, driver))
    finally:
        driver.quit()

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("daiso_recommend_data.csv", index=False, encoding="utf-8-sig")
        print(f"\n[완료] {len(df)}개 리뷰 저장 완료.")