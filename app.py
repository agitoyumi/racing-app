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

# ================= 2. 晏晝最正嘅譯名 (死命令) =================
TRANSLATION = {
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓",
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Arsenal": "阿仙奴", "Sporting Lisbon": "士砵亭", "Bayern Munich": "拜仁慕尼黑",
    "Real Madrid": "皇家馬德里", "Sarpsborg": "薩普斯堡", "Bodo/Glimt": "波杜基林特",
    "Al-Ettifaq": "伊提法克", "Seoul": "FC首爾", "Northampton": "諾咸頓"
}

def hard_translate(text):
    for eng, hkg in TRANSLATION.items():
        text = text.replace(eng, hkg)
    return text.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核心救亡引擎 =================
def get_rescue_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 真心救亡報表】\n========================\n\n"
    used_matches = set() # 紀錄用過嘅場次，防止重複

    # --- A. 💎 核武波膽 (8x - 80x) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：高倍波膽狙擊】\n"
            count = 0
            for m in cs_res.json():
                m_id = f"{m['home_team']}_{m['away_team']}"
                if count >= 4: break
                # 篩選合理高倍
                picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 80.0]
                if picks:
                    m_name = hard_translate(f"{m['home_team']} 對 {m['away_team']}")
                    report += f"📍 {m_name} | {picks[0]['name']} | {picks[0]['price']}x\n"
                    used_matches.add(m_id) # 標記呢場用咗，下面唔准再出
                    count += 1
    except: report += "⚠️ 核武模組離線\n"

    time.sleep(1.5)

    # --- B. ✅ 穩定組合 (2.0x+ 鋼鐵過濾) ---
    try:
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【高勝率：2.0x+ 組合】\n"
            v_count = 0
            for m in h2h_data:
                m_id = f"{m['home_team']}_{m['away_team']}"
                if v_count >= 6: break
                if m_id in used_matches: continue # 如果核武出咗呢場，穩定盤就唔准出
                
                # 只攞 2.0 到 8.0 之間
                valid = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.0]
                if valid:
                    m_name = hard_translate(f"{m['home_team']} 對 {m['away_team']}")
                    report += f"🔹 {m_name} | {hard_translate(valid[0]['name'])} | {valid[0]['price']}x\n"
                    used_matches.add(m_id)
                    v_count += 1

            # --- C. 🚨 資金監控 ---
            report += "\n🚨 【資金突襲：大戶監控】\n"
            for m in h2h_data[:15]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.01 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {hard_translate(m['home_team'])} ({o['price']}x)\n"
    except: report += "⚠️ 穩定模組離線\n"

    return report

# ================= 4. TG 啟動 (恢復晏晝氣勢) =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    bot.send_message(CHAT_ID, "☢️ 核武系統啟動，正在幫老闆挖出所有高倍波膽...")
    bot.send_message(CHAT_ID, get_rescue_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：救亡整合版")
st.write("已修正重複場次、補回核武、鎖定 2.0x+ 門檻。")
if st.button("🔥 全功能救亡掃描"):
    st.code(get_rescue_report())
