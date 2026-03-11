import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def search_naver(query):

    url = f"https://search.naver.com/search.naver?query={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        text = soup.get_text()

        return text

    except:
        return None


def validate(df):

    results = []
    real_addr = []

    for i,row in df.iterrows():

        name = str(row[0])
        addr = str(row[1])

        search = name.replace("롯데리아","롯데리아 ")

        page = search_naver(search)

        if page is None:

            results.append("X")
            real_addr.append("검색실패")
            continue

        key = addr.split()[0]

        if key in page:

            results.append("O")
            real_addr.append("검색확인")

        else:

            results.append("X")
            real_addr.append("주소불일치")

        time.sleep(0.5)

    df["진위여부"] = results
    df["확인결과"] = real_addr

    return df


st.title("가맹점 주소 검증기")

st.write("엑셀 업로드 → 지점명 기반 주소 검증")

file = st.file_uploader("엑셀 업로드", type=["xlsx"])

if file:

    df = pd.read_excel(file)

    st.write("데이터 확인")

    st.dataframe(df.head())

    if st.button("검증 시작"):

        with st.spinner("검증 진행중..."):

            result = validate(df)

        st.success("검증 완료")

        st.dataframe(result)

        result.to_excel("result.xlsx", index=False)

        with open("result.xlsx","rb") as f:

            st.download_button(
                "결과 엑셀 다운로드",
                f,
                file_name="result.xlsx"
            )