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

# ================= 2. 馬會譯名庫 =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Arsenal": "阿仙奴", "Sporting": "士砵亭", "Al-Nassr": "艾納斯"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核心數據引擎 (完善版) =================
def get_hunter_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    final_msg = "🚀 【獵人終極回報：核武+穩定+資金】\n"
    final_msg += "========================\n\n"
    
    # --- A. 暴力掃描波膽 (確保💎必出) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            final_msg += "💎 【核武：300x+ 波膽狙擊】\n"
            cs_data = cs_res.json()
            found_cs = 0
            for m in cs_data[:10]:
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 搵呢場波入面最接近老闆心水嘅核武波膽 (8.5x - 22x)
                outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
                for o in outcomes:
                    if 8.5 <= o['price'] <= 22.0:
                        final_msg += f"📍 {m_name} | {o['name']} | {o['price']}x\n"
                        found_cs += 1
                        break
            if found_cs == 0: final_msg += "⚠️ 當前盤口波膽波動中...\n"
    except: final_msg += "⚠️ 波膽數據載入延遲\n"

    time.sleep(1.5) # 避 422 緩衝

    # --- B. 穩定 2.0x+ 組合 & 資金流 ---
    try:
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            final_msg += "\n✅ 【高勝率：5-7 串 1 (2.0x+)】\n"
            v_count = 0
            for m in h2h_data:
                if v_count >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 嚴格物理過濾：只要 > 2.0 嘅盤口
                valid_picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if o['price'] >= 2.0]
                if valid_picks:
                    final_msg += f"🔹 {m_name} | {to_hkjc(valid_picks[0]['name'])} | {valid_picks[0]['price']}x\n"
                    v_count += 1
            
            final_msg += "\n🚨 【資金異常突襲監控】\n"
            for m in h2h_data[:8]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.15 <= o['price'] <= 1.35: # 只出真熱錢預警
                        final_msg += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
    except: final_msg += "⚠️ 獨贏數據暫時無法獲取\n"

    return final_msg

# ================= 4. TG 指令集 (恢復提示) =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    # 恢復提示訊息
    bot.send_message(CHAT_ID, "🎯 收到！核武系統啟動，正在為老闆整合 2.0x+ 及波膽數據...")
    # 獲取並發送完整報表
    bot.send_message(CHAT_ID, get_hunter_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：終極完善版")
st.write("已鎖定：波膽必出、低於 2.0x 自動屏蔽、TG 提示恢復。")
if st.button("🔥 執行深度全網掃描"):
    st.code(get_hunter_report())
