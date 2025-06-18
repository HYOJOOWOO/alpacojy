import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ✅ 인증 설정 (dict 변환 중요!)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    dict(st.secrets["gcp_service_account"]),  # ⚠️ 꼭 dict로 감싸야 함
    scopes=scopes
)
client = gspread.authorize(credentials)

# ✅ 구글 시트 열기
try:
    sheet = client.open("이수율데이터").sheet1  # 또는 open_by_key("시트ID")
    records = sheet.get_all_records()
except Exception as e:
    st.error(f"❌ 구글 시트 접근 중 오류가 발생했습니다: {e}")
    st.stop()

# ✅ UI 구성
st.set_page_config(page_title="내 이수율 확인", layout="centered")
st.title("📊 교육 이수율 확인 서비스")
st.markdown("##### 이름과 전화번호 뒷자리를 입력해주세요.")
name = st.text_input("이름", placeholder="예: 전제영")
phone_last4 = st.text_input("전화번호 뒷자리", max_chars=4, placeholder="예: 7797")
st.divider()

# ✅ 사용자 찾기
def find_user(name, phone_last4):
    for user in records:
        if user["이름"] == name and str(user["전화번호뒷자리"]) == phone_last4:
            return user
    return None

# ✅ 버튼 동작
if st.button("📥 이수율 조회하기"):
    if not name or not phone_last4:
        st.warning("⚠️ 이름과 전화번호 뒷자리를 모두 입력해주세요.")
    else:
        user = find_user(name, phone_last4)
        if user:
            st.success("🎉 이수율 조회 성공!")
            st.markdown(f"### 👤 {user['이름']}님의 이수 정보")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="사전진단", value=f"{user['사전진단']}%")
                st.metric(label="원격연수", value=f"{user['원격연수']}%")
            with col2:
                st.metric(label="사전 워크샵", value=f"{user['사전워크샵']}%")
                st.metric(label="집합연수", value=f"{user['집합연수']}%")

            st.divider()
            st.metric(label="총 이수율", value=f"{user['총이수율']}%")

            if user["이수여부"] == "이수":
                st.success("✅ 이수 완료")
            else:
                st.error("📌 미이수")
        else:
            st.error("😢 입력하신 정보와 일치하는 사용자가 없습니다.")
