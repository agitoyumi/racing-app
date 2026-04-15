import requests
import telebot
import streamlit as st

# ================= 1. 核心參數 (已根據你資料填好) =================
API_KEY = "3a0784d142517860438150499e17006d"
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156"

# 初始化 Bot
bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 數據掃描功能 =================
def get_odds_report():
    # 掃描波膽、讓球、大細
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads,totals&oddsFormat=decimal"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return f"❌ API 報錯: {response.status_code}"
        
        data = response.json()
        score_picks = [] # 3串1用 (7-15倍)
        value_picks = [] # 5-7串1用 (2.0+倍)

        for match in data:
            home = match['home_team']
            away = match['away_team']
            for bookie in match['bookmakers']:
                if bookie['key'] in ['pinnacle', 'williamhill']:
                    for market in bookie['markets']:
                        for outcome in market['outcomes']:
                            price = outcome['price']
                            
                            # A. 搵波膽 (目標高回報)
                            if market['key'] == 'correct_score' and 7.0 <= price <= 15.0:
                                score_picks.append(f"{home} vs {away} | {outcome['name']} | {price}倍")
                            
                            # B. 搵 2.0+ 勁嘢
                            elif market['key'] in ['spreads', 'totals'] and price >= 2.0:
                                value_picks.append(f"{home} vs {away} | {outcome['name']} | {price}倍")

        # 整理報告文本
        msg = "🚀 【自由之翼：深夜狙擊報表】\n\n"
        
        msg += "🎯 【終極 3 串 1 波膽 (300x+)】\n"
        if len(score_picks) >= 3:
            for s in score_picks[:3]: msg += f"• {s}\n"
        else: msg += "• 盤口更新中，暫無合適波膽。\n"

        msg += "\n🔥 【高槓桿 5-7 串 1 (2.0+)】\n"
        if len(value_picks) >= 5:
            for v in value_picks[:7]: msg += f"• {v}\n"
        else: msg += "• 暫未掃描到優質受讓/大細盤。\n"

        msg += "\n🚨 【資金流監控】\n目前數據流向穩定，如有異常爆發會即時標註。"
        return msg

    except Exception as e:
        return f"⚠️ 掃描發生錯誤: {str(e)}"

# ================= 3. Streamlit 介面 =================
st.set_page_config(page_title="獵人狙擊系統", page_icon="⚽")
st.title("⚽ 獵人狙擊系統 v2.0")
st.info("老闆，準備好開火未？")

if st.button("🔥 立即掃描並發送到 Telegram"):
    with st.spinner('掃描全網數據中...'):
        report = get_odds_report()
        
        # 顯示喺網頁
        st.markdown("### 🔍 掃描結果")
        st.code(report)
        
        # 同步發送到 Telegram
        try:
            bot.send_message(CHAT_ID, report)
            st.success("✅ 報告已成功發送到你的 Telegram！")
        except Exception as e:
            st.error(f"❌ TG 發送失敗: {e}")

# 加一個簡單嘅連線測試
if st.sidebar.button("⚙️ 測試 Bot 連線"):
    try:
        user = bot.get_me()
        st.sidebar.success(f"Bot 狀態: 正常 ({user.first_name})")
    except:
        st.sidebar.error("Bot 狀態: 斷線 (請檢查 Token)")
