import requests
import telebot
import streamlit as st
import time

# ================= 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人 500x 系統", layout="wide")
st.title("🏹 獵人狙擊系統 v6.0：分段收割版")

# ================= 數據獲取工具 =================
def get_data(market_type):
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": "uk,eu",
        "markets": market_type,
        "oddsFormat": "decimal"
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None

# ================= 核心按鈕 =================
if st.button("🔥 啟動深度掃描 (避開 422 專用)"):
    report = "🚀 【自由之翼：深夜獵報 全功能版】\n"
    report += "========================\n\n"
    
    with st.spinner('🎯 第一階段：正在捕捉 300x 波膽數據...'):
        score_data = get_data("correct_score")
        score_picks = []
        if score_data:
            for match in score_data:
                for bookie in match['bookmakers']:
                    if bookie['key'] in ['pinnacle', 'williamhill', 'betfair_ex']:
                        for mkt in bookie['markets']:
                            for opt in mkt['outcomes']:
                                if 7.0 <= opt['price'] <= 16.0:
                                    score_picks.append(f"{match['home_team']} | {opt['name']} | {opt['price']}x")
        
        report += "🎯 【終極 3 串 1 波膽 (300x+)】\n"
        if len(score_picks) >= 3:
            for s in score_picks[:3]: report += f"📍 {s}\n"
            report += "💰 預估回報：350x - 600x\n\n"
        else:
            report += "📉 暫無合適波膽數據\n\n"

    time.sleep(1) # 停一停，費事 API 鎖我哋

    with st.spinner('🔥 第二階段：正在計算 5-7 串 1 組合...'):
        h2h_data = get_data("h2h")
        value_picks = []
        unusual = []
        if h2h_data:
            for match in h2h_data:
                for bookie in match['bookmakers']:
                    for mkt in bookie['markets']:
                        for opt in mkt['outcomes']:
                            if 2.0 <= opt['price'] <= 3.5:
                                value_picks.append(f"{match['home_team']} vs {match['away_team']} | {opt['name']} | {opt['price']}x")
                            if opt['price'] < 1.35: # 監控熱錢
                                unusual.append(f"⚠️ 異常熱錢: {match['home_team']} ({opt['price']}x)")

        report += "🔥 【高勝率 5-7 串 1 (2.0x+)】\n"
        if len(value_picks) >= 5:
            for v in value_picks[:7]: report += f"✅ {v}\n"
        else:
            report += "📉 優質讓球盤口不足\n"

    report += "\n🚨 【資金流/數據異常監控】\n"
    if unusual:
        for u in unusual[:3]: report += f"{u}\n"
    else:
        report += "⚖️ 全網資金流向目前穩定\n"

    # 顯示結果
    st.markdown("### 🔍 掃描結果")
    st.code(report)
    
    # 推送 TG
    try:
        bot.send_message(CHAT_ID, report)
        st.balloons()
        st.success("🎯 數據已同步推送到 Telegram！")
    except Exception as e:
        st.error(f"TG 失敗: {e}")

st.sidebar.button("🔔 測試通訊", on_click=lambda: bot.send_message(CHAT_ID, "✅ 連線正常！"))
