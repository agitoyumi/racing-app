import streamlit as st
import telebot
import threading

# --- 1. Telegram Bot 初始化 ---
TOKEN = '8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A'
bot = telebot.TeleBot(TOKEN)

# 呢個 Function 負責 24 小時喺背景行
def run_bot():
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Bot Error: {e}")

# 啟動背景線程 (只啟動一次)
if 'bot_thread' not in st.session_state:
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    st.session_state.bot_thread = True

# --- 2. Streamlit 網頁內容 ---
st.title("🛡️ 掠食者：雙線控制台")
st.success("✅ TG 指揮部已喺後台啟動")

if st.button("🚀 測試發送 TG 訊號"):
    bot.send_message("你的_CHAT_ID", "測試：全球對標引擎運作正常！")
    st.write("訊號已發出，請檢查 Telegram。")
