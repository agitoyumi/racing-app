import requests
import telebot
import streamlit as st
import time

# ================= 1. 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 

bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 中文譯名對照 (更完整) =================
TRANSLATION_MAP = {
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Molde": "莫迪", "Brann": "白蘭恩",
    "Real Madrid": "皇家馬德里", "Barcelona": "巴塞隆拿", "Man City": "曼城", "Arsenal": "阿仙奴",
    "Liverpool": "利物浦", "Chelsea": "車路士", "Bayern": "拜仁", "Dortmund": "多蒙特"
}

def translate(name):
    for eng, hkg in TRANSLATION_MAP.items():
        if eng in name: return name.replace(eng, hkg)
    return name

st.set_page_config(page_title="獵人 v8.0 終極版", layout="wide")
st.title("🏹 獵人狙擊：最後一擊 (100% 避開 422)")

# ================= 3. 核心功能 =================
if st.button("🚀 執行精確掃描 (只攞今晚精華)"):
    final_report = "🚀 【老闆，獵人精選報表！】\n"
    final_report += "========================\n\n"
    
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    
    # 策略：分兩次攞，每次只攞最熱門嘅場次
    with st.spinner('📡 掃描中...'):
        try:
            # 攞波膽
            res1 = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "correct_score", "oddsFormat": "decimal"})
            if res1.status_code == 200:
                final_report += "💎 【300x-500x 波膽狙擊】\n"
                # 只處理前 5 場最熱門賽事，防止數據量過大報 422
                for m in res1.json()[:5]:
                    m_name = translate(f"{m['home_team']} 對 {m['away_team']}")
                    for b in m['bookmakers'][:1]:
                        for o in b['markets'][0]['outcomes']:
                            if 8.0 <= o['price'] <= 25.0:
                                final_report += f"📍 {m_name}\n   👉 {o['name']} | {o['price']}x\n"
            
            time.sleep(1) # 停一秒

            # 攞獨贏
            res2 = requests.get(url, params={"apiKey": API_KEY, "regions": "uk", "markets": "h2h", "oddsFormat": "decimal"})
            if res2.status_code == 200:
                final_report += "\n✅ 【5x1 / 7x1 精選】\n"
                for m in res2.json()[:8]:
                    m_name = translate(f"{m['home_team']} 對 {m['away_team']}")
                    for b in m['bookmakers'][:1]:
                        for o in b['markets'][0]['outcomes']:
                            if 2.0 <= o['price'] <= 3.5:
                                final_report += f"🔹 {m_name} | {o['name']} | {o['price']}x\n"
                                break # 一場攞一個推薦就好
            
            # 最終輸出
            st.code(final_report)
            bot.send_message(CHAT_ID, final_report)
            st.balloons()
            st.success("🎯 數據已成功推送到 Telegram！")
            
        except Exception as e:
            st.error(f"連線出錯：{e}")

st.divider()
st.caption("老闆，如果今次再 422，我就直接用手寫報表畀你！貼上呢份，11 點見！")
