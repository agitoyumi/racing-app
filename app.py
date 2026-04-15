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

# ================= 3. 核心抓取邏輯 (暴力過濾垃圾) =================
def run_strict_hunt():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report_lines = ["🚀 【獵人：尊嚴重生・2.0x+ 嚴選】", "========================", ""]
    
    try:
        # --- A. 獲取波膽 (Correct Score) ---
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            report_lines.append("💎 【核武：300x+ 波膽狙擊】")
            count = 0
            for m in cs_res.json():
                if count >= 6: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 嚴格篩選波膽：只攞 8x 以上
                outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
                valid = [o for o in outcomes if o['price'] >= 8.0]
                if valid:
                    report_lines.append(f"📍 {m_name} | {valid[0]['name']} | {valid[0]['price']}x")
                    count += 1
        
        time.sleep(2.0)

        # --- B. 獲取獨贏 (H2H) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            
            # 1. 穩定 2.0x+ 組合
            report_lines.append("\n✅ 【穩定：5-7 串 1 (2.0x+)】")
            v_count = 0
            for m in h2h_data:
                if v_count >= 7: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 硬性物理過濾：低過 2.05x 直接唔睇
                best = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if o['price'] >= 2.05]
                if best:
                    report_lines.append(f"🔹 {m_name} | {to_hkjc(best[0]['name'])} | {best[0]['price']}x")
                    v_count += 1

            # 2. 資金異常 (屏蔽 1.1 以下垃圾)
            report_lines.append("\n🚨 【資金異常突襲】")
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 只顯示 1.15 到 1.35 嘅預警
                    if 1.15 <= o['price'] <= 1.35:
                        report_lines.append(f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)")

    except Exception as e:
        report_lines.append(f"❌ 數據錯誤: {str(e)}")

    return "\n".join(report_lines)

# ================= 4. 啟動服務 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 門檻物理鎖定 2.0x+，垃圾數據清除中...")
    bot.send_message(CHAT_ID, run_strict_hunt())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：2.0x 物理鎖死版")
if st.button("🔥 執行深度過濾掃描"):
    st.code(run_strict_hunt())
