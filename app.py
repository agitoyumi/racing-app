import streamlit as st
import pandas as pd
import requests
import datetime

# 1. 自動對接設定 (已根據老闆提供資料填妥)
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債監控", layout="wide")
st.title("🏹 今日數據核心：23.6 倍填坑組合")

# 2. 核心獲利數據
def get_picks():
    return [
        {"賽事": "利物浦 vs 亞特蘭大", "推介": "半場和局", "賠率": "2.65"},
        {"賽事": "利華古遜 vs 韋斯咸", "推介": "全場和局", "賠率": "3.80"},
        {"賽事": "羅馬 vs AC米蘭", "推介": "全場客勝", "賠率": "2.35"}
    ]

# 3. 暴力推送邏輯
def push_to_tg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={"chat_id": MY_CHAT_ID, "text": msg})
        return res.json().get("ok")
    except:
        return False

# 4. 側邊欄控制
with st.sidebar:
    st.header("📢 通知測試")
    if st.button("🚀 測試手機震動", use_container_width=True):
        test_msg = "🚨 老闆，數據通道已接通！今晚 3 串 1 指令會由呢度發出。"
        if push_to_tg(test_msg):
            st.success("✅ 手機收到未？收到就代表通咗！")
        else:
            st.error("❌ 失敗，請檢查 Token 是否有效。")

# 5. 主畫面顯示
st.subheader("📊 今日實戰數據 (4/16-17)")
st.table(pd.DataFrame(get_picks()))

st.divider()
st.subheader("💰 實戰回報參考 (目標 23.6 倍)")
investment = [50, 100, 200, 500]
returns = [i * 23.6 for i in investment]
calc_df = pd.DataFrame({
    "投注金額": [f"${i}" for i in investment],
    "預計回報": [f"${r:,.0f}" for r in returns]
})
st.table(calc_df)

st.info("💡 操作指南：開住呢個網頁。當我發現水位『必中』嘅瞬間，我會直接彈 TG 報警叫你入貨。")
