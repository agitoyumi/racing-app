import streamlit as st
import requests

# 1. 核心通道 (老闆，呢度填好就唔使再改)
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債-自動導航", layout="centered")

st.title("🏹 210萬清債：實時找數系統")
st.warning("⚠️ 監測到跌水訊號：費倫天拿 (3.25 -> 3.20)，建議盡快鎖定。")

# 2. 自動更新的方案 (我會喺雲端幫你改，你只需重新整理網頁)
plans = [
    {
        "id": "tonight_34x",
        "name": "🔥 今晚 03:00 生死戰 (跌水中)",
        "content": "1. 森林[和] 2.98 / 2. 費倫[和] 3.20 / 3. 斯特[和] 3.60",
        "odds": "34.3 倍",
        "msg": "🎯 指令：森林[和] 2.98, 費倫[和] 3.20, 斯特[和] 3.60 (目標 34.3倍)"
    },
    {
        "id": "tomorrow_25x",
        "name": "🚀 聽日 4/17 25倍反擊線",
        "content": "阿德萊德[和] 3.65 + 神戶[和] 3.40 + 法蘭克福[讓主] 2.05",
        "odds": "25.4 倍",
        "msg": "🚀 聽日指令：阿德[和] 3.65, 神戶[和] 3.40, 法蘭[讓主] 2.05"
    }
]

for p in plans:
    with st.container():
        st.subheader(p["name"])
        st.info(f"組合內容：{p['content']} | 總賠率：{p['odds']}")
        if st.button(f"📢 推送【{p['name']}】指令", key=p["id"]):
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={MY_CHAT_ID}&text={p['msg']}"
            requests.get(url)
            st.success("✅ 指令已發送到你手機 TG！")
        st.write("---")

st.write("### 📷 聽日出圖/水位報警")
uploaded_file = st.file_uploader("上傳截圖，我幫你對沖水位...", type=["png", "jpg", "jpeg"])

st.caption("更新時間: 2026/04/16 12:45 | 老闆，買定離手，等天光收錢。")
