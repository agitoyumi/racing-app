import requests
import telebot
import streamlit as st

# ================= 1. 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 

bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 馬會譯名對照表 (老闆專用) =================
TRANSLATION_MAP = {
    # 聯賽名
    "Premier League": "英超", "La Liga": "西甲", "Serie A": "意甲", "Bundesliga": "德甲",
    # 球隊名 (持續增加中)
    "Real Madrid": "皇家馬德里", "Barcelona": "巴塞隆拿", "Man City": "曼城", "Man Utd": "曼聯",
    "Liverpool": "利物浦", "Arsenal": "阿仙奴", "Chelsea": "車路士", "Bayern": "拜仁慕尼黑",
    "PSG": "巴黎聖日耳門", "Inter": "國際米蘭", "Milan": "AC米蘭", "Juventus": "祖雲達斯",
    "Tottenham": "熱刺", "Dortmund": "多蒙特", "Leverkusen": "利華古遜", "Roma": "羅馬",
    "Ajax": "阿積士", "Porto": "波圖", "Benfica": "賓菲加", "Tromso": "特林素", "Lillestrom": "利尼史特朗"
}

def translate_name(name):
    for eng, hkg in TRANSLATION_MAP.items():
        if eng in name:
            return name.replace(eng, hkg)
    return name

st.set_page_config(page_title="獵人中文版", layout="wide")
st.title("🏹 獵人狙擊系統：馬會譯名版")

# ================= 3. 核心功能 =================
if st.button("🔥 執行全網掃描 (自動翻譯至中文)"):
    full_report = "🚀 【老闆，獵人中文報表到！】\n"
    full_report += "========================\n\n"
    
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {"apiKey": API_KEY, "regions": "uk,eu", "markets": "correct_score,h2h", "oddsFormat": "decimal"}
    
    with st.spinner('📡 正在抓取數據並翻譯中...'):
        try:
            res = requests.get(url, params=params, timeout=20)
            if res.status_code == 200:
                data = res.json()
                
                # 1. 300x 波膽組合
                full_report += "💎 【300x - 500x 波膽組合】\n"
                s_count = 0
                for m in data:
                    if s_count >= 5: break
                    m_name = translate_name(f"{m['home_team']} 對 {m['away_team']}")
                    for b in m['bookmakers'][:1]:
                        for mkt in b['markets']:
                            if mkt['key'] == 'correct_score':
                                for o in mkt['outcomes']:
                                    if 8.0 <= o['price'] <= 18.0:
                                        full_report += f"📍 {m_name}\n   👉 {o['name']} | {o['price']}x\n"
                                        s_count += 1
                
                # 2. 5x1 / 7x1 組合
                full_report += "\n✅ 【高勝率 5x1 / 7x1 組合】\n"
                v_count = 0
                for m in data:
                    if v_count >= 8: break
                    m_name = translate_name(f"{m['home_team']} 對 {m['away_team']}")
                    for b in m['bookmakers'][:1]:
                        for mkt in b['markets']:
                            if mkt['key'] == 'h2h':
                                for o in mkt['outcomes']:
                                    if 2.0 <= o['price'] <= 3.5:
                                        full_report += f"🔹 {m_name} | {o['name']} | {o['price']}x\n"
                                        v_count += 1
                
                st.code(full_report)
                bot.send_message(CHAT_ID, full_report)
                st.balloons()
                st.success("🎯 中文報表已發送到 Telegram！")
            else:
                st.error(f"API 異常: {res.status_code}")
        except Exception as e:
            st.error(f"出錯：{e}")
