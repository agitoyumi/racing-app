import requests
import telebot
import streamlit as st
import time
import threading

# ================= 1. 配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會對譯 (確保無誤) =================
HKJC_MAP = {"Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", "Stockport": "史托港", "Racing Club": "競賽會", "Ulsan": "蔚山現代", "Arsenal": "阿仙奴", "Bayern": "拜仁"}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 修正後嘅數據引擎 =================
def run_final_fix():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：數據清洗完成版】\n========================\n\n"
    
    try:
        # --- A. 核武波膽 (嚴格限制 8x - 35x) ---
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：8x-35x 波膽】\n"
            count = 0
            for m in cs_res.json()[:12]:
                if count >= 6: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 關鍵修正：剔除 501x 呢類垃圾，只攞 8 到 35 嘅正常高倍
                outcomes = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 35.0]
                if outcomes:
                    report += f"📍 {m_name} | {outcomes[0]['name']} | {outcomes[0]['price']}x\n"
                    count += 1
        
        time.sleep(1.5)

        # --- B. 穩定盤 (嚴格鎖死 2.0x 以上) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            report += "\n✅ 【組合：2.0x+ 嚴選】\n"
            v_count = 0
            for m in h2h_res.json():
                if v_count >= 8: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 物理過濾：低過 2.0 一律當睇唔到
                valid = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if o['price'] >= 2.0]
                if valid:
                    report += f"🔹 {m_name} | {to_hkjc(valid[0]['name'])} | {valid[0]['price']}x\n"
                    v_count += 1
    except: report += "❌ 數據提取中斷"
    
    return report

# ================= 4. TG 控制 =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    bot.send_message(CHAT_ID, "📡 正在攔截 501x 垃圾數據，重組 2.0x 核心報表...")
    bot.send_message(CHAT_ID, run_final_fix())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：數據清算版")
if st.button("🔥 執行物理過濾掃描"):
    st.code(run_final_fix())
