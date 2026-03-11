import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup


def search_store(query):

    url = f"https://map.naver.com/v5/search/{query}"

    headers = {
        "User-Agent":"Mozilla/5.0"
    }

    r = requests.get(url,headers=headers)

    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text,"html.parser")

    text = soup.get_text()

    return text


def validate_excel(file):

    df = pd.read_excel(file)

    results=[]
    real_addresses=[]

    for i,row in df.iterrows():

        name=str(row[0])
        input_addr=str(row[1])

        search=name.replace("롯데리아","롯데리아 ")

        page=search_store(search)

        if page is None:

            results.append("X")
            real_addresses.append("검색실패")
            continue

        if input_addr.split()[0] in page:

            results.append("O")
            real_addresses.append("확인됨")

        else:

            results.append("X")
            real_addresses.append("주소불일치")

    df["진위"]=results
    df["실제주소"]=real_addresses

    return df


st.title("지점 주소 검증기")

file=st.file_uploader("엑셀 업로드",type=["xlsx"])

if file:

    st.write("검증 진행중")

    result_df=validate_excel(file)

    st.success("완료")

    st.dataframe(result_df)

    result_df.to_excel("result.xlsx",index=False)

    with open("result.xlsx","rb") as f:

        st.download_button(
            "결과 엑셀 다운로드",
            f,
            file_name="result.xlsx"
        )