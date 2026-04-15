import requests
import telebot
import streamlit as st
import time

# ================= 1. 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 

bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會化譯名工具 =================
TRANSLATION_MAP = {
    "Real Madrid": "皇家馬德里", "Barcelona": "巴塞隆拿", "Man City": "曼城", "Man Utd": "曼聯",
    "Liverpool": "利物浦", "Arsenal": "阿仙奴", "Chelsea": "車路士", "Bayern": "拜仁",
    "PSG": "巴黎聖日耳門", "Inter": "國際米蘭", "Milan": "AC米蘭", "Juventus": "祖雲達斯",
    "Tottenham": "熱刺", "Dortmund": "多蒙特", "Leverkusen": "利華古遜", "Roma": "羅馬",
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Molde": "莫迪", "Brann": "白蘭恩"
}

def translate(name):
    for eng, hkg in TRANSLATION_MAP.items():
        if eng in name: return name.replace(eng, hkg)
    return name

st.set_page_config(page_title="獵人 v7.0", layout="wide")
st.title("🏹 獵人狙擊：分段收割版 (防 422)")

# ================= 3. 核心功能 =================
if st.button("🔥 啟動分段掃描 (300x + 5串1)"):
    report = "🚀 【老闆，獵人全火力回歸！】\n"
    report += "========================\n\n"
    
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    
    # --- 第一階段：波膽 (避開 422) ---
    with st.spinner('📡 正在掃描 300x 波膽...'):
        res1 = requests.get(url, params={"apiKey": API_KEY, "regions": "uk,eu", "markets": "correct_score", "oddsFormat": "decimal"})
        if res1.status_code == 200:
            report += "💎 【300x - 500x 波膽組合】\n"
            data1 = res1.json()
            for m in data1[:10]:
                m_name = translate(f"{m['home_team']} 對 {m['away_team']}")
                for b in m['bookmakers'][:1]:
                    for mkt in b['markets']:
                        for o in mkt['outcomes']:
                            if 8.0 <= o['price'] <= 20.0:
                                report += f"📍 {m_name}\n   👉 {o['name']} | {o['price']}x\n"
        else:
            st.error(f"波膽抓取失敗: {res1.status_code}")

    time.sleep(1) # 呼吸一秒，防止 API 封鎖

    # --- 第二階段：獨贏 (避開 422) ---
    with st.spinner('🔥 正在掃描 5-7 串 1...'):
        res2 = requests.get(url, params={"apiKey": API_KEY, "regions": "uk,eu", "markets": "h2h", "oddsFormat": "decimal"})
        if res2.status_code == 200:
            report += "\n✅ 【高勝率 5x1 / 7x1 (2.0x+)】\n"
            data2 = res2.json()
            for m in data2[:15]:
                m_name = translate(f"{m['home_team']} 對 {m['away_team']}")
                for b in m['bookmakers'][:1]:
                    for mkt in b['markets']:
                        for o in mkt['outcomes']:
                            if 2.0 <= o['price'] <= 3.5:
                                report += f"🔹 {m_name} | {o['name']} | {o['price']}x\n"
        else:
            st.error(f"獨贏抓取失敗: {res2.status_code}")

    # --- 顯示與發送 ---
    st.code(report)
    try:
        bot.send_message(CHAT_ID, report)
        st.balloons()
        st.success("🎯 數據已全數推送到 Telegram！")
    except Exception as e:
        st.error(f"TG 失敗: {e}")
