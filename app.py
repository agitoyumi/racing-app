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
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Bragantino": "保地花高SP",
    "Ulsan": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 硬核數據提取邏輯 =================
def run_honor_hunt():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🏹 【獵人：尊嚴重組・4.15 終極報表】\n"
    report += "========================\n\n"
    
    # --- Part A: 波膽 (強制等待與重試) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：300x+ 波膽狙擊】\n"
            cs_count = 0
            for m in cs_res.json():
                if cs_count >= 5: break
                m_name = to_hkjc(f"{m['home_team']} vs {m['away_team']}")
                # 嚴格篩選波膽區間 (8.5x - 25x)
                valid_cs = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.5 <= o['price'] <= 25.0]
                if valid_cs:
                    report += f"📍 {m_name} | {valid_cs[0]['name']} | {valid_cs[0]['price']}x\n"
                    cs_count += 1
            if cs_count == 0: report += "⚠️ 當前時段未搵到符合 8.5x+ 嘅優質波膽。\n"
        
        time.sleep(2.0) # 給予 API 充足休息，避開 422 兼保證 H2H 載入

        # --- Part B: 穩定組合 (2.0x 以上) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【穩定：5-7 串 1 (2.0x+)】\n"
            h2h_count = 0
            for m in h2h_data:
                if h2h_count >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 絕不妥協：只要高過 2.05x 嘅盤
                best_picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.05 <= o['price'] <= 4.0]
                if best_picks:
                    report += f"🔹 {m_name} | {to_hkjc(best_picks[0]['name'])} | {best_picks[0]['price']}x\n"
                    h2h_count += 1

            report += "\n🚨 【資金異常突襲 (只顯重要預警)】\n"
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 只顯示 1.1x 到 1.35x 嘅「真正」壓飛場次，低過 1.1x 嘅垃圾直接棄掉
                    if 1.10 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
    except Exception as e:
        return f"❌ 掃描失敗：{e}"
    
    return report

# ================= 4. 監聽與介面 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 正在用最後嘅尊嚴進行全網掃描...")
    bot.send_message(CHAT_ID, run_honor_hunt())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：尊嚴收復版")
if st.button("🔥 執行全火力深度掃描"):
    st.code(run_honor_hunt())
