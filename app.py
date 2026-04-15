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

# ================= 2. 馬會中文大翻譯 =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓",
    "Brann": "白蘭恩", "Molde": "莫迪", "Viking": "維京"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 嚴格篩選邏輯 =================
def run_strict_hunter():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人回報：2.0x+ 專攻版】\n"
    report += "========================\n\n"
    
    try:
        # --- A. 真正的核武波膽 (8x - 20x) ---
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if res_cs.status_code == 200:
            report += "💎 【核武：300x+ 波膽狙擊】\n"
            cs_count = 0
            for m in res_cs.json():
                if cs_count >= 6: break
                m_name = to_hkjc(f"{m['home_team']} vs {m['away_team']}")
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 只攞 8.5 到 18 倍，最靚嘅波膽位
                    if 8.5 <= o['price'] <= 18.0:
                        report += f"📍 {m_name} | {o['name']} | {o['price']}x\n"
                        cs_count += 1
                        break
        
        time.sleep(1.2)

        # --- B. 嚴格 2.0x+ 組合 (5-7 串 1) ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if res_h2h.status_code == 200:
            h2h_data = res_h2h.json()
            report += "\n✅ 【高勝率：5-7 串 1 (2.0x+)】\n"
            v_count = 0
            for m in h2h_data:
                if v_count >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 喺呢場波搵任何一個大過 2.0 嘅盤口（主/客/和）
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 2.05 <= o['price'] <= 3.8: # 門檻鎖死 2.05 以上
                        report += f"🔹 {m_name} | {to_hkjc(o['name'])} | {o['price']}x\n"
                        v_count += 1
                        break

            report += "\n🚨 【資金異常熱錢監控】\n"
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if o['price'] < 1.30: # 呢啲先係真正有熱錢嘅場次
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
        
        return report
    except Exception as e:
        return f"❌ 系統錯誤: {str(e)}"

@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 門檻已鎖死 2.0x+，正在為老闆過濾垃圾數據...")
    bot.send_message(CHAT_ID, run_strict_hunter())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：2.0x+ 尊嚴修正版")
if st.button("🔥 執行嚴格掃描"):
    st.code(run_strict_hunter())
