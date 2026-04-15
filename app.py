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

# ================= 2. 強力譯名 (死命令) =================
TRANSLATION = {
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Luton": "盧頓",
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Botafogo": "保地花高SP",
    "Arsenal": "阿仙奴", "Sporting Lisbon": "士砵亭", "Bayern Munich": "拜仁慕尼黑",
    "Real Madrid": "皇家馬德里", "Sarpsborg": "薩普斯堡", "Bodo/Glimt": "波杜基林特",
    "Al-Ettifaq": "伊提法克", "Seoul": "FC首爾", "Northampton": "諾咸頓"
}

def hard_translate(text):
    for eng, hkg in TRANSLATION.items():
        text = text.replace(eng, hkg)
    return text.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 核心報表 (核武優先) =================
def get_atomic_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🚀 【獵人：4.15 核武強制回歸報表】\n========================\n\n"
    used_match_ids = set()

    # --- A. 💎 核武波膽 (優先執行，攞唔到就再攞) ---
    for _ in range(2): # 嘗試兩次，確保波膽必出
        try:
            cs_res = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"}, timeout=10)
            if cs_res.status_code == 200:
                report += "💎 【核武：8x-60x 波膽狙擊】\n"
                cs_data = cs_res.json()
                c = 0
                for m in cs_data:
                    if c >= 5: break
                    m_id = f"{m['home_team']}_{m['away_team']}"
                    # 篩選 8-60x 波膽，物理攔截 1001x 垃圾
                    picks = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 8.0 <= o['price'] <= 60.0]
                    if picks:
                        m_name = hard_translate(f"{m['home_team']} 對 {m['away_team']}")
                        report += f"📍 {m_name} | {picks[0]['name']} | {picks[0]['price']}x\n"
                        used_match_ids.add(m_id)
                        c += 1
                break # 成功攞到就跳出重試迴圈
        except:
            time.sleep(2)
            continue
    
    if "💎" not in report: report += "⚠️ 核武波膽數據獲取超時，請稍後重試。\n"

    time.sleep(2) # 緩衝，避免 422

    # --- B. ✅ 穩定組合 (鋼鐵 2.0x+ / 絕不重複場次) ---
    try:
        h2h_res = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"}, timeout=10)
        if h2h_res.status_code == 200:
            h2h_data = h2h_res.json()
            report += "\n✅ 【穩定：5-7 串 1 (2.0x+)】\n"
            v = 0
            for m in h2h_data:
                m_id = f"{m['home_team']}_{m['away_team']}"
                if v >= 7: break
                if m_id in used_match_ids: continue # 絕對不准重複
                
                valid = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.5]
                if valid:
                    m_name = hard_translate(f"{m['home_team']} 對 {m['away_team']}")
                    report += f"🔹 {m_name} | {hard_translate(valid[0]['name'])} | {valid[0]['price']}x\n"
                    used_match_ids.add(m_id)
                    v += 1

            # --- C. 🚨 資金監控 (唯一球隊版) ---
            report += "\n🚨 【資金異常突襲監控】\n"
            seen_mon = set()
            for m in h2h_data[:20]:
                h = m['home_team']
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 1.01 <= o['price'] <= 1.35 and h not in seen_mon:
                        report += f"⚠️ 壓飛: {hard_translate(h)} ({o['price']}x)\n"
                        seen_mon.add(h)
    except: pass

    return report

# ================= 4. TG 控制 (氣勢回歸) =================
@bot.message_handler(commands=['check', 'start'])
def handle_check(message):
    # 死命令：第一時間噴提示
    bot.send_message(CHAT_ID, "☢️ 核武系統啟動，正在為老闆挖出所有高倍波膽...")
    # 算數據
    msg = get_atomic_report()
    bot.send_message(CHAT_ID, msg)

def start_bot():
    bot.infinity_polling()

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=start_bot, daemon=True)
    st.session_state.bot_thread.start()

st.title("🏹 獵人：4.15 核武強制歸位版")
if st.button("🔥 立即全功能救亡掃描"):
    st.code(get_atomic_report())
