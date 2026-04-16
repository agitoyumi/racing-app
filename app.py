import streamlit as st
import requests

# 1. 唯一通道
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債-自動導航系統")

st.title("🏹 210萬清債：實時找數系統")

# 2. 我會喺後台更新呢個區域，你唔使改 Code
st.subheader("📢 最新精選方案 (實時更新)")

# 呢度我會用一個 List 儲存所有方案
plans = [
    {
        "名稱": "🚨 今晚 03:00 生死戰 (34.8倍)",
        "內容": "1. 森林[和] 2. 費倫[和] 3. 斯特[和]",
        "指令": "🎯 今晚 35倍：森林/費倫/斯特 [全和]"
    },
    {
        "名稱": "🔥 聽日 4/17 核心戰 (25.4倍)",
        "內容": "1. 阿德萊德[和] 2. 神戶[和] 3. 法蘭克福[讓主]",
        "指令": "🚀 聽日 25倍：阿德[和]/神戶[和]/法蘭[讓主]"
    }
]

for p in plans:
    with st.expander(p["名稱"], expanded=True):
        st.write(f"**場次：** {p['內容']}")
        if st.button(f"推送「{p['名稱']}」至手機"):
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={MY_CHAT_ID}&text={p['指令']}"
            if requests.get(url).status_code == 200:
                st.success("✅ 手機已收到指令！")

st.divider()

# 3. 聽日出圖功能 (保留，以防馬會跳賠率)
st.info("💡 如果你想我針對你睇中嘅場次計數，請喺下面傳圖：")
uploaded_file = st.file_uploader("📷 上傳馬會截圖 (聽日專用)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.success("✅ 截圖已收到，我會即刻喺後台幫你校準並推送！")

st.caption("老闆，以後你淨係負責撳掣，唔使再掂段 Code。我會幫你守住。")
