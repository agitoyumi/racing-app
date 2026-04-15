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

# ================= 2. 強力譯名 =================
HKJC_MAP = {"Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", "Stockport": "史托港", "Racing Club": "競賽會", "Ulsan": "蔚山現代", "Arsenal": "阿仙奴", "Bayern": "拜仁", "Brann": "白蘭恩"}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 物理粉碎引擎 =================
def get_strictly_clean_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 物理清洗報表】\n"
    report += "========================\n\n"
    
    try:
        # --- A. 暴力核武波膽 (8.0x - 80.0x) ---
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：8x-80x 波膽】\n"
            count = 0
            for m in cs_res.json():
                if count >= 6: break
                m_name = to_hkjc(f"{m['home_team']} vs {m['away_team']}")
                # 嚴禁超過 80 倍嘅垃圾數據
                valid_cs = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 80.0]
                if valid_cs:
                    report += f"📍 {m_name} | {valid_cs[0]['name']} | {valid_cs[0]['price']}x\n"
                    count += 1
        
        time.sleep(2.0)

        # --- B. 物理鎖死主客和 (1.95x - 8.0x) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            report += "\n✅ 【組合：2.0x-8.0x 嚴選】\n"
            v_count = 0
            for m in h2h_res.json():
                if v_count >= 8: break
                m_name = to_hkjc(f"{m['home_team']} vs {m['away_team']}")
                # 物理鎖定：主客和賠率如果大過 8 倍，肯定係垃圾或者已封盤數據
                valid_h2h = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 1.95 <= o['price'] <= 8.0]
                if valid_h2h:
                    report += f"🔹 {m_name} | {to_hkjc(valid_h2h[0]['name'])} | {valid_h2h[0]['price']}x\n"
                    v_count += 1
    except:
        report += "❌ 數據讀取故障"
    
    return report

# ================= 4. TG 控制 =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    bot.reply_to(message, "📡 物理粉碎 1001x 垃圾數據中，正生成真實 2.0x 報表...")
    bot.send_message(CHAT_ID, get_strictly_clean_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：物理粉碎垃圾版")
if st.button("🔥 執行物理硬過濾掃描"):
    st.code(get_strictly_clean_report())
