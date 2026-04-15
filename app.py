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

# ================= 2. 馬會譯名 (深夜鎖定) =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Arsenal": "阿仙奴", "Bayern": "拜仁", "Real Madrid": "皇家馬德里"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 全火力功能函數 =================
def run_final_hunt():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人終極回報：核武全開】\n"
    report += "========================\n\n"
    
    # --- A. 暴力波膽 (唔出唔收工) ---
    try:
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if res_cs.status_code == 200:
            report += "💎 【核武：300x+ 波膽狙擊】\n"
            cs_data = res_cs.json()
            found_cs = 0
            for m in cs_data:
                if found_cs >= 8: break # 俾多幾場老闆揀
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 直接攞呢場波最高賠率嗰幾個波膽 (8x - 25x)
                outcomes = sorted(m['bookmakers'][0]['markets'][0]['outcomes'], key=lambda x: x['price'], reverse=True)
                for o in outcomes:
                    if 8.5 <= o['price'] <= 22.0:
                        report += f"📍 {m_name} | {o['name']} | {o['price']}x\n"
                        found_cs += 1
                        break
        time.sleep(1.5) # 休息避 422
        
        # --- B. 穩定組合 (2.0x 以上嚴格執行) ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if res_h2h.status_code == 200:
            report += "\n✅ 【高勝率：5-7 串 1 (2.0x+)】\n"
            h2h_data = res_h2h.json()
            found_h2h = 0
            for m in h2h_data:
                if found_h2h >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 嚴格篩選：低過 2.0 唔準出！
                    if 2.05 <= o['price'] <= 4.0:
                        report += f"🔹 {m_name} | {to_hkjc(o['name'])} | {o['price']}x\n"
                        found_h2h += 1
                        break
                        
            report += "\n🚨 【資金突襲監控】\n"
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if o['price'] < 1.35:
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
    except Exception as e:
        report += f"❌ 獲取失敗: {str(e)}"
    
    return report

# ================= 4. TG 監聽 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 怒火系統啟動！波膽同高倍數盤口一併奉上...")
    bot.send_message(CHAT_ID, run_final_hunt())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：終極怒火重生版")
if st.button("🔥 執行全火力掃描"):
    st.code(run_final_hunt())
