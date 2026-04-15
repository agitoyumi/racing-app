import requests, telebot, time, threading
import streamlit as st

# ================= 1. 配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3"
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742"
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會譯名庫 =================
MAP = {
    "Ulsan Hyundai": "蔚山現代", "Al-Nassr": "艾納斯", "Al-Ettifaq": "伊提法克", 
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Arsenal": "阿仙奴", 
    "Bayern": "拜仁", "Sarpsborg": "薩普斯堡", "Seoul": "FC首爾"
}

def trans(t):
    for k, v in MAP.items(): t = t.replace(k, v)
    return t.replace("Draw", "和局").replace(" vs ", " 對 ")

# ================= 3. 掃描引擎 =================
def get_report():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    report = "🎯 【獵人：4.15 獲利掃描】\n\n"
    used_teams = set()

    # --- A. 💎 核武 3x1 (300-500倍組合) ---
    try:
        r = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score"}, timeout=15)
        if r.status_code == 200:
            report += "💎 【核武 3x1 (瞄準 300x-500x)】\n"
            c = 0
            for m in r.json():
                if c >= 3: break # 只要3場組成3x1
                # 篩選 7x 到 15x 之間的波膽，組合起來大約就是幾百倍
                p = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 7.0 <= o['price'] <= 15.0]
                if p:
                    report += f"📍 {trans(m['home_team'])} vs {trans(m['away_team'])} | {p[0]['name']} | {p[0]['price']}x\n"
                    used_teams.update([m['home_team'], m['away_team']])
                    c += 1
    except: report += "⚠️ 3x1 模組暫時離線\n"

    # --- B. ✅ 穩定 6x1 (2.0x+ 系統) ---
    try:
        r = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h"}, timeout=15)
        if r.status_code == 200:
            report += "\n✅ 【穩定 6x1 (2.0x+ 組合)】\n"
            v = 0
            for m in r.json():
                h, a = m['home_team'], m['away_team']
                if v >= 6: break
                if h in used_teams or a in used_teams: continue
                sel = [o for o in m['bookmakers'][0]['markets'][0]['outcomes'] if 2.0 <= o['price'] <= 8.5]
                if sel:
                    report += f"🔹 {trans(h)} 對 {trans(a)} | {trans(sel[0]['name'])} | {sel[0]['price']}x\n"
                    used_teams.update([h, a]); v += 1
    except: pass
    
    return report

# ================= 4. TG Bot 通知 =================
@bot.message_handler(commands=['check', 'start'])
def run_bot(m):
    # 恢復晏晝的氣勢通知
    bot.send_message(CHAT_ID, "☢️ 核武系統啟動，正在挖出 300-500 倍 3x1 組合...")
    time.sleep(0.5)
    bot.send_message(CHAT_ID, get_report())

if 'bot_started' not in st.session_state:
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    st.session_state.bot_started = True

st.title("🏹 獵人：3x1 / 6x1 雙核版")
if st.button("🔥 執行專注掃描"):
    st.code(get_report())
