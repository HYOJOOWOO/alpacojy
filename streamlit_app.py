
# streamlit_app.py
# pip install streamlit gspread oauth2client

import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="이수율 확인", layout="centered")
st.title("📊 내 이수율 확인 프로그램 (구글 시트 연동, secrets 이용)")

# 사용자 입력
name = st.text_input("이름을 입력하세요")
phone_last4 = st.text_input("전화번호 뒷자리(4자리)", max_chars=4)

# Google Sheets 연동
def find_user(name, phone_last4):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        json_key = json.loads(st.secrets["gcp_service_account"])  # secrets에서 가져오기
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
        client = gspread.authorize(creds)
        sheet = client.open("이수율데이터").sheet1
        records = sheet.get_all_records()

        for user in records:
            if user["이름"] == name and str(user["전화번호뒷자리"]) == phone_last4:
                return user
        return None
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
        return None

# 결과 버튼
if st.button("조회하기"):
    if not name or not phone_last4:
        st.warning("이름과 전화번호 뒷자리를 모두 입력해주세요.")
    else:
        user = find_user(name, phone_last4)
        if user:
            st.success("✅ 이수율 결과")
            st.write(f"**이름**: {user['이름']}")
            st.write(f"사전진단: {user['사전진단']}%")
            st.write(f"사전 워크샵: {user['사전워크샵']}%")
            st.write(f"원격연수: {user['원격연수']}%")
            st.write(f"집합연수: {user['집합연수']}%")
            st.write(f"총 이수율: {user['총이수율']}%")
            st.write(f"이수 여부: {user['이수여부']}")
        else:
            st.error("❌ 일치하는 사용자를 찾을 수 없습니다.")
