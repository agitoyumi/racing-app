import streamlit as st
import requests
import datetime

# 1. 介面設定
st.set_page_config(page_title="核武翻身系統-緊急修復", layout="wide")
st.title("🚀 TG 暴力推送中心 (繞過廢 Bot)")

# 2. 核心真錢數據 (已人工過濾 4.15 垃圾)
def get_nuke_data():
    return [
        {"match": "利物浦 vs 亞特蘭大", "pick": "半場和局", "odds": "2.65"},
        {"match": "利華古遜 vs 韋斯咸", "pick": "全場和局", "odds": "3.80"},
        {"match": "羅馬 vs AC米蘭", "pick": "客勝", "odds": "2.35"}
    ]

# 3. 暴力推送邏輯 (直接調用 TG API)
def force_send_message():
    # 老闆，請確保呢度兩個 ID 係啱嘅
    token = "YOUR_TG_BOT_TOKEN" 
    chat_id = "YOUR_CHAT_ID"
    
    data = get_nuke_data()
    msg = f"🔥 【實質翻身報警】 {datetime.datetime.now().strftime('%H:%M:%S')}\n"
    msg += "----------------------\n"
    for d in data:
        msg += f"⚽ {d['match']}\n🎯 {d['pick']} @ {d['odds']}\n"
    msg += "----------------------\n"
    msg += "🚀 暴力 3 串 1 (約 23 倍)"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        res = requests.post(url, data={"chat_id": chat_id, "text": msg})
        return res.json()
    except Exception as e:
        return str(e)

# 4. 側邊欄：暴力掣
with st.sidebar:
    st.header("⚡ 緊急操作")
    if st.button("📢 唔理個 Bot，直接推送最新料去 TG", use_container_width=True):
        result = force_send_message()
        if isinstance(result, dict) and result.get("ok"):
            st.success("✅ TG 訊息已強行發出！")
        else:
            st.error(f"❌ 失敗：{result}")

# 5. 主頁面顯示數據
st.subheader("📊 今日數據掃描 (4/16-17)")
st.table(get_nuke_data())

st.warning("⚠️ 警告：個 TG Bot 嘅 /check 邏輯已死，請改用左邊個『📢 推送』掣嚟收料。")
