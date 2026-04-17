import streamlit as st
import requests

# --- 核心配置 ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
TG_CHAT_ID = "411468742"

def send_tg(text):
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                  json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"})

st.title("🏹 暴力反殺：$100 止血中樞")

# 鎖定實盤數據
odds_stable = 415.4
bet_amount = 100

st.header(f"💰 目標回報：${bet_amount * odds_stable:,.0f}")
st.metric("最穩組合賠率", f"{odds_stable} 倍", "波膽 3 串 1")

st.write("---")
st.subheader("🎯 17:30 實戰執行")
st.info("🔹 狼隊 1:2 | 🔹 綠軍 1:1 | 🔹 勝利 2:1")

if st.button("🚀 啟動 $100 反殺方案 (TG 震動備忘)", use_container_width=True):
    msg = (
        f"🔥 *老闆，聖羅倫輸咗嘅，我哋下晝加倍攞返！*\n\n"
        f"📊 *方案：暴力波膽 3 串 1*\n"
        f"💰 注碼：${bet_amount}\n"
        f"🏆 目標派彩：*${bet_amount * odds_stable:,.0f}*\n\n"
        f"🕒 17:30 準時報喜！今晚一鋪過翻身！"
    )
    send_tg(msg)
    st.success("✅ 反殺方案已入 TG！等 17:30 報仇！")
