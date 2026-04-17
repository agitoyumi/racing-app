import streamlit as st
import requests

# --- 核心配置 ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
TG_CHAT_ID = "411468742"

def send_tg_msg(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=5)

# --- 暴力波膽方案 (對準 08:24 盤口) ---
st.title("🔥 暴力波膽 3 串 1 實戰中樞")

# 每場揀兩個波膽（雙膽），增加中獎機會
plans = [
    {"time": "17:30", "name": "溫納姆狼隊 vs 黃金海岸騎士", "picks": "1:2 / 2:2", "odds": 9.5},
    {"time": "17:30", "name": "賓特利綠軍 vs 普雷斯頓雄獅", "picks": "2:1 / 1:1", "odds": 8.0},
    {"time": "17:35", "name": "墨爾本勝利 vs 紐卡素噴射機", "picks": "2:1 / 3:1", "odds": 10.0}
]

total_odds = 760.0 # 9.5 * 8.0 * 10.0

# --- 買幾錢贏幾錢 ---
st.header("💰 追數利潤計算器")
bet_amount = st.number_input("輸入你想買幾錢 ($)", min_value=10, value=100, step=10)
payout = bet_amount * total_odds

col1, col2 = st.columns(2)
col1.metric("總賠率", f"{total_odds} 倍")
col2.metric("預計派彩", f"${payout:,.0f}")

st.write("---")
st.subheader("🎯 具體點樣買？")
for p in plans:
    st.info(f"🕒 **{p['time']}** | {p['name']}\n\n👉 建議波膽：**{p['picks']}** (約 {p['odds']} 倍)")

# --- 暴力按鈕 ---
if st.button("🚀 確定方案並 TG 備忘", use_container_width=True):
    msg = (
        f"🚨 *老闆，波膽 3 串 1 實戰方案！*\n\n"
        f"1️⃣ 17:30 狼隊 -> *{plans[0]['picks']}*\n"
        f"2️⃣ 17:30 綠軍 -> *{plans[1]['picks']}*\n"
        f"3️⃣ 17:35 勝利 -> *{plans[2]['picks']}*\n\n"
        f"💰 注碼：${bet_amount}\n"
        f"📈 總賠率：{total_odds} 倍\n"
        f"🏆 目標派彩：*${payout:,.0f}*\n\n"
        f"🔥 *中一鋪收幾萬，今晚即刻還債！*"
    )
    send_tg_msg(msg)
    st.success("✅ 方案已發送到 TG，手機應該會再震一次！")
