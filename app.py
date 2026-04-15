import requests
import telebot
import streamlit as st

# ================= 1. 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 

bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會譯名大數據庫 =================
HKJC_MAP = {
    # 聯賽
    "Premier League": "英超", "La Liga": "西甲", "Serie A": "意甲", "Bundesliga": "德甲",
    # 球隊 (針對你截圖見到嘅波)
    "Wimbledon": "溫布頓", "Stockport County FC": "史托港", "Racing Club": "競賽會",
    "Botafogo": "保地花高", "Ulsan Hyundai FC": "蔚山現代", "FC Seoul": "FC首爾",
    "Tromso": "特林素", "Lillestrom": "利尼史特朗", "Al-Nassr": "艾納斯",
    # 通用轉換
    " FC": "", " United": "聯", " City": "城", " Real": "皇家", " Atletico": "馬德里體育會"
}

def to_hkjc_name(name):
    # 先做全名匹配
    if name in HKJC_MAP:
        return HKJC_MAP[name]
    # 做關鍵字替換
    for eng, hkg in HKJC_MAP.items():
        if eng in name:
            name = name.replace(eng, hkg)
    return name

st.set_page_config(page_title="獵人馬會專用版", layout="wide")
st.title("🏹 獵人狙擊系統：馬會繁中對照版")

# ================= 3. 數據核心 =================
if st.button("🚀 執行馬會對照掃描 (300x-500x)"):
    report = "🚀 【老闆，馬會繁中清單到！】\n"
    report += "========================\n\n"
    
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {"apiKey": API_KEY, "regions": "uk,eu", "markets": "h2h,correct_score", "oddsFormat": "decimal"}
    
    with st.spinner('🔭 正在翻譯馬會譯名中...'):
        try:
            res = requests.get(url, params=params, timeout=20)
            if res.status_code == 200:
                data = res.json()
                
                # 篩選波膽 (300x)
                report += "💎 【深夜 300x 波膽狙擊】\n"
                s_count = 0
                for m in data:
                    if s_count >= 5: break
                    h = to_hkjc_name(m['home_team'])
                    a = to_hkjc_name(m['away_team'])
                    for b in m['bookmakers'][:1]:
                        for mkt in b['markets']:
                            if mkt['key'] == 'correct_score':
                                for o in mkt['outcomes']:
                                    if 8.5 <= o['price'] <= 18.0:
                                        report += f"📍 {h} 對 {a}\n   👉 預測：{o['name']} | {o['price']}x\n"
                                        s_count += 1

                # 篩選 5x1 / 7x1 組合
                report += "\n✅ 【高勝率 5x1 / 7x1 (馬會版)】\n"
                v_count = 0
                for m in data:
                    if v_count >= 8: break
                    h = to_hkjc_name(m['home_team'])
                    a = to_hkjc_name(m['away_team'])
                    for b in m['bookmakers'][:1]:
                        for mkt in b['markets']:
                            if mkt['key'] == 'h2h':
                                for o in mkt['outcomes']:
                                    if 2.2 <= o['price'] <= 3.8:
                                        report += f"🔹 {h} 對 {a} | {o['name']} | {o['price']}x\n"
                                        v_count += 1
                
                st.code(report)
                bot.send_message(CHAT_ID, report)
                st.balloons()
                st.success("🎯 繁中報表已推送至 Telegram！")
            else:
                st.error(f"API Error: {res.status_code}")
        except Exception as e:
            st.error(f"錯誤：{e}")
