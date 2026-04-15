import requests
import telebot
import streamlit as st

# ================= 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156" 

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人 300x 系統", layout="wide")
st.title("🎯 獵人狙擊系統：格式修正版")

# ================= 1. 測試按鈕 =================
if st.sidebar.button("傳送測試訊號"):
    try:
        bot.send_message(CHAT_ID, "✅ 訊號已通！CHAT_ID 正確。")
        st.sidebar.success("TG 已發送！")
    except Exception as e:
        st.sidebar.error(f"TG 失敗：{e}")

# ================= 2. 核心掃描 (修正 422 問題) =================
if st.button("🔥 立即全網掃描 (修正格式)"):
    # 422 通常是因為 markets 參數太多或格式不對，這裡改用最精確的格式
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk&markets=h2h&oddsFormat=decimal"
    
    with st.spinner('正在用最精準格式抓取數據...'):
        try:
            res = requests.get(url, timeout=15)
            
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ 抓取成功！獲取 {len(data)} 場數據。")
                
                # 建立報告
                report = "🚀 【老闆，獵人修正版清單！】\n\n"
                for m in data[:5]: # 抓前5場測試
                    report += f"⚽ {m['home_team']} vs {m['away_team']}\n"
                
                # 發送到 TG
                bot.send_message(CHAT_ID, report)
                st.balloons()
                st.success("🎯 數據已推送到 Telegram！")
                
            else:
                st.error(f"❌ 依然失敗 (Code: {res.status_code})")
                st.write("詳細錯誤訊息：", res.text) # 呢行會直接顯示 422 到底想點
                
        except Exception as e:
            st.error(f"⚠️ 網絡出錯：{str(e)}")
