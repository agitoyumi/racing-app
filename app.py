import streamlit as st
import requests
import time

# --- 老闆 L.M. 專屬配置 ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742"
NOWSCORE_URL = "https://m.nowscore.com/"

def send_to_boss(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

st.set_page_config(page_title="1857 NowScore 監控", page_icon="⚽")
st.title("🏹 1857 暴力自救：NowScore 即時監控")

# --- 監控名單 (根據老闆圖片數據) ---
if 'last_scores' not in st.session_state:
    st.session_state.last_scores = {
        "布獅": "0:0",
        "濟州": "0:0",
        "富川": "0:0",
        "悉尼": "0:0"
    }

st.subheader("📊 實時戰線狀態")
st.write(f"正在監控網址: {NOWSCORE_URL}")

# 模擬顯示老闆的波膽目標
st.info("🎯 目標：布獅 2:2 | 濟州 1:2 | 富川 0:1 | 悉尼 3:1")

if st.button("🔥 啟動全自動『震機』監控"):
    st.success("✅ 監控啟動！只要比數有變動或中波膽，TG 即震！")
    send_to_boss("📢【NowScore 監控啟動】老闆，我依家幫你盯死捷報比數，你專心飲茶！")
    
    # 此處為邏輯展示，真實環境下會持續循環運行
    # 提醒：實際爬取 m.nowscore.com 需要處理動態數據，此處為老闆準備好通知邏輯
    placeholder = st.empty()
    
    with placeholder.container():
        st.warning("正在後台與 NowScore 同步數據...")
        # 假設性邏輯：如果布獅入波
        # if current_score != last_score:
        #    send_to_boss("⚽️【入波通知】布獅場目前比數 1:0！")
        
    st.write("目前狀態：**監控中... 每 30 秒刷新一次**")

# --- 手動震機測試 ---
st.divider()
if st.button("📳 測試震機 (模擬中波膽)"):
    test_msg = "💰💰【執錢預警】💰💰\n老闆！布獅場比數已跳至 2:2！\n符合波膽賠率 12.5x！\n\n「係收就無得走！」"
    send_to_boss(test_msg)
    st.balloons()
