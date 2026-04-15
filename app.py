import requests
import telebot
import streamlit as st
import time
import threading

# ================= 1. 配置中心 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 終極馬會譯名大辭典 =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Bragantino": "保地花高SP",
    "Arsenal": "阿仙奴", "Bayern": "拜仁", "Real Madrid": "皇家馬德里",
    "Molde": "莫迪", "Viking": "維京", "Brann": "白蘭恩", "Bodø/Glimt": "波杜基林特"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核心一鍵掃描邏輯 =================
def run_full_check():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人全功能回報：核武+穩定+資金】\n"
    report += "========================\n\n"
    
    try:
        # --- A. 核武波膽 (300x-1000x) ---
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if res_cs.status_code == 200:
            report += "💎 【核武：300x+ 波膽狙擊】\n"
            for m in res_cs.json()[:10]:
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 篩選 9-22 倍
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 9.0 <= o['price'] <= 22.0:
                        report += f"📍 {m_name} | {o['name']} | {o['price']}x\n"
                        break
        
        time.sleep(1.2) # 必備停頓，避開 422

        # --- B. 5x1/7x1 & 資金監控 ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if res_h2h.status_code == 200:
            h2h_data = res_h2h.json()
            
            report += "\n✅ 【穩定：5-7 串 1 精選 (2.0x+)】\n"
            for m in h2h_data[:12]:
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 2.1 <= o['price'] <= 3.6:
                        report += f"🔹 {m_name} | {to_hkjc(o['name'])} | {o['price']}x\n"
                        break

            report += "\n🚨 【資金流異常突襲】\n"
            for m in h2h_data[:8]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if o['price'] < 1.32: # 強力熱錢
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
        
        return report
    except Exception as e:
        return f"❌ 掃描失敗: {str(e)}"

# ================= 4. TG /check 指令復活 =================
@bot.message_handler(commands=['check', 'nuclear', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 收到！核武系統啟動，正在為老闆整合所有數據...")
    result = run_full_check()
    bot.send_message(CHAT_ID, result)

def start_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

# ================= 5. 網頁介面 =================
st.set_page_config(page_title="獵人終極體", layout="wide")
st.title("🏹 獵人：全功能合一狙擊系統")

if st.button("🔥 執行全火力掃描 (網頁同步)"):
    with st.spinner('🎯 深度掃描中...'):
        final_report = run_full_check()
        st.code(final_report)
        bot.send_message(CHAT_ID, final_report)
        st.success("🎯 數據已全數推送！")
