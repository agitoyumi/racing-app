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

# ================= 2. 專注譯名 =================
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

# ================= 3. 核心引擎 (專注唯一性) =================
def get_final_rescue_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 最終專注報表】\n========================\n\n"
    used_match_names = set() # 確保場次唯一

    # --- A. 💎 核武波膽 (優先執行) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            cs_data = cs_res.json()
            report += "💎 【核武：高倍波膽狙擊】\n"
            c = 0
            for m in cs_data:
                if c >= 4: break
                m_title = f"{m['home_team']} vs {m['away_team']}"
                # 篩選 8-60x 正常波膽，拒絕 1001x 垃圾
                picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 60.0]
                if picks:
                    report += f"📍 {hard_translate(m_title)} | {picks[0]['name']} | {picks[0]['price']}x\n"
                    used_match_names.add(m['home_team'])
                    used_match_names.add(m['away_team'])
                    c += 1
    except: report += "⚠️ 核武模組離線\n"

    time.sleep(1.2)

    # --- B. ✅ 穩定組合 (沿用 20:37 成功邏輯) ---
    try:
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【穩定：5-7 串 1 精選 (2.0x+)】\n"
            v = 0
            for m in h2h_data:
                if v >= 7: break
                # 物理檢查：核武用過嘅隊，穩定盤唔准再用
                if m['home_team'] in used_match_names or m['away_team'] in used_match_names: continue
                
                valid = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.5]
                if valid:
                    m_title = f"{m['home_team']} 對 {m['away_team']}"
                    report += f"🔹 {hard_translate(m_title)} | {hard_translate(valid[0]['name'])} | {valid[0]['price']}x\n"
                    used_match_names.add(m['home_team'])
                    used_match_names.add(m['away_team'])
                    v += 1

            # --- C. 🚨 資金監控 ---
            report += "\n🚨 【資金異常熱錢監控】\n"
            for m in h2h_data[:15]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.01 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {hard_translate(m['home_team'])} ({o['price']}x)\n"
    except: report += "⚠️ 穩定模組離線\n"

    return report

# ================= 4. TG 啟動 (死命令：提示必須先發) =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    # 先發氣勢提示
    bot.send_message(CHAT_ID, "☢️ 核武系統啟動，正在幫老闆挖出所有高倍波膽...")
    # 延遲 1 秒確保提示先出
    time.sleep(1)
    # 再發完整報表
    bot.send_message(CHAT_ID, get_final_rescue_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：4.15 專注完整版")
if st.button("🔥 立即執行全功能救亡掃描"):
    st.code(get_final_rescue_report())
