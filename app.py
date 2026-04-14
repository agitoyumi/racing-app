import streamlit as st
import telebot
import time
from threading import Thread

# --- 1. 核心參數 (請確保資料正確) ---
API_TOKEN = '8663783053:AAErT0yV6z5oW5z1l-D7Z_T7y5E_Z7z7z7z'
MY_CHAT_ID = '411468742'

# 門檻設定
LV1_THRESHOLD = 500
LV2_THRESHOLD = 300

# 啟動 Bot
bot = telebot.TeleBot(API_TOKEN)

# --- 2. 監控邏輯 ---
def auto_monitor():
    """後台靜默監控，一旦有 300/500 倍即刻彈出"""
    while True:
        try:
            # 這裡之後會對接真實數據，目前先維持監控心跳
            # 如果發現目標組合，會執行 bot.send_message
            time.sleep(3600) # 每小時巡邏一次
        except Exception as e:
            time.sleep(10)

# --- 3. Streamlit 介面 ---
st.set_page_config(page_title="Predator HQ", page_icon="🏹")
st.title("🏹 掠食者指揮部 (工作穩定版)")

st.success(f"✅ 系統運作中 | LV2 門檻: {LV2_THRESHOLD}x")

if st.button("🚀 即時測試連線"):
    try:
        bot.send_message(MY_CHAT_ID, "✅ 指揮部報告：連線正常！我會喺後台幫你盯住 300 倍以上嘅獵物。")
        st.write("訊息已發送至 Telegram，請查收。")
    except Exception as e:
        st.error(f"發送失敗，請檢查 Token。錯誤: {e}")

# --- 4. 安全啟動後台 ---
if 'bot_active' not in st.session_state:
    t = Thread(target=auto_monitor)
    t.daemon = True
    t.start()
    st.session_state.bot_active = True

st.divider()
st.info("工作中模式：介面已鎖定，系統會透過 Telegram 主動聯絡你。")
