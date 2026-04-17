import streamlit as st
import requests

# --- TG 配置 ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
TG_CHAT_ID = "411468742"

def send_tg(text):
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                  json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"})

# --- 4/17 黃金週末數據 ---
st.title("🔥 暴力波膽：三場雙膽攻略")

# 對準 08:24 截圖賽事
matches = [
    {"time": "17:30", "name": "溫納姆狼隊 vs 黃金海岸騎士", "ball_A": "1:2", "ball_B": "2:2", "odds": 9.5},
    {"time": "17:30", "name": "賓特利綠軍 vs 普雷斯頓雄獅", "ball_A": "2:1", "ball_B": "1:1", "odds": 8.5},
    {"time": "17:35", "name": "墨爾本勝利 vs 紐卡素噴射機", "ball_A": "2:1", "ball_B": "3:1", "odds": 10.5}
]

# --- 注碼選擇 ---
st.subheader("💰 注碼及回報 (8條組合線)")
unit_bet = st.radio("選擇每注金額：", [10, 20], horizontal=True)
total_bet = unit_bet * 8
estimated_odds = 850.0 # 估計平均 3 串 1 賠率

st.metric("總本金", f"${total_bet}", f"每注 ${unit_bet}")
st.metric("預計最高派彩", f"${unit_bet * estimated_odds:,.0f}", "暴力 850 倍計")

st.write("---")
st.subheader("🎯 具體注項 (每場揀兩膽)")
for m in matches:
    col1, col2 = st.columns([2, 1])
    col1.write(f"🕒 **{m['time']}** | {m['name']}")
    col2.warning(f"膽：{m['ball_A']} / {m['ball_B']}")

# --- 暴力啟動 ---
if st.button("🚀 啟動黃金監控 (發送 8 組合到 TG)", use_container_width=True):
    msg = (
        f"🌟 *老闆，黃金週末『雙膽』方案已啟動！*\n\n"
        f"📊 *組合：3 串 1 (共 8 條線)*\n"
        f"💰 *每注 ${unit_bet} | 總本金 ${total_bet}*\n\n"
        f"1️⃣ 狼隊：{matches[0]['ball_A']} / {matches[0]['ball_B']}\n"
        f"2️⃣ 綠軍：{matches[1]['ball_A']} / {matches[1]['ball_B']}\n"
        f"3️⃣ 勝利：{matches[2]['ball_A']} / {matches[2]['ball_B']}\n\n"
        f"🏆 *預計派彩：約 ${unit_bet * estimated_odds:,.0f}*\n\n"
        f"🔥 *中咗呢鋪，聽日全世界幫你搬石！*"
    )
    send_tg(msg)
    st.success("✅ 8 條組合線已傳送到 TG！手機震咗未？")
