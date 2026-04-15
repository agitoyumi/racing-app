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
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Sarpsborg": "薩普斯堡", "Bodo/Glimt": "波杜基林特"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核武數據提取器 (物理級過濾) =================
def fetch_final_data():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：尊嚴重生・4.15 終極報表】\n"
    report += "========================\n\n"
    
    try:
        # --- A. 暴力獲取波膽 (Correct Score) ---
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：300x+ 波膽狙擊】\n"
            found_cs = 0
            for m in cs_res.json():
                if found_cs >= 5: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 硬性篩選波膽區間 8.0x - 25.0x
                valid_cs = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 25.0]
                if valid_cs:
                    report += f"📍 {m_name} | {valid_cs[0]['name']} | {valid_cs[0]['price']}x\n"
                    found_cs += 1
            if found_cs == 0: report += "⚠️ 當前時段未搵到符合 8x+ 嘅優質波膽。\n"
        
        time.sleep(2.0) # 避 422 緩衝

        # --- B. 穩定組合 (2.0x 以上硬過濾) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            report += "\n✅ 【高勝率：5-7 串 1 (2.0x+)】\n"
            found_h2h = 0
            for m in h2h_res.json():
                if found_h2h >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 重點：硬過濾！只要低過 2.0，呢場波我直接唔出！
                valid_picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 4.2]
                if valid_picks:
                    report += f"🔹 {m_name} | {to_hkjc(valid_picks[0]['name'])} | {valid_picks[0]['price']}x\n"
                    found_h2h += 1

            report += "\n🚨 【資金異常突襲監控】\n"
            for m in h2h_res.json()[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 只有 1.15 到 1.35 嘅「真熱錢」先准噴出嚟，其餘 1.01 垃圾全部 Block！
                    if 1.15 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛預警: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
    except Exception as e:
        report += f"❌ 系統錯誤: {str(e)}"
    
    return report

# ================= 4. 指令與啟動 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 數據清洗中... 低過 2.0x 嘅垃圾賠率已被我徹底丟棄！")
    bot.send_message(CHAT_ID, fetch_final_data())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：最後尊嚴版")
if st.button("🔥 執行全網物理掃描 (絕無 1.0x 垃圾)"):
    st.code(fetch_final_data())
