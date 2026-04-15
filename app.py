import requests
import telebot
import streamlit as st
import time

# ================= 1. 配置 (老闆 L) =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會譯名大辭典 (已大幅擴充) =================
HKJC_NAMES = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Molde": "莫迪", "Brann": "白蘭恩",
    "Ulsan Hyundai": "蔚山現代", "FC Seoul": "FC首爾", "Al-Nassr": "艾納斯", "Al-Ettifaq": "艾列迪法克",
    "Wimbledon": "溫布頓", "Stockport": "史托港", "Luton": "盧頓", "Arsenal": "阿仙奴",
    "Chelsea": "車路士", "Man City": "曼城", "Liverpool": "利物浦", "Man Utd": "曼聯",
    "Real Madrid": "皇家馬德里", "Barcelona": "巴塞隆拿", "Bayern": "拜仁慕尼黑", "Dortmund": "多蒙特"
}

def to_hkg(name):
    for eng, hkg in HKJC_NAMES.items():
        if eng in name: return name.replace(eng, hkg)
    return name

st.set_page_config(page_title="獵人最後反擊", layout="wide")
st.title("🏹 獵人：中文數據收割 (終極版)")

# ================= 3. 核心按鈕 =================
if st.button("🔥 立即全網掃描 (300倍+波膽+中文)"):
    report = "🚀 【老闆，獵人清單：全港馬會版】\n"
    report += "========================\n\n"
    
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    
    # --- 階段一：波膽 (300倍) ---
    with st.spinner('🔭 正在鎖定 300x 波膽...'):
        try:
            res1 = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score", "oddsFormat": "decimal"})
            if res1.status_code == 200:
                report += "💎 【終極 3 串 1 波膽組合 (300x+)】\n"
                for m in res1.json()[:10]: # 攞返多啲場次
                    m_name = to_hkg(f"{m['home_team']} vs {m['away_team']}")
                    for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                        if 9.0 <= o['price'] <= 18.0:
                            report += f"📍 {m_name}\n   👉 {o['name']} | {o['price']}x\n"
            time.sleep(1) # 避 429
            
            # --- 階段二：5x1 / 7x1 ---
            res2 = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h", "oddsFormat": "decimal"})
            if res2.status_code == 200:
                report += "\n✅ 【穩定收割：5-7 串 1 組合】\n"
                for m in res2.json()[:15]:
                    m_name = to_hkg(f"{m['home_team']} vs {m['away_team']}")
                    o = m['bookmakers'][0]['markets'][0]['outcomes'][0] # 取主隊或和
                    if 1.8 <= o['price'] <= 3.5:
                        report += f"🔹 {m_name} | {o['name']} | {o['price']}x\n"
            
            # --- 輸出 ---
            st.code(report)
            bot.send_message(CHAT_ID, report)
            st.success("🎯 中文清單已出爐，TG 響咗！")
        except Exception as e:
            st.error(f"系統出錯：{e}")

st.divider()
st.caption("老闆，一波三折我知你煩。呢份 Code 鎖死晒中文同 ID，11 點見！")
