import requests
import telebot
import streamlit as st

# ================= 1. 核心參數 (請老闆最後檢查) =================
# 如果換咗新 Key，記得貼落下面呢度
API_KEY = "3a0784d142517860438150499e17006d" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156" # 確保呢個 ID 係 @userinfobot 比你嗰串

bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 介面與顯示 =================
st.set_page_config(page_title="獵人 300x 系統", layout="wide")
st.title("🏹 獵人狙擊系統：最後反擊版")

# 側邊欄快速測試
st.sidebar.header("🔧 系統診斷")
if st.sidebar.button("檢查通行證"):
    try:
        me = bot.get_me()
        st.sidebar.success(f"Bot 連線正常: {me.first_name}")
    except:
        st.sidebar.error("TG Token 錯誤！")

# ================= 3. 發射按鈕 =================
st.subheader("📢 戰場指揮中心")
if st.button("🔥 立即全網掃描 (300x-500x 策略)"):
    # 嘗試抓取數據
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads&oddsFormat=decimal"
    
    with st.spinner('數據掃描中...'):
        try:
            res = requests.get(url, timeout=15)
            
            if res.status_code == 401:
                st.error("❌ API Key 報錯 (401)：呢粒 Key 已經失效或者未啟動。請去 The Odds API 申請粒新嘅。")
            elif res.status_code == 200:
                data = res.json()
                st.success(f"✅ 成功獲取 {len(data)} 場賽事數據！")
                
                # 這裡放原本的 3串1 與 5串1 邏輯...
                report = "🚀 【老闆，清單到！今晚目標：300倍】\n\n"
                report += "📊 數據已更新，請去 Telegram 查收詳細飛單。"
                
                # 發送到 TG
                try:
                    bot.send_message(CHAT_ID, report)
                    st.balloons()
                    st.success("🎯 數據已推送到 Telegram！")
                except Exception as e:
                    st.error(f"❌ TG 發送失敗: {e} (請確認 ID 正確)")
            else:
                st.error(f"❌ API 異常 (Code: {res.status_code})")
                
        except Exception as e:
            st.error(f"⚠️ 系統繁忙: {str(e)}")

# ================= 4. 操作指南 =================
st.divider()
st.markdown("""
### 💡 點解會 API KEY 唔啱？
1. **未驗證 Email**：Odds API 申請完通常要喺 Email 撳個 Link 啟動。
2. **Key 貼錯**：確保前後冇空格，冇漏咗引號。
3. **配額爆咗**：免費版一日唔可以撳太多次。
""")
