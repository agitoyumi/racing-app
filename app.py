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
    "Real Madrid": "皇家馬德里", "Sarpsborg FK": "薩普斯堡", "Bodo/Glimt": "波杜基林特"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核心報表引擎 (晏晝底 + 新核武) =================
def get_combined_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 終極整合報表】\n"
    report += "========================\n\n"
    
    try:
        # --- A. 💎 核武波膽 (8x - 60x 嚴選) ---
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report += "💎 【核武：高倍波膽狙擊】\n"
            cs_count = 0
            for m in cs_res.json():
                if cs_count >= 5: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 篩選合理高倍波膽
                valid_cs = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 60.0]
                if valid_cs:
                    report += f"📍 {m_name} | {valid_cs[0]['name']} | {valid_cs[0]['price']}x\n"
                    cs_count += 1
        
        time.sleep(1.5)

        # --- B. ✅ 穩定組合 (恢復晏晝排版 + 2.0x 鋼鐵過濾) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【高勝率：5-7 串 1 (2.0x+)】\n"
            v_count = 0
            for m in h2h_data:
                if v_count >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 鋼鐵門檻：只攞 2.0 到 8.0 之間嘅 H2H
                valid_h2h = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.0]
                if valid_h2h:
                    report += f"🔹 {m_name} | {to_hkjc(valid_h2h[0]['name'])} | {valid_h2h[0]['price']}x\n"
                    v_count += 1

            # --- C. 🚨 晏晝版資金流監控 ---
            report += "\n🚨 【資金突襲監控：大戶去向】\n"
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 恢復晏晝睇開嘅熱錢範圍
                    if 1.10 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"

    except Exception as e:
        report += f"❌ 系統暫時忙碌: {str(e)}"
    
    return report

# ================= 4. TG 提示恢復 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.send_message(CHAT_ID, "🎯 收到！核武系統啟動，正在整合晏晝版優質數據...")
    bot.send_message(CHAT_ID, get_combined_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：4.15 整合重生版")
st.write("已找回晏晝譯名及資金監控，並鎖定 2.0x+ 及高倍波膽。")
if st.button("🔥 執行全火力整合掃描"):
    st.code(get_combined_report())
