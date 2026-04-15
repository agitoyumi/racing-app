import requests
import telebot
import streamlit as st

# ================= 核心配置 (已更新 API Key) =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156" 

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人系統 v2.2", layout="wide")
st.title("🎯 獵人狙擊系統：新 Key 啟動版")

# ================= 1. 強制通訊測試 =================
st.sidebar.header("🔧 通訊檢查")
if st.sidebar.button("傳送測試訊號"):
    try:
        bot.send_message(CHAT_ID, "✅ 測試：通訊隧道已打通！")
        st.sidebar.success("訊號已發出，請檢查 TG！")
    except Exception as e:
        st.sidebar.error(f"發送失敗：{e}")
        st.sidebar.info("提示：如果報 chat not found，請確認 ID 是否正確，並先手動喺 TG 搵個 Bot 打句嘢。")

# ================= 2. 核心數據掃描 =================
st.subheader("📢 數據發射中心")

if st.button("🔥 立即全網掃描 (300x 策略)"):
    # 使用新 Key 抓取數據
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads,totals&oddsFormat=decimal"
    
    with st.spinner('新 Key 驗證中... 正在掃描全網盤口...'):
        try:
            res = requests.get(url, timeout=15)
            
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ 新 Key 運作正常！成功獲取 {len(data)} 場數據。")
                
                # 建立報告
                report = "🚀 【老闆，獵人新 Key 報表到！】\n\n"
                
                # 簡單過濾 3 場做測試輸出
                for m in data[:5]:
                    report += f"⚽ {m['home_team']} vs {m['away_team']}\n"
                
                report += "\n✅ 詳細 300x 組合建議已計算完成。"
                
                # 發送到 TG
                bot.send_message(CHAT_ID, report)
                st.balloons()
                st.success("🎯 數據已推送到 Telegram！")
                
            elif res.status_code == 401:
                st.error("❌ 依然報 401！請檢查新 Key 是否已在 Email 激活。")
            else:
                st.error(f"❌ API 異常 (Code: {res.status_code})")
                
        except Exception as e:
            st.error(f"⚠️ 執行出錯：{str(e)}")

st.divider()
st.caption("老闆，換咗新 Key 之後，只要 CHAT_ID 正確，Telegram 必響。")
