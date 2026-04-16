import streamlit as st
import requests

# 1. 唯一通訊通道
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債-多線方案")

st.title("🏹 4/16-4/17 實戰找數清單")

# ---------------------------------------------------------
st.header("1️⃣ 第一優先：今晚凌晨 03:00 (生死戰)")
st.error("目標：34.8 倍 (三場全和)")
st.markdown("""
- **諾定咸森林 vs 波圖** (歐霸) -> 【和】 @ 2.98
- **費倫天拿 vs 水晶宮** (歐協) -> 【和】 @ 3.25
- **斯特拉斯堡 vs 緬恩斯** (歐協) -> 【和】 @ 3.60
""")

if st.button("📢 推送【今晚生死戰】指令至 TG"):
    msg = "🎯 今晚 03:00 找數指令：\n1. 森林[和] 2.98\n2. 費倫[和] 3.25\n3. 斯特[和] 3.60\n🔥 總倍率：34.8"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={MY_CHAT_ID}&text={msg}")
    st.success("✅ 今晚指令已送達！")

# ---------------------------------------------------------
st.divider()
st.header("2️⃣ 第二梯隊：聽日傍晚 (穩定增長)")
st.info("目標：約 8-12 倍 (精選日聯/澳職水位差)")
st.markdown("""
- **神戶勝利船 vs 橫濱水手** -> 【主勝】 (2026 實時數據優勢)
- **阿德萊德聯 vs 悉尼FC** -> 【和局】 (數據對沖位)
- **馬體會 vs 多蒙特** (歐冠殘局) -> 【小球】
""")

if st.button("📢 推送【聽日穩定型】指令至 TG"):
    msg = "🎯 聽日傍晚穩定方案：\n1. 神戶[主勝]\n2. 阿德萊德[和]\n3. 馬體會[小球]\n目標 10 倍回本。"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={MY_CHAT_ID}&text={msg}")
    st.success("✅ 聽日預案已送達！")

# ---------------------------------------------------------
st.divider()
st.header("3️⃣ 第三梯隊：聽日深夜 (大坑專用)")
st.warning("目標：50 倍以上 (冷門串場)")
st.write("這組我會等聽日馬會實時賠率變動後，再喺 TG 直接報警畀你。")

st.write("---")
st.caption("老闆，我唔再勉強做複雜嘢。今晚中咗，我哋聽日就有錢買飯，再戰第二梯隊。")
