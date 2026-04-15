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

# ================= 2. 強力譯名庫 =================
TRANSLATION = {
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓",
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Arsenal": "阿仙奴", "Sporting Lisbon": "士砵亭", "Bayern Munich": "拜仁慕尼黑",
    "Real Madrid": "皇家馬德里", "Sarpsborg": "薩普斯堡", "Bodo/Glimt": "波杜基林特",
    "Al-Ettifaq": "伊提法克", "Seoul": "FC首爾", "Northampton": "諾咸頓", "Ettifaq": "伊提法克"
}

def hard_translate(text):
    for eng, hkg in TRANSLATION.items():
        text = text.replace(eng, hkg)
    return text.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核心救命引擎 =================
def get_final_money_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 救命報表】\n========================\n\n"
    used_teams = set()

    # --- A. 💎 核武波膽 (暴力重試，直到出貨) ---
    report += "💎 【核武：8x-60x 波膽狙擊】\n"
    for _ in range(3):
        try:
            cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"}, timeout=None)
            if cs_res.status_code == 200:
                c = 0
                for m in cs_res.json():
                    if c >= 5: break
                    h, a = m['home_team'], m['away_team']
                    picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 60.0]
                    if picks:
                        report += f"📍 {hard_translate(h)} 對 {hard_translate(a)} | {picks[0]['name']} | {picks[0]['price']}x\n"
                        used_teams.update([h, a])
                        c += 1
                if c > 0: break
        except: time.sleep(1)

    # --- B. ✅ 穩定組合 (2.0x+ 且不重複球隊) ---
    try:
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"}, timeout=None)
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【穩定：5-7 串 1 (2.0x+)】\n"
            v = 0
            for m in h2h_data:
                h, a = m['home_team'], m['away_team']
                if v >= 6: break
                if h in used_teams or a in used_teams: continue
                
                valid = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.5]
                if valid:
                    report += f"🔹 {hard_translate(h)} 對 {hard_translate(a)} | {hard_translate(valid[0]['name'])} | {valid[0]['price']}x\n"
                    used_teams.update([h, a])
                    v += 1

            # --- C. 🚨 資金監控 (去重版) ---
            report += "\n🚨 【資金異常突襲】\n"
            monitored = set()
            for m in h2h_data[:25]:
                h = m['home_team']
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.01 <= o['price'] <= 1.35 and h not in monitored:
                        report += f"⚠️ 壓飛: {hard_translate(h)} ({o['price']}x)\n"
                        monitored.add(h)
    except: pass

    return report

# ================= 4. TG 控制 =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    # 提示先行
    bot.send_message(CHAT_ID, "☢️ 核武系統啟動，正在挖高倍波膽 (拒絕超時)...")
    bot.send_message(CHAT_ID, get_final_money_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：4.15 救命版")
if st.button("🔥 立即全功能救命掃描"):
    st.code(get_final_money_report())
