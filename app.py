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
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核武數據提取器 =================
def fetch_data():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 深夜全功能報表】\n"
    report += "========================\n\n"
    
    # --- Part A: 暴力波膽 (強制追索) ---
    try:
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if res_cs.status_code == 200:
            report += "💎 【核武：300x+ 波膽組合】\n"
            cs_data = res_cs.json()
            found_cs = 0
            for m in cs_data:
                if found_cs >= 6: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 喺呢場波入面搵符合 8.5x - 22x 嘅波膽
                outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
                for o in outcomes:
                    if 8.5 <= o['price'] <= 22.0:
                        report += f"📍 {m_name} | {o['name']} | {o['price']}x\n"
                        found_cs += 1
                        break
        time.sleep(1.5) # 避 422 緩衝
        
        # --- Part B: 穩定 5-7 串 1 (絕無 2.0x 以下垃圾) ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if res_h2h.status_code == 200:
            report += "\n✅ 【精選：2.0x+ 高倍組合】\n"
            h2h_data = res_h2h.json()
            found_h2h = 0
            for m in h2h_data:
                if found_h2h >= 8: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 嚴格篩選：只攞 2.05x 以上嘅結果
                valid_picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.05 <= o['price'] <= 4.5]
                if valid_picks:
                    pick = valid_picks[0]
                    report += f"🔹 {m_name} | {to_hkjc(pick['name'])} | {pick['price']}x\n"
                    found_h2h += 1

            report += "\n🚨 【資金異常流向】\n"
            for m in h2h_data[:8]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if o['price'] < 1.30: # 只顯示真正壓飛嘅場次
                        report += f"⚠️ 莊家壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
    except:
        report += "❌ 數據讀取超時，請再試一次。"
    
    return report

# ================= 4. 指令集 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 數據重新較準中，正在過濾垃圾賠率...")
    bot.send_message(CHAT_ID, fetch_data())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

# ================= 5. Streamlit =================
st.set_page_config(page_title="獵人最後尊嚴版")
st.title("🏹 獵人：422 徹底解決版")
if st.button("🔥 立即全網掃描 (保證波膽+2.0x)"):
    st.code(fetch_data())
