import streamlit as st
import requests

# 1. 老闆資料
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
TG_CHAT_ID = "411468742"

def send_tg(text):
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                  json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"})

# 2. 暴力場次
st.title("🏹 30 萬清債：波膽暴力 3 串 1")

st.markdown("""
### 🎯 今日暴力戰略
* **每場揀雙膽**：提高勝率
* **17:30 雙場齊開**：一開波就要見血
""")

total_odds = 760
bet_per_line = st.number_input("每注波膽買幾錢 ($)", value=20)
total_bet = bet_per_line * 8

st.metric("目標總回報", f"${bet_per_line * total_odds:,.0f}", f"總注碼: ${total_bet}")

# 3. 實施按鈕
if st.button("🚀 確定方案並 TG 通知", use_container_width=True):
    msg = (
        f"💰 *老闆，30萬清債方案！*\n\n"
        f"1️⃣ 狼隊 (1:2 / 2:2)\n"
        f"2️⃣ 綠軍 (1:1 / 2:1)\n"
        f"3️⃣ 勝利 (2:1 / 1:1)\n\n"
        f"📈 總賠率：約 {total_odds} 倍\n"
        f"🏆 每注 ${bet_per_line}，全中收 *${bet_per_line * total_odds:,.0f}*！\n\n"
        f"🔥 *醒多過人！17:30 準時報喜！*"
    )
    send_tg(msg)
    st.success("✅ TG 已經發送！返去搬石注意安全！")
