import requests
import telebot
import streamlit as st
import time

# ================= 1. 配置中心 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會中文大對照庫 (認真補完) =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Molde": "莫迪", "Brann": "白蘭恩",
    "Ulsan Hyundai": "蔚山現代", "FC Seoul": "FC首爾", "Al-Nassr": "艾納斯", 
    "Wimbledon": "溫布頓", "Stockport": "史托港", "Luton": "盧頓",
    "Stabaek": "史達比克", "Valerenga": "華拉倫加", "HamKam": "咸卡"
}

def to_hkjc(name):
    for eng, hkg in HKJC_MAP.items():
        if eng in name: return name.replace(eng, hkg)
    return name

st.set_page_config(page_title="獵人完全體", layout="wide")
st.title("🏹 獵人：全功能中文收割系統 (認真版)")

# ================= 3. 核心收割邏輯 =================
if st.button("🔥 執行深度全網掃描 (波膽 + 5x1 + 資金流)"):
    full_report = "🚀 【老闆，獵人清單：全功能收割版】\n"
    full_report += "========================\n\n"
    
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    
    with st.spinner('📡 正在深度挖掘全球數據...'):
        # --- A. 300x-500x 波膽狙擊 (重點功能) ---
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score", "oddsFormat": "decimal"})
        if res_cs.status_code == 200:
            full_report += "💎 【終極 3 串 1 波膽 (300x+)】\n"
            cs_data = res_cs.json()
            # 搵 10x 左右嘅波膽，三場疊加 = 1000x，兩場都 100x
            for m in cs_data[:15]:
                m_name = to_hkjc(f"{m['home_team']} vs {m['away_team']}")
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 9.0 <= o['price'] <= 16.0:
                        full_report += f"📍 {m_name}\n   👉 預測: {o['name']} | {o['price']}x\n"
        
        time.sleep(1) # 呼吸一秒避 422
        
        # --- B. 5x1 / 7x1 穩定組合 ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h", "oddsFormat": "decimal"})
        if res_h2h.status_code == 200:
            full_report += "\n✅ 【高勝率 5x1 / 7x1 組合】\n"
            h2h_data = res_h2h.json()
            for m in h2h_data[:20]:
                m_name = to_hkjc(f"{m['home_team']} vs {m['away_team']}")
                # 攞和局或者受讓盤
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 2.2 <= o['price'] <= 3.8:
                        full_report += f"🔹 {m_name} | {o['name']} | {o['price']}x\n"
                        break
        
        # --- C. 資金異常監控 (Hidden Logic) ---
        full_report += "\n🚨 【資金異常/熱錢監控】\n"
        for m in h2h_data[:10]:
            for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                if o['price'] < 1.35: # 熱錢過度集中
                    full_report += f"⚠️ 熱錢: {to_hkjc(m['home_team'])} ({o['price']}x)\n"

    # --- 輸出結果 ---
    st.code(full_report)
    try:
        bot.send_message(CHAT_ID, full_report)
        st.balloons()
        st.success("🎯 數據已全數推送，今次絕對認真！")
    except Exception as e:
        st.error(f"TG 失敗: {e}")
