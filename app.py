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

# ================= 2. 強力譯名庫 (絕不失靈) =================
TRANSLATION = {
    "Ulsan Hyundai FC": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓",
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport County": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Arsenal": "阿仙奴", "Sporting Lisbon": "士砵亭", "Bayern Munich": "拜仁慕尼黑",
    "Real Madrid": "皇家馬德里", "Sarpsborg": "薩普斯堡", "Bodo/Glimt": "波杜基林特",
    "Seoul": "FC首爾", "Northampton": "諾咸頓", "Ettifaq": "伊提法克"
}

def hard_translate(text):
    for eng, hkg in TRANSLATION.items():
        text = text.replace(eng, hkg)
    return text.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核心抓取邏輯 =================
def fetch_final_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：真心脫困版】\n========================\n\n"
    
    # --- Part A: 💎 核武波膽 (8x - 60x) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：高倍波膽狙擊】\n"
            count = 0
            for m in cs_res.json():
                if count >= 5: break
                # 只攞 8.0x 到 60.0x 嘅正常高倍，攔截 1001x 垃圾
                picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 60.0]
                if picks:
                    m_name = hard_translate(f"{m['home_team']} 對 {m['away_team']}")
                    report += f"📍 {m_name} | {picks[0]['name']} | {picks[0]['price']}x\n"
                    count += 1
    except: report += "⚠️ 波膽模組載入失敗\n"

    time.sleep(1)

    # --- Part B: ✅ 穩定 2.0x+ 組合 ---
    try:
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【高勝率：鋼鐵 2.0x+ 組合】\n"
            v_count = 0
            for m in h2h_data:
                if v_count >= 7: break
                # 鋼鐵門檻：低過 2.0x 一律殺無赦
                valid = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.0]
                if valid:
                    m_name = hard_translate(f"{m['home_team']} 對 {m['away_team']}")
                    report += f"🔹 {m_name} | {hard_translate(valid[0]['name'])} | {valid[0]['price']}x\n"
                    v_count += 1

            # --- Part C: 🚨 資金監控 (壓飛) ---
            report += "\n🚨 【資金突襲：大戶監控】\n"
            for m in h2h_data[:15]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.01 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {hard_translate(m['home_team'])} ({o['price']}x)\n"
    except: report += "⚠️ 穩定盤模組載入失敗\n"

    return report

# ================= 4. TG 啟動 =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    bot.send_message(CHAT_ID, "📡 正在用「真心」重組數據，絕不容許 1.93x 或英文名...")
    bot.send_message(CHAT_ID, fetch_final_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：真心脫困版")
if st.button("🔥 全火力掃描 (2.0x 鋼鐵過濾)"):
    st.code(fetch_final_report())
