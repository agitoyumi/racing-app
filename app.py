import requests
import telebot
import streamlit as st

# ================= 核心參數 (請老闆喺呢度填返啱嘅嘢) =================
API_KEY = "3a0784d142517860438150499e17006d" # 檢查呢度！
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156" # 呢度一定要用 @userinfobot 比你嗰串！

bot = telebot.TeleBot(TG_TOKEN)

# ================= 介面設計 =================
st.title("⚽ 獵人狙擊系統 v2.1")
st.write(f"當前設定的 CHAT_ID: `{CHAT_ID}`")

if st.button("🔥 立即掃描並發送到 Telegram"):
    # 1. 測試 API 數據
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk&markets=h2h&oddsFormat=decimal"
    
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 401:
            st.error("❌ API Key 唔啱 (Error 401)。請檢查 API_KEY 變量。")
        elif res.status_code == 200:
            st.success("✅ API 連線正常！")
            data = res.json()
            report = "🚀 【老闆，最新獵報！】\n"
            report += f"掃描到 {len(data)} 場深夜球賽數據...\n"
            report += "--------------------\n"
            # 簡化輸出做測試
            for m in data[:3]:
                report += f"⚽ {m['home_team']} vs {m['away_team']}\n"
            
            # 2. 嘗試發送
            try:
                bot.send_message(CHAT_ID, report)
                st.balloons()
                st.success("✅ Telegram 收到未？收到就代表成功咗！")
            except Exception as e:
                st.error(f"❌ TG 發送失敗: {e}")
                st.info("💡 提示：請確保你已經喺 TG 搵個 Bot 打過指令，而且 CHAT_ID 係啱。")
        else:
            st.error(f"❌ API 出咗事 (Code {res.status_code})")
    except Exception as e:
        st.error(f"⚠️ 網絡錯誤: {e}")

# 側邊欄測試工具
if st.sidebar.button("⚙️ 檢查通行證狀態"):
    try:
        me = bot.get_me()
        st.sidebar.success(f"Bot 身份: {me.first_name}")
        st.sidebar.info("請確保你已手動啟動個 Bot (打過 /start)")
    except:
        st.sidebar.error("Token 唔啱，搵唔到個 Bot。")
