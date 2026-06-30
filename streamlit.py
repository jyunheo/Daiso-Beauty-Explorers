# dashboard.py
# 실행: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import platform
import matplotlib
import re
import time
from collections import Counter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

if platform.system() == "Windows":
    matplotlib.rc("font", family="Malgun Gothic")
else:
    matplotlib.rc("font", family="AppleGothic")

CONFIG_DYNAMIC = {
    "메이크업": {
        "세부항목": ["베이스(쿠션/파우더)", "아이(라이너/브로우/섀도우)", "립(틴트/립밤)", "블러셔", "기타"]
    }
}
RECOMMEND_DATA_PATH = "daiso_recommend_data.csv"

# 제공된 고정 가격 및 이미지 매핑 데이터
FIXED_DATA_MAP = {
    "1049275": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20251226/thumbnail/850/wfjY4E205mScTabgox171049275_00_02wfjY4E205mScTabgox17.jpg"
    },
    "1044553": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260402/thumbnail/850/YAGyPq2hshglHl0qRLSj1044553_00_00YAGyPq2hshglHl0qRLSj.jpg"
    },
    "1061918": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20251216/thumbnail/850/lcOc1IVBETy66kefZV8g1061918_00_00lcOc1IVBETy66kefZV8g.jpg"
    },
    "1067495": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250929/thumbnail/850/ne9YHnao1D592hc9xmCp1067495_00_01ne9YHnao1D592hc9xmCp.jpg"
    },
    "1055374": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20240510/thumbnail/850/wTSEmHZQH0IdkA4Xfwv31055374_00_00wTSEmHZQH0IdkA4Xfwv3.jpg"
    },
    "1067497": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250929/thumbnail/850/wzKrzwRCrDqgHZDTtgId1067497_00_01wzKrzwRCrDqgHZDTtgId.jpg"
    },
    "1046401": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260402/thumbnail/850/2IpLkeG3fNXZq404dbN11046401_00_002IpLkeG3fNXZq404dbN1.jpg"
    },
    "1045146": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250425/thumbnail/850/ATDev4SQOg7J1IEOb9j01045146_00_01ATDev4SQOg7J1IEOb9j0.jpg"
    },
    "1053481": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20251202/thumbnail/850/1mjpgiOTWenoGikEKnWR1053481_00_001mjpgiOTWenoGikEKnWR.jpg"
    },
    "1060211": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250311/thumbnail/850/QGjtoQh4Tv8bUcOEAchc1060211_00_01QGjtoQh4Tv8bUcOEAchc.jpg"
    },
    "1035081": {
        "가격": "2,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260402/thumbnail/850/ewBB1X1rZgg7uZRMr0BN1035081_00_00ewBB1X1rZgg7uZRMr0BN.jpg"
    },
    "1051352": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20240226/thumbnail/850/1XsEg25kgvetjWRCChuz1051352_00_011XsEg25kgvetjWRCChuz.jpg"
    },
    "1061379": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260429/thumbnail/850/bGFIVFEuZgWQyFhqVlsV1061379_00_00bGFIVFEuZgWQyFhqVlsV.jpg"
    },
    "1045418": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20231221/thumbnail/850/Zg9ux7ZMCZ6Ov0rBe8Os1045418_00_00Zg9ux7ZMCZ6Ov0rBe8Os.jpg"
    },
    "1072800": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260105/thumbnail/850/BBuw9crU6REV3VrtkYez1072800_00_00BBuw9crU6REV3VrtkYez.jpg"
    },
    "1072797": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260105/thumbnail/850/SxEzOnwteyNgbunLlymG1072797_00_00SxEzOnwteyNgbunLlymG.jpg"
    },
    "1045431": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20251223/thumbnail/850/qWbO1PJcLHiHmOFQM6yk1045431_00_00qWbO1PJcLHiHmOFQM6yk.jpg"
    },
    "1060128": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20240926/thumbnail/850/7QzvV8hzLiWLNEV1KuxS1060128_00_007QzvV8hzLiWLNEV1KuxS.jpg"
    },
    "1061139": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250312/thumbnail/850/6H3CrEYp1l166967geId1061139_00_016H3CrEYp1l166967geId.jpg"
    },
    "1061829": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260219/thumbnail/850/fZbjRv9oMmVM6OAxwqyQ1061829_00_01fZbjRv9oMmVM6OAxwqyQ.jpg"
    },
    "1035214": {
        "가격": "1,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260402/thumbnail/850/JxYTukxbjvSEWoF90nzn1035214_00_02JxYTukxbjvSEWoF90nzn.jpg"
    },
    "1048918": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20251002/thumbnail/850/mHdYniGIMGrfsIXctJBy1048918_00_00mHdYniGIMGrfsIXctJBy.png"
    },
    "1065359": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260526/thumbnail/850/iMauCXCd7PkTk11CC3p51065359_00_01iMauCXCd7PkTk11CC3p5.jpg"
    },
    "1061152": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250117/thumbnail/850/3iTaiosCVyoHmRlLVCJz1061152_00_013iTaiosCVyoHmRlLVCJz.jpg"
    },
    "1062774": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260429/thumbnail/850/0NZoK4Fy94Ipwf6v6vjt1062774_00_000NZoK4Fy94Ipwf6v6vjt.jpg"
    },
    "1045425": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20240105/thumbnail/850/kThjIRfXVuzSRj1guQyp1045425_00_00kThjIRfXVuzSRj1guQyp.jpg"
    },
    "1078727": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260429/thumbnail/850/iZQnHiR5VA7hbvggY36Y1078727_00_00iZQnHiR5VA7hbvggY36Y.jpg"
    },
    "1071673": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20251015/thumbnail/850/5Nq7h5eipVzId9eFfPmh1071673_00_015Nq7h5eipVzId9eFfPmh.jpg"
    },
    "1072801": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20260105/thumbnail/850/9rYrrTDuGuXh7DvCAhJc1072801_00_009rYrrTDuGuXh7DvCAhJc.jpg"
    },
    "1062738": {
        "가격": "5,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250417/thumbnail/850/EpU35rZfDPqmhkGvkCBS1062738_00_04EpU35rZfDPqmhkGvkCBS.jpg"
    },
    "1050179": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20240610/thumbnail/850/cAbduotDWReg1aBrtSbH1050179_00_00cAbduotDWReg1aBrtSbH.jpg"
    },
    "1060660": {
        "가격": "3,000원",
        "이미지": "https://cdn.daisomall.co.kr/file/resize/PD/20250617/thumbnail/850/XiadbV2aMw2m5yEQSohB1060660_00_03XiadbV2aMw2m5yEQSohB.jpg"
    },
}


def crawl_realtime_on_demand(product_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo={product_id}"
    reviews = []

    try:
        driver.get(url)
        time.sleep(2.5)

        for xp in ['//button[contains(text(),"리뷰")]', '//button[contains(text(),"후기")]']:
            try:
                el = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].click();", el)
                time.sleep(1.2)
                break
            except:
                continue

        for _ in range(2):
            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.select("li.review-detail")
            if not items: break
            for item in items:
                text_el = item.select_one(".review-desc .cont span")
                text = text_el.get_text(strip=True) if text_el else ""
                score_el = item.select_one(".hiddenText")
                score_raw = score_el.get_text(strip=True) if score_el else ""
                score_num = int(re.findall(r"\d+", score_raw)[0]) if re.findall(r"\d+", score_raw) else 5
                if text.strip():
                    mapped_price = FIXED_DATA_MAP.get(str(product_id), {}).get("가격", "가격 확인 불가")
                    mapped_img = FIXED_DATA_MAP.get(str(product_id), {}).get("이미지", "")
                    reviews.append({
                        "품번": str(product_id), "카테고리": "임시", "세부항목": "None", "제품명": f"조회 제품({product_id})",
                        "리뷰내용": text, "별점": score_num, "가격": mapped_price, "이미지": mapped_img, "링크": url
                    })
            try:
                btn = driver.find_element(By.XPATH, '//button[contains(@class,"btn-next")]')
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.0)
            except:
                break
    except:
        pass
    finally:
        driver.quit()
    return pd.DataFrame(reviews)


@st.cache_data
def load_recommend_data():
    try:
        df = pd.read_csv(RECOMMEND_DATA_PATH, encoding="utf-8-sig")
        df["품번"] = df["품번"].astype(str).str.strip()

        for idx, row in df.iterrows():
            pid = str(row["품번"])
            if pid in FIXED_DATA_MAP:
                df.at[idx, "가격"] = FIXED_DATA_MAP[pid]["가격"]
                df.at[idx, "이미지"] = FIXED_DATA_MAP[pid]["이미지"]
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def split_and_analyze_sentences_strict(df):
    perfect_satisfaction = []
    reference_tips = []

    pos_keywords = ["순하", "순해", "세정", "지워", "촉촉", "보습", "진정", "좋", "만족", "재구매"]
    neg_keywords = ["트러블", "안지워", "따가", "붉어", "자극", "건조", "당김", "아쉽", "부족"]
    quality_keywords = ["피부", "제형", "효과", "바르면", "흡수", "화장", "밀착", "발색", "향도", "성분"]

    for _, row in df.iterrows():
        sentences = re.split(r'[.!?\n~]+', str(row["리뷰내용"]))
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 18: continue

            p_score = sum(1 for kw in pos_keywords if kw in sentence)
            n_score = sum(1 for kw in neg_keywords if kw in sentence)
            q_score = sum(1 for kw in quality_keywords if kw in sentence)

            if row["별점"] == 5 and p_score > 0 and n_score == 0:
                if not any(stop in sentence for stop in ["안 ", "못 ", "않", "다만"]):
                    if q_score > 0:
                        perfect_satisfaction.insert(0, sentence)
                    else:
                        perfect_satisfaction.append(sentence)
            elif n_score > 0 or row["별점"] <= 3 or any(tip in sentence for tip in ["다만", "사용 팁", "바를 때"]):
                reference_tips.append(sentence)

    return list(dict.fromkeys(perfect_satisfaction)), list(dict.fromkeys(reference_tips))


def get_clean_keywords(df):
    text_pool = " ".join(df["리뷰내용"].dropna().astype(str).tolist())
    candidates = ["촉촉함", "보습력", "저자극", "순함", "세정력", "커버력", "지속력", "밀착력", "발색력", "발림성", "가성비"]
    found = [(cand, text_pool.count(cand[:2])) for cand in candidates if text_pool.count(cand[:2]) > 0]
    found = sorted(found, key=lambda x: x[1], reverse=True)
    return found[0][0] if found else "종합 사용감 우수"


def get_ranked_keywords_fixed(sentences, mode="장점"):
    extracted_words = []
    for text in sentences:
        if mode == "장점":
            if any(k in text for k in ["순하", "순해", "저자극"]): extracted_words.append("순함/저자극")
            if any(k in text for k in ["촉촉", "보습"]): extracted_words.append("촉촉함/보습력 우수")
            if any(k in text for k in ["세정", "잘지워"]): extracted_words.append("우수한 세정력")
        else:
            if any(k in text for k in ["트러블", "여드름"]): extracted_words.append("트러블/여드름 유발 우려")
            if any(k in text for k in ["건조", "당김"]): extracted_words.append("사용 후 건조함/보습력 부족")
            if "자극" in text or "따가" in text: extracted_words.append("피부 자극 및 따가움")

    counted = Counter(extracted_words).most_common(5)
    result = [item[0] for item in counted]
    return result


def convert_rating_to_stars(score):
    if pd.isna(score): return "☆☆☆☆☆ (0점)"
    rounded = round(score, 2)
    return f"{'★' * int(rounded)}{'☆' * (5 - int(rounded))} ({rounded} / 5.0)"


def render_quality_verification(df):
    st.subheader("궁금한 제품의 품번을 입력하세요")
    product_id = st.text_input("품번 입력", placeholder="예시: 1053481").strip()

    if st.button("초고속 품질 조회"):
        if not product_id: return

        target_df = df[df["품번"] == product_id] if not df.empty else pd.DataFrame()

        if target_df.empty:
            with st.spinner("로컬 데이터 파일에 존재하지 않는 품번입니다. 실시간 수집 엔진을 가동합니다..."):
                target_df = crawl_realtime_on_demand(product_id)

            if target_df.empty:
                st.error("다이소몰에 등록되지 않았거나 리뷰가 존재하지 않는 품번입니다.")
                return

        avg_score = target_df["별점"].mean()
        st.markdown(f"### 평균 별점\n#### {convert_rating_to_stars(avg_score)}")
        st.markdown("---")

        perfect_satisfaction, reference_tips = split_and_analyze_sentences_strict(target_df)

        pos_ranked = get_ranked_keywords_fixed(perfect_satisfaction, mode="장점")
        neg_ranked = get_ranked_keywords_fixed(reference_tips, mode="단점")

        clean_neg_ranked = []
        for neg in neg_ranked:
            if "건조" in neg and "촉촉함/보습력 우수" in pos_ranked: continue
            if "자극" in neg and "순함/저자극" in pos_ranked: continue
            clean_neg_ranked.append(neg)

        default_pos = ["사용감 및 텍스처 만족", "피부 친화적 포뮬러", "가성비 대비 뛰어난 효과"]
        default_neg = ["개인차에 따른 체감 상이", "용량 및 패키지 아쉬움", "특정 환경 내 사용 주의"]

        while len(pos_ranked) < 3:
            candidate = default_pos[len(pos_ranked)]
            if candidate not in pos_ranked: pos_ranked.append(candidate)
        while len(clean_neg_ranked) < 3:
            candidate = default_neg[len(clean_neg_ranked)]
            if candidate not in clean_neg_ranked: clean_neg_ranked.append(candidate)

        col_pos, col_neg = st.columns(2)

        with col_pos:
            st.markdown("#### 😊 긍정 키워드 순위")
            for idx, kw in enumerate(pos_ranked[:3], 1):
                st.success(f"{idx}위. {kw}")
        with col_neg:
            st.markdown("#### 😡 부정 키워드 순위")
            for idx, kw in enumerate(clean_neg_ranked[:3], 1):
                st.error(f"{idx}위. {kw}")

        st.markdown("---")
        st.markdown("#### 대표 핵심 리뷰 (추천순 기준)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**👍 완전 만족해요**")
            for i, s in enumerate(perfect_satisfaction[:3], 1):
                st.info(f"{i}. {s}")
        with c2:
            # [수정 적용] 이모티콘과 글자 사이에 공백 한 칸 추가 완료
            st.markdown("**⚠️ 참고해주세요**")
            for i, s in enumerate(reference_tips[:3], 1):
                st.warning(f"{i}. {s}")


def render_attribute_recommendation(df):
    st.subheader("카테고리별 제품 추천")
    cat_cols = st.columns(4)
    categories = ["스킨케어", "선케어", "클렌징", "메이크업"]

    if "selected_cat" not in st.session_state: st.session_state.selected_cat = "스킨케어"
    for i, cat in enumerate(categories):
        with cat_cols[i]:
            if st.button(cat, use_container_width=True,
                         type="primary" if st.session_state.selected_cat == cat else "secondary"):
                st.session_state.selected_cat = cat
                st.rerun()

    current_cat = st.session_state.selected_cat
    sub_item = None

    if current_cat == "메이크업":
        sub_items = CONFIG_DYNAMIC["메이크업"]["세부항목"]
        sub_cols = st.columns(5)
        if "selected_sub" not in st.session_state: st.session_state.selected_sub = sub_items[0]
        for i, sub in enumerate(sub_items):
            with sub_cols[i]:
                if st.button(sub, use_container_width=True,
                             type="primary" if st.session_state.selected_sub == sub else "secondary"):
                    st.session_state.selected_sub = sub
                    st.rerun()
        sub_item = st.session_state.selected_sub
        filtered_df = df[(df["카테고리"] == "메이크업") & (df["세부항목"] == sub_item)] if not df.empty else pd.DataFrame()
    else:
        filtered_df = df[df["카테고리"] == current_cat] if not df.empty else pd.DataFrame()

    st.markdown("---")
    if filtered_df.empty:
        st.warning("선택하신 카테고리의 수집된 데이터가 없습니다. crawling.py를 통해 데이터를 수집해 주세요.")
        return

    unique_products = filtered_df["제품명"].unique()[:4]
    grid_cols = st.columns(2)

    for idx, prod in enumerate(unique_products):
        target_col = grid_cols[idx % 2]
        p_df = filtered_df[filtered_df["제품명"] == prod]

        avg_rating = p_df["별점"].mean()
        prod_id = str(p_df["품번"].iloc[0]).strip()
        detected_attr = get_clean_keywords(p_df)
        perfect_satisfaction, _ = split_and_analyze_sentences_strict(p_df)

        if prod_id in FIXED_DATA_MAP:
            prod_price = FIXED_DATA_MAP[prod_id]["가격"]
            prod_img = FIXED_DATA_MAP[prod_id]["이미지"]
        else:
            prod_price = p_df["가격"].iloc[0] if "가격" in p_df.columns and pd.notna(p_df["가격"].iloc[0]) else "가격 정보 없음"
            prod_img = p_df["이미지"].iloc[0] if "이미지" in p_df.columns and pd.notna(p_df["이미지"].iloc[0]) else ""

        # [최종 오류 해결] 이 부분의 "リンク"까지 완벽하게 한국어 "링크" 컬럼으로 전수 교체 완료했습니다!
        prod_link = p_df["링크"].iloc[
            0] if "링크" in p_df.columns else f"https://www.daisomall.co.kr/pd/pdr/SCR_PDR_0001?pdNo={prod_id}"

        with target_col:
            st.markdown(f"""
            <div style="border:1px solid #e2e8f0; border-radius:14px; padding:18px; margin-bottom:15px; background-color:#ffffff;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <span style="background-color:#E28743;
                color:white; padding:5px 14px; border-radius:20px; font-weight:bold; font-size:15px;">추천 속성: {detected_attr}</span>
            </div>
            """, unsafe_allow_html=True)

            img_col, info_col = st.columns([1, 1.6])
            with img_col:
                if prod_img and str(prod_img).startswith("http"):
                    st.image(prod_img, use_container_width=True)
                else:
                    st.markdown(
                        "<div style='background-color:#f1f5f9; height:160px; border-radius:8px; display:flex; justify-content:center; align-items:center; color:#94a3b8; font-size:13px;'>No Image</div>",
                        unsafe_allow_html=True)
            with info_col:
                st.markdown(f"#### {prod}")
                st.markdown(f"<span style='color:#dc2626; font-weight:bold; font-size:16px;'>{prod_price}</span>",
                            unsafe_allow_html=True)
                st.text(f"매대 현장품번: {prod_id}")
                st.text(f"평점: {convert_rating_to_stars(avg_rating)}")
                st.link_button("👉 다이소몰 매칭 상품 페이지", prod_link, use_container_width=True)

            st.markdown(
                """<div style="border-top:1px dashed #e2e8f0;
                margin-top:12px; padding-top:8px;"><p style="font-size:13px; font-weight:bold; color:#475569;">대표 핵심 리뷰</p></div>""",
                unsafe_allow_html=True)

            if perfect_satisfaction:
                for i, s in enumerate(perfect_satisfaction[:3], 1):
                    st.markdown(
                        f"<div style='font-size:14px; color:#334155; background-color:#f8fafc; padding:7px; border-radius:6px; margin-bottom:4px; border-left:3px solid #cbd5e1;'>{i}. {s}</div>",
                        unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-size:13px; color:#94a3b8;'>조건을 충족하는 심층 증명 리뷰가 부족합니다.</div>",
                            unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="다이소 현장 매대 뷰티 가이드", layout="wide")
    st.title("다이소-Beauty 탐사대 🔍")
    df = load_recommend_data()

    tab1, tab2 = st.tabs(["궁금한 제품이 생긴다면?", "카테고리별 제품 추천"])
    with tab1: render_quality_verification(df)
    with tab2: render_attribute_recommendation(df)


if __name__ == "__main__":
    main()