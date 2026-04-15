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

# ================= 2. 強力譯名轉換 =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP"
}

def to_hkjc(name):
    res = name
    for eng, hkg in HKJC_MAP.items():
        if eng in res: res = res.replace(eng, hkg)
    return res.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核武數據提取引擎 (最後防線) =================
def fetch_perfect_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 終極完善報表】\n"
    report += "========================\n\n"
    
    # --- Part A: 核武波膽 (💎 必須出現) ---
    try:
        cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"})
        if cs_res.status_code == 200:
            cs_data = cs_res.json()
            report += "💎 【核武：300x+ 波膽狙擊】\n"
            cs_found = 0
            for m in cs_data:
                if cs_found >= 6: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 只篩選 8.5x - 25.0x 嘅優質波膽
                valid_cs = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.5 <= o['price'] <= 25.0]
                if valid_cs:
                    report += f"📍 {m_name} | {valid_cs[0]['name']} | {valid_cs[0]['price']}x\n"
                    cs_found += 1
            if cs_found == 0: report += "⚠️ 當前盤口波動中，請稍後再試。\n"
        
        time.sleep(2.0)

        # --- Part B: 2.0x+ 穩定組合 (硬性過濾) ---
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"})
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【高勝率：2.0x+ 尊嚴組合】\n"
            h2h_count = 0
            for m in h2h_data:
                if h2h_count >= 8: break
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                # 鋼鐵過濾器：只要大過或等於 2.00x，差 0.01 都唔准過
                valid_picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if o['price'] >= 2.00]
                if valid_picks:
                    # 揀賠率最高嗰個，務求回報最大化
                    pick = max(valid_picks, key=lambda x: x['price'])
                    report += f"🔹 {m_name} | {to_hkjc(pick['name'])} | {pick['price']}x\n"
                    h2h_count += 1

            report += "\n🚨 【資金異常突襲預警】\n"
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 只報 1.15 到 1.35 嘅「真預警」，廢除 1.01 垃圾
                    if 1.15 <= o['price'] <= 1.35:
                        report += f"⚠️ 壓飛: {to_hkjc(m['home_team'])} ({o['price']}x)\n"
    except Exception as e:
        report += f"❌ 系統錯誤: {str(e)}"
    
    return report

# ================= 4. TG 監聽恢復 =================
@bot.message_handler(commands=['check', 'start'])
def handle_commands(message):
    bot.reply_to(message, "🎯 收到！核武系統正式重啟，正在剔除所有垃圾數據...")
    bot.send_message(CHAT_ID, fetch_perfect_report())

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：4.15 終極完善解決版")
if st.button("🔥 執行深度物理掃描"):
    st.code(fetch_perfect_report())
