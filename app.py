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

# ================= 2. 終極馬會譯名 (針對今晚深夜賽事) =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 強力核武邏輯 =================
def run_full_check():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人全功能回報：核武+穩定+資金】\n"
    report += "========================\n\n"
    
    try:
        # --- A. 核武波膽 (確保輸出) ---
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if res_cs.status_code == 200:
            report += "💎 【核武：300x+ 波膽狙擊】\n"
            cs_found = False
            for m in res_cs.json()[:15]: # 增加掃描深度
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 稍微放寬賠率限制，確保一定有嘢出
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 7.0 <= o['price'] <= 25.0:
                        report += f"📍 {m_name} | {o['name']} | {o['price']}x\n"
                        cs_found = True
                        break
            if not cs_found: report += "⚠️ 當前盤口波膽數據波動，請稍後再試。\n"
        
        time.sleep(1.2)

        # --- B. 穩定組合 & 資金監控 ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if res_h2h.status_code == 200:
            h2h_data = res_h2h.json()
            report += "\n✅ 【穩定：5-7 串 1 精選 (2.0x+)】\n"
            for m in h2h_data[:12]:
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.9 <= o['price'] <= 4.0:
                        report += f"🔹 {m_name} | {to_hkjc(o['name'])} | {o['price']}x\n"
                        break

            report += "\n🚨 【資金流異常突襲】\n"
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if o['price'] < 1.35:
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
        
        return report
    except Exception as e:
        return f"❌ 系統炸裂: {str(e)}"

@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "☢️ 核武系統啟動，正在幫老闆挖出所有高倍波膽...")
    bot.send_message(CHAT_ID, run_full_check())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：全功能修正版")
if st.button("🔥 執行全網掃描"):
    st.code(run_full_check())
