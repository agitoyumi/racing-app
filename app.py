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

# ================= 2. 晏晝最正嘅譯名庫 =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓",
    "Arsenal": "阿仙奴", "Sporting Lisbon": "士砵亭", "Bayern Munich": "拜仁慕尼黑",
    "Real Madrid": "皇家馬德里", "Sarpsborg": "薩普斯堡", "Bodo/Glimt": "波杜基林特",
    "Seoul": "FC首爾", "Northampton": "諾咸頓"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 終極數據引擎 =================
def fetch_perfect_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 終極全功能報表】\n"
    report += "========================\n\n"
    
    # --- A. 💎 核武波膽 (保證出貨) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：8x-60x 波膽狙擊】\n"
            found_cs = 0
            for m in cs_res.json():
                if found_cs >= 5: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 嚴格鎖死 8-60x，踢走 1001x 垃圾
                valid_cs = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 60.0]
                if valid_cs:
                    report += f"📍 {m_name} | {valid_cs[0]['name']} | {valid_cs[0]['price']}x\n"
                    found_cs += 1
            if found_cs == 0: report += "⚠️ 波膽數據載入中...\n"
    except: report += "⚠️ 核武模組暫時離線\n"

    time.sleep(1.5)

    # --- B. ✅ 穩定組合 + 🚨 資金監控 (晏晝優點全保留) ---
    try:
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            
            report += "\n✅ 【高勝率：5-7 串 1 (2.0x+)】\n"
            v_count = 0
            for m in h2h_data:
                if v_count >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 鋼鐵門檻：H2H 必須喺 2.0x 到 8.0x 之間
                valid_h2h = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.0]
                if valid_h2h:
                    report += f"🔹 {m_name} | {to_hkjc(valid_h2h[0]['name'])} | {valid_h2h[0]['price']}x\n"
                    v_count += 1

            report += "\n🚨 【資金異常突襲：大戶去向】\n"
            for m in h2h_data[:12]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 恢復晏晝睇開嘅熱錢範圍
                    if 1.10 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
    except: report += "⚠️ 穩定盤模組暫時離線\n"

    return report

# ================= 4. TG 指令恢復 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 收到！正在整合所有功能（譯名+波膽+2.0x+資金流）...")
    bot.send_message(CHAT_ID, fetch_perfect_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：4.15 終極整合重生版")
if st.button("🔥 執行全功能掃描"):
    st.code(fetch_perfect_report())
