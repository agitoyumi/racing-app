import requests
import telebot
import streamlit as st
import sys

# ================= 1. 配置 (請老闆確保呢度無空格) =================
API_KEY = "3a0784d142517860438150499e17006d"
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156"

st.set_page_config(page_title="獵人系統除錯中")
st.title("🏹 獵人系統：正面突破版")

# ================= 2. 強制診斷區 =================
st.header("🔍 系統連線診斷")

col1, col2 = st.columns(2)

with col1:
    if st.button("第一步：測試 TG 通訊"):
        try:
            test_bot = telebot.TeleBot(TG_TOKEN)
            me = test_bot.get_me()
            st.success(f"✅ TG Token 正常！\nBot 名稱: {me.first_name}")
            # 嘗試發一條測試訊息
            test_bot.send_message(CHAT_ID, "🚀 測試訊息：如果你睇到呢句，代表 CHAT_ID 正確！")
            st.success("✅ 測試訊息已發出，請檢查 TG！")
        except Exception as e:
            st.error(f"❌ TG 連線失敗: {str(e)}")
            st.info("💡 如果報 'chat not found'，請先喺 TG 隨便打句嘢畀個 Bot。")

with col2:
    if st.button("第二步：測試 API 密鑰"):
        url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk&markets=h2h"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                st.success(f"✅ API Key 正常！掃到 {len(res.json())} 場波。")
            else:
                st.error(f"❌ API 報錯：Code {res.status_code}")
                st.write(res.text) # 顯示具體報錯內容
        except Exception as e:
            st.error(f"❌ API 連線超時: {str(e)}")

# ================= 3. 核心功能 =================
st.divider()
st.header("🎯 狙擊指令發射")

def run_hunt():
    # 呢度係你最想要嘅掃描邏輯
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads&oddsFormat=decimal"
    try:
        data = requests.get(url).json()
        score_picks = [f"{m['home_team']} vs {m['away_team']}" for m in data[:3]] # 範例邏輯
        report = "📊 【獵人實時報表】\n" + "\n".join(score_picks)
        
        # 暴力發送
        final_bot = telebot.TeleBot(TG_TOKEN)
        final_bot.send_message(CHAT_ID, report)
        return "✅ 報表已推送到 Telegram！"
    except Exception as e:
        return f"❌ 執行失敗: {str(e)}"

if st.button("🔥 執行全網掃描並 Push 到 TG"):
    result = run_hunt()
    st.write(result)

st.divider()
st.caption("老闆，如果第一步過到而第二步過唔到，就係 Key 嘅問題；如果兩步都過到但撳大掣無反應，就係 Streamlit 暫時屏蔽咗自動推送。")
