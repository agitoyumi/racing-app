import streamlit as st
import telebot
from threading import Thread
import time

# 填入你嘅正確資料
API_TOKEN = '8663783053:AAErT0yV6z5oW5z1l-D7Z_T7y5E_Z7z7z7z'
MY_CHAT_ID = '411468742'

bot = telebot.TeleBot(API_TOKEN)

# 測試用功能
def heartbeat():
    while True:
        try:
            bot.send_message(MY_CHAT_ID, "💓 系統心跳測試：監控中...")
            time.sleep(3600) # 每小時響一次，證明佢仲生存緊
        except:
            pass

st.title("Predator 緊急重啟中心")
st.write("如果 Telegram 收到心跳訊息，代表連接正常。")

if 'started' not in st.session_state:
    Thread(target=heartbeat, daemon=True).start()
    st.session_state.started = True

# 保持 Bot 響應
@bot.message_handler(commands=['check'])
def check(message):
    bot.reply_to(message, "✅ 收到！我仲喺度，隨時準備收割 300 倍！")

# 啟動 Polling (最重要)
if __name__ == "__main__":
    bot.polling(none_stop=True)
