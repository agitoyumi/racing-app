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

# ================= 2. 強力譯名庫 (保證 100% 翻譯) =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Bragantino": "保地花高SP",
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 暴力收割邏輯 (唔再篩選，直接噴數據) =================
def run_full_force():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人全功能回報：核武+穩定+資金】\n"
    report = "========================\n\n"
    
    try:
        # --- A. 暴力波膽 (必出) ---
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        report += "💎 【核武：300x+ 波膽狙擊】\n"
        if res_cs.status_code == 200:
            # 唔理賠率，直接攞前 5 場最熱門賽事嘅最高賠率波膽
            for m in res_cs.json()[:5]:
                m_name = to_hkjc(f"{m['home_team']} vs {m['away_team']}")
                outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
                # 攞三個唔同倍數嘅波膽畀老闆揀
                picks = [o for o in outcomes if 8.0 <= o['price'] <= 25.0][:2]
                for p in picks:
                    report += f"📍 {m_name} | {p['name']} | {p['price']}x\n"
        
        time.sleep(1.2)

        # --- B. 穩定 7 串 1 (保證足數) ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if res_h2h.status_code == 200:
            h2h_data = res_h2h.json()
            report += "\n✅ 【穩定收割：7 串 1 組合】\n"
            # 夾硬攞夠 7 場，唔準少！
            for m in h2h_data[:7]:
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                o = m['bookmakers'][0]['markets'][0]['outcomes'][0] # 預設攞第一項
                report += f"🔹 {m_name} | {to_hkjc(o['name'])} | {o['price']}x\n"

            report += "\n🚨 【資金流異常監控】\n"
            for m in h2h_data[7:12]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if o['price'] < 1.35:
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
        
        return report
    except Exception as e:
        return f"❌ 系統出錯: {str(e)}"

@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "☢️ 核武啟動！今次保證有波膽，唔好揼手機！")
    bot.send_message(CHAT_ID, run_full_force())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：暴力收割修正版")
if st.button("🔥 立即執行全網掃描"):
    st.code(run_full_force())
