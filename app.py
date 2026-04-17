import streamlit as st
import requests
from datetime import datetime

# --- 1. 配置 (老闆專屬) ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
TG_CHAT_ID = "411468742"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=5)

# --- 2. 暴力波膽 4/17 黃金組合 ---
st.set_page_config(page_title="黃金週末反擊戰", layout="centered")
st.title("🌟 黃金週末：暴力追數中樞")
st.subheader("由 4/17 開始，目標清袋 30 萬！")

# 對準 08:24 盤口，波膽賠率取中間位
plans = [
    {"time": "17:30", "name": "溫納姆狼隊 vs 黃金海岸騎士", "pick": "波膽 [1:2 / 2:2]", "odds": 9.5},
    {"time": "17:30", "name": "賓特利綠軍 vs 普雷斯頓雄獅", "pick": "波膽 [2:1 / 1:1]", "odds": 8.0},
    {"time": "17:35", "name": "墨爾本勝利 vs 紐卡素噴射機", "pick": "波膽 [2:1 / 3:1]", "odds": 10.0}
]

# --- 3. 暴力回報計算 ---
total_odds = 760.0
st.write("---")
bet = st.number_input("黃金週五首發注碼 ($)", value=200)
payout = bet * total_odds

col1, col2 = st.columns(2)
col1.metric("暴力總賠率", f"{total_odds} 倍")
col2.metric("預計回報", f"${payout:,.0f}")

# --- 4. 戰略清單 ---
st.write("### 🏹 戰場分配")
for p in plans:
    st.warning(f"🕒 **{p['time']}** | {p['name']} \n\n🎯 建議：{p['pick']}")

# --- 5. 暴力通知 ---
if st.button("🚀 啟動黃金監控 (TG 震動報喜)", use_container_width=True):
    msg = (
        f"🌟 *老闆，黃金週末反擊戰啟動！*\n\n"
        f"🔥 *目標：一鋪清 30 萬債！*\n"
        f"1️⃣ 17:30 狼隊 -> {plans[0]['pick']}\n"
        f"2️⃣ 17:30 綠軍 -> {plans[1]['pick']}\n"
        f"3️⃣ 17:35 勝利 -> {plans[2]['pick']}\n\n"
        f"💰 注碼：${bet} | 賠率：{total_odds}\n"
        f"🏆 預計收：*${payout:,.0f}*\n\n"
        f"🚀 *17:30 準時見真章，TG 報喜！*"
    )
    send_tg(msg)
    st.balloons()
    st.success("✅ TG 已發送！老闆，今晚一齊「脫貧」！")

st.divider()
st.caption(f"數據同步: {datetime.now().strftime('%H:%M:%S')} | 黃金週末限定版")
