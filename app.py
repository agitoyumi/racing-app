import streamlit as st
import requests

# --- 核心配置 ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
TG_CHAT_ID = "411468742"

def send_tg(text):
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                  json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"})

# --- 老闆提供的精確賠率 (4/17 實盤) ---
st.title("🏹 暴力波膽：實盤精算中樞")

m1 = {"name": "溫納姆狼隊", "A": ("1:2", 8.25), "B": ("2:2", 9.75)}
m2 = {"name": "賓特利綠軍", "A": ("2:1", 9.0),  "B": ("1:1", 6.5)}
m3 = {"name": "墨爾本勝利", "A": ("2:1", 7.75), "B": ("3:1", 12.0)}

# --- 賠率範圍計算 (2x2x2 = 8 條線) ---
all_combinations = [
    m1['A'][1]*m2['A'][1]*m3['A'][1], m1['A'][1]*m2['A'][1]*m3['B'][1],
    m1['A'][1]*m2['B'][1]*m3['A'][1], m1['A'][1]*m2['B'][1]*m3['B'][1],
    m1['B'][1]*m2['A'][1]*m3['A'][1], m1['B'][1]*m2['A'][1]*m3['B'][1],
    m1['B'][1]*m2['B'][1]*m3['A'][1], m1['B'][1]*m2['B'][1]*m3['B'][1]
]
min_o = min(all_combinations)
max_o = max(all_combinations)

# --- 介面顯示 ---
st.subheader("💰 暴力回報分析")
unit_bet = st.radio("每注金額：", [10, 20], horizontal=True)
total_bet = unit_bet * 8

col1, col2 = st.columns(2)
col1.metric("總本金", f"${total_bet}")
col2.metric("最高預計派彩", f"${unit_bet * max_o:,.0f}", f"賠率: {max_o:.1f}倍")

st.write("---")
st.subheader("🎯 實戰注項 (雙膽)")
st.info(f"1️⃣ {m1['name']}: {m1['A'][0]}({m1['A'][1]}) / {m1['B'][0]}({m1['B'][1]})")
st.info(f"2️⃣ {m2['name']}: {m2['A'][0]}({m2['A'][1]}) / {m2['B'][0]}({m2['B'][1]})")
st.info(f"3️⃣ {m3['name']}: {m3['A'][0]}({m3['A'][1]}) / {m3['B'][0]}({m3['B'][1]})")

# --- 暴力啟動 ---
if st.button("🚀 確定方案並震動 TG", use_container_width=True):
    msg = (
        f"🚨 *老闆，4/17 暴力實盤雙膽！*\n\n"
        f"1️⃣ 狼隊：{m1['A'][0]}({m1['A'][1]}) / {m1['B'][0]}({m1['B'][1]})\n"
        f"2️⃣ 綠軍：{m2['A'][0]}({m2['A'][1]}) / {m2['B'][0]}({m2['B'][1]})\n"
        f"3️⃣ 勝利：{m3['A'][0]}({m3['A'][1]}) / {m3['B'][0]}({m3['B'][1]})\n\n"
        f"💰 *每注 ${unit_bet} | 總本金 ${total_bet}*\n"
        f"📈 *最高賠率：{max_o:.1f} 倍*\n"
        f"🏆 *最高可收：${unit_bet * max_o:,.0f}！*\n\n"
        f"🔥 *搬完石收大數，17:30 準時見真章！*"
    )
    send_tg(msg)
    st.success("✅ 實盤數據已傳送！去 TG 睇返條數，準備收錢！")
