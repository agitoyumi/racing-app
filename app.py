import streamlit as st
import requests
import time

# --- 老闆專屬配置 (已自動填寫) ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742"

def send_tg_alert(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        st.error(f"TG 發送失敗: {e}")

st.set_page_config(page_title="1857 自救監控", page_icon="🏹")

st.title("🏹 1857 暴力自救：老闆 L.M. 專屬")

# --- 戰線數據看板 ---
st.subheader("🍱 晚餐：4 串 11 (目標 $8.9萬)")
col1, col2 = st.columns(2)
with col1:
    st.info("🕒 15:00 布獅 vs 墨城 (2:2) - 12.5x")
    st.info("🕒 15:30 濟州 vs 金泉 (1:2) - 8.0x")
with col2:
    st.info("🕒 15:30 富川 vs 仁川 (0:1) - 5.7x")
    st.info("🕒 17:35 悉尼 vs 珀斯 (3:1) - 10.0x")

st.subheader("🌙 宵夜：2 x 3 (逆轉起家彈)")
st.warning("🎯 波琴 + 李斯特城 [主客/客主] | 中一場即收 $220+ | 全中 $8,280")

# --- 震機監控按鈕 ---
if st.button("🔥 啟動 TG 實時震機監控 (自救開始)"):
    st.balloons()
    send_tg_alert("✅【老闆 L.M. 自救啟動】\n\n子彈已鎖定：\n1. 4串11 ($110) -> 衝擊 $89,173\n2. 2x3 ($80) -> 逆轉收割 $8,280\n\n「係收就無得走！」第一場布獅即將開火！")
    st.success("🎯 已發送測試訊號到你的 Telegram！請檢查手機震唔震！")

st.divider()
st.caption("副手備註：數據已對準圖片，ID/Token 已入位。老闆，今日一定要收錢！")
