import requests
import telebot
import streamlit as st
import time

# ================= 1. 配置中心 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會中文翻譯 (針對今晚熱門) =================
HKJC_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Wimbledon": "AFC 溫布頓", 
    "Stockport": "史托港", "Racing Club": "競賽會", "Bragantino": "保地花高SP",
    "Arsenal": "阿仙奴", "Bayern": "拜仁", "Real Madrid": "皇家馬德里"
}

def to_hkjc(name):
    for eng, hkg in HKJC_MAP.items():
        if eng in name: return name.replace(eng, hkg)
    return name

st.set_page_config(page_title="獵人全功能系統", layout="wide")
st.title("🏹 獵人狙擊系統：300x + 5串1 + 資金流")

# ================= 3. 核心邏輯確認 =================
if st.button("🔥 啟動全功能深度掃描 (認真全開)"):
    report = f"🚀 【老闆，獵人清單：全功能收割版】\n"
    report += "========================\n\n"
    
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    
    with st.spinner('📡 掃描 300x 波膽中...'):
        # --- 功能 1: 300x-500x 波膽狙擊 (3串1) ---
        res_cs = requests.get(url, params={"apiKey": API_KEY, "regions": "eu", "markets": "correct_score", "oddsFormat": "decimal"})
        if res_cs.status_code == 200:
            report += "💎 【終極 3 串 1 波膽 (目標 300x+)】\n"
            for m in res_cs.json()[:12]:
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    # 篩選 9x-16x 波膽，3 場串埋即成 500x-1000x
                    if 9.0 <= o['price'] <= 16.0:
                        report += f"📍 {m_name} | {o['name']} | {o['price']}x\n"
        
        time.sleep(1) # 避開 422 關鍵動手

        # --- 功能 2 & 3: 5x1/7x1 (2.0x+) & 資金監控 ---
        res_h2h = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h", "oddsFormat": "decimal"})
        if res_h2h.status_code == 200:
            h2h_data = res_h2h.json()
            
            report += "\n✅ 【高勝率 5x1 / 7x1 組合 (2.0x+)】\n"
            for m in h2h_data[:15]:
                m_name = to_hkjc(f"{m['home_team']} 對 {m['away_team']}")
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if 2.1 <= o['price'] <= 3.8:
                        report += f"🔹 {m_name} | {o['name']} | {o['price']}x\n"
                        break
            
            report += "\n🚨 【資金異常/熱錢監控】\n"
            for m in h2h_data[:10]:
                for o in m['bookmakers'][0]['markets'][0]['outcomes']:
                    if o['price'] < 1.32: # 監控賠率異常低、熱錢湧入嘅場次
                        report += f"⚠️ 熱錢警戒: {to_hkjc(m['home_team'])} ({o['price']}x)\n"

    # --- 輸出結果 ---
    st.code(report)
    try:
        bot.send_message(CHAT_ID, report)
        st.balloons()
        st.success("🎯 數據已全數推送至 Telegram！")
    except Exception as e:
        st.error(f"TG 發送失敗: {e}")
