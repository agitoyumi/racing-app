import requests
import telebot
import streamlit as st

# ================= 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人終極回歸", layout="wide")
st.title("🏹 獵人狙擊系統：暴力收割版")

def fetch_all_markets(m_type):
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {"apiKey": API_KEY, "regions": "uk,eu,us", "markets": m_type, "oddsFormat": "decimal"}
    try:
        res = requests.get(url, params=params, timeout=20)
        return res.json() if res.status_code == 200 else []
    except: return []

if st.button("🔥 執行終極暴力掃描 (不放過任何組合)"):
    full_report = "🚀 【老闆，獵人全火力回歸！】\n"
    full_report += "========================\n\n"
    
    with st.spinner('📡 正在暴力抓取全球波膽...'):
        scores = fetch_all_markets("correct_score")
        full_report += "💎 【300x - 500x 波膽狙擊】\n"
        count = 0
        for m in scores:
            if count >= 8: break # 攞多啲畀老闆揀
            for b in m['bookmakers'][:1]: # 只攞第一個莊家
                for mkt in b['markets']:
                    for o in mkt['outcomes']:
                        if 8.0 <= o['price'] <= 25.0: # 放寬到 25 倍，更容易湊成 500x
                            full_report += f"📍 {m['home_team']} | {o['name']} | {o['price']}x\n"
                            count += 1
        
    with st.spinner('🔥 正在掃描 5x1 / 7x1 資金流...'):
        h2h = fetch_all_markets("h2h")
        full_report += "\n✅ 【5x1 / 7x1 精選 (2.0x+)】\n"
        v_count = 0
        for m in h2h:
            if v_count >= 10: break
            for b in m['bookmakers'][:1]:
                for mkt in b['markets']:
                    for o in mkt['outcomes']:
                        if 2.0 <= o['price'] <= 4.0:
                            full_report += f"🔹 {m['home_team']} vs {m['away_team']} | {o['name']} | {o['price']}x\n"
                            v_count += 1

        full_report += "\n🚨 【資金異常/熱錢警告】\n"
        for m in h2h[:5]:
            for b in m['bookmakers'][:1]:
                for mkt in b['markets']:
                    for o in mkt['outcomes']:
                        if o['price'] < 1.3:
                            full_report += f"⚠️ 熱錢湧入: {m['home_team']} ({o['price']}x)\n"

    st.code(full_report)
    try:
        bot.send_message(CHAT_ID, full_report)
        st.balloons()
        st.success("🎯 暴力報表已發送！今次大把嘢睇！")
    except Exception as e:
        st.error(f"TG 失敗: {e}")
