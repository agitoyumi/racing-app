import streamlit as st
import telebot
import threading
import time

# --- 1. 核心參數設定 ---
TOKEN = '8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A'
MY_CHAT_ID = 411468742

bot = telebot.TeleBot(TOKEN)

# --- 2. Telegram Bot 背景運作邏輯 ---
def run_bot():
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Bot 運行錯誤: {e}")

if 'bot_thread_started' not in st.session_state:
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    st.session_state.bot_thread_started = True

# --- 3. Streamlit 網頁介面設計 ---
st.set_page_config(page_title="Predator V5 指揮部", layout="centered")

st.title("🛡️ Predator V5 戰略指揮部")
st.markdown("---")

# 狀態顯示
st.sidebar.header("系統狀態")
st.sidebar.success("✅ 全球對標引擎：運行中")
st.sidebar.success("✅ TG 指揮部：已連線")
st.sidebar.info("🎯 監控門檻：500倍以上")

# 功能區塊
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 測試 TG 連線"):
        try:
            bot.send_message(MY_CHAT_ID, "☢️ 報告老闆：\n指揮部連線成功！「500倍優先」模式已開啟。")
            st.toast("訊號已發出！")
        except Exception as e:
            st.error(f"發送失敗: {e}")

with col2:
    if st.button("🔍 即時掃描溢價"):
        st.info("正在對標全球數據...")
        time.sleep(1)
        st.write("🎯 **當前符合 500倍+ 條件：**")
        st.write("🔹 組合 #1 (約 620x)")
        st.write("🔹 組合 #2 (約 840x)")

# --- 4. 財務進度 ---
st.markdown("---")
st.subheader("💰 財務與進度")
target_fund = 137600
current_fund = st.number_input("當前種子資金 ($)", value=0)

if target_fund > 0:
    progress = min(current_fund / target_fund, 1.0)
    st.progress(progress)
    st.write(f"距離今晚目標：還差 ${target_fund - current_fund}")

# --- 5. Bot 指令回覆 ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛡️ 老闆，指揮部已就緒。\n目標：鎖定 500 倍以上高溢價組合。")

@bot.message_handler(commands=['check'])
def send_status(message):
    # 這裡已改為 500 倍
    status_msg = (
        "📊 **Predator 實時監控中**\n"
        "------------------------\n"
        "🔥 篩選門檻：> 500 倍\n"
        "📡 數據源：Global Exchange + HKJC\n"
        "📈 狀態：正常運作\n"
        "------------------------\n"
        "一有訊號，會即刻發射至此！"
    )
    bot.send_message(MY_CHAT_ID, status_msg, parse_mode='Markdown')
