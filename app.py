import requests
import telebot
import streamlit as st
import time
import threading

# ================= 1. 配置 (老闆專用) =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 核心抓取邏輯 (極致簡化，防斷線) =================
def fetch_raw_data():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 歸零重啟報表】\n"
    report += "========================\n\n"
    
    # --- A. 抓取波膽 (放寬門檻，保證有💎) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：高倍波膽】\n"
            for m in cs_res.json()[:8]:
                m_name = f"{m['home_team']} vs {m['away_team']}"
                # 只要係 7x 以上嘅波膽全部噴出嚟
                outcomes = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if o['price'] >= 7.0]
                if outcomes:
                    report += f"📍 {m_name} | {outcomes[0]['name']} | {outcomes[0]['price']}x\n"
        time.sleep(2) # 避 422

        # --- B. 抓取穩定盤 (硬過濾 1.95x+) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            report += "\n✅ 【組合：2.0x+ 嚴選】\n"
            for m in h2h_res.json()[:15]:
                m_name = f"{m['home_team']} vs {m['away_team']}"
                # 只要場波入面有任何一個盤高過 1.95x
                picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if o['price'] >= 1.95]
                if picks:
                    report += f"🔹 {m_name} | {picks[0]['name']} | {picks[0]['price']}x\n"
            
            report += "\n🚨 【資金異常預警】\n"
            for m in h2h_res.json()[:8]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.15 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {m['home_team']} ({o['price']}x)\n"
    except Exception as e:
        report += f"❌ 獲取失敗: {e}"
    
    return report

# ================= 3. TG 指令 (保證回應) =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    bot.reply_to(message, "📡 接收指令！正聯網提取全球數據...")
    result = fetch_raw_data()
    bot.send_message(CHAT_ID, result)

def run_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=run_bot, daemon=True)
    st.session_state.bot_thread.start()

# ================= 4. Streamlit =================
st.title("🏹 獵人：歸零重啟版")
if st.button("🔥 立即全網提取 (保證出貨)"):
    st.code(fetch_raw_data())
