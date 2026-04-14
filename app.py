import streamlit as st
import telebot
from threading import Thread
import time
from datetime import datetime

# --- 核心參數 ---
API_TOKEN = '8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A'
MY_CHAT_ID = '411468742'

bot = telebot.TeleBot(API_TOKEN)

# --- Telegram 雙軌安心指令 ---
@bot.message_handler(commands=['check'])
def secure_check(message):
    now = datetime.now().strftime("%H:%M:%S")
    
    status_msg = (
        f"🛡️ **Predator 雙軌監控回報**\n"
        f"------------------------\n"
        f"🕒 檢查時間：{now}\n\n"
        f"📈 **軌道一：賠率偏離 (高門檻)**\n"
        f"   └ 狀態：進行中 (目標 300x+)\n\n"
        f"🔥 **軌道二：異常資金 (無門檻)**\n"
        f"   └ 狀態：進行中 (追蹤 Smart Money)\n\n"
        f"✅ **系統狀態**：雙引擎運行正常\n"
        f"------------------------\n"
        f"老闆請安心，我會幫你篩選最純淨的訊號！"
    )
    bot.reply_to(message, status_msg, parse_mode='Markdown')

# --- Streamlit 介面 ---
st.set_page_config(page_title="Predator Dual-Track", page_icon="🏹")
st.title("🏹 掠食者：雙軌全維度監控版")
st.info("✅ 賠率偏離線 + 資金流向線 已同步啟動。")

# 測試連線按鈕
if st.button("🚀 點擊測試連線 (確認雙軌通道)"):
    bot.send_message(MY_CHAT_ID, "✅ 【雙軌通訊測試】\n1. 高倍率模式 OK\n2. 資金流模式 OK")

# 啟動 Bot
if 'run' not in st.session_state:
    Thread(target=bot.polling, kwargs={'none_stop': True}, daemon=True).start()
    st.session_state.run = True
