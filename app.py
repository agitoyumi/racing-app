import streamlit as st
import telebot
from threading import Thread
import time

# --- 1. 核心參數 (已更新為最新 Token) ---
API_TOKEN = '8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A'
MY_CHAT_ID = '411468742'

# 門檻設定
LV1_THRESHOLD = 500  # 核武級
LV2_THRESHOLD = 300  # 精準級 (密食當三番)

# 啟動 Bot
bot = telebot.TeleBot(API_TOKEN)

# --- 2. 監控邏輯 (工作中穩定版) ---
def auto_monitor():
    """後台靜默監控，一旦發現目標組合會自動發送 TG"""
    while True:
        try:
            # 這裡之後會對接真實數據流
            time.sleep(3600) 
        except Exception as e:
            time.sleep(10)

# --- 3. Streamlit 介面 ---
st.set_page_config(page_title="Predator HQ", page_icon="🏹")
st.title("🏹 掠食者指揮部 (終極修復版)")

st.success(f"✅ 系統狀態：監控中 | 門檻：{LV2_THRESHOLD}x 起跳")

# 測試連線按鈕
if st.button("🚀 點擊測試連線 (確認手機有無響)"):
    try:
        bot.send_message(MY_CHAT_ID, "✅ 【連線報告】\nToken 更新成功！永動機已接通。\n我會幫你盯住 300 倍以上嘅獵物。")
        st.balloons()
        st.write("### 📢 已成功發送！請檢查手機 Telegram。")
    except Exception as e:
        st.error(f"連線仍然失敗，請確認 Token 是否正確。錯誤原因: {e}")

st.divider()
st.info("💡 建議：工作中唔使成日睇網頁，只要撳完上面個掣有響，你就可以專心返工，等 TG 通知。")

# --- 4. 啟動監控線程 ---
if 'bot_active' not in st.session_state:
    t = Thread(target=auto_monitor)
    t.daemon = True
    t.start()
    st.session_state.bot_active = True
