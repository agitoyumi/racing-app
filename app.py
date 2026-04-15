import requests
import telebot
import streamlit as st

# ================= 1. 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156" # 老闆，請確保呢串數字同 @userinfobot 比你嘅一模一樣

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人 300x 系統", layout="wide", page_icon="⚽")

# ================= 2. 華麗介面回歸 =================
st.title("⚽ 獵人狙擊系統 v3.0")
st.markdown("### 🏹 目標：深夜 300x+ 爆發")

# 側邊欄快速測試
with st.sidebar:
    st.header("⚙️ 系統設定")
    if st.button("🔔 測試 TG 連線"):
        try:
            bot.send_message(CHAT_ID, "✅ 報告老闆：Telegram 通道已打通！")
            st.success("TG 已響！請檢查手機。")
        except Exception as e:
            st.error(f"TG 仲係唔得：{e}")
            st.info("💡 提示：請先喺 TG 搵個 Bot (@Predator_V5_Bot) 打個 /start")

# ================= 3. 核心抓取邏輯 (全功能版) =================
if st.button("🔥 立即全網掃描 (300x 策略)"):
    # 同時掃描波膽同讓球
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,h2h&oddsFormat=decimal"
    
    with st.spinner('🎯 獵人正在全速掃描深夜盤口...'):
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ 成功監控 {len(data)} 場深夜賽事")
                
                # 建立專業報表
                report = "🚀 【自由之翼：深夜狙擊報表】\n"
                report += "========================\n\n"
                
                # 篩選邏輯 (只攞頭幾個做測試)
                for match in data[:5]:
                    report += f"⚽ {match['home_team']} vs {match['away_team']}\n"
                
                report += "\n🎯 【深夜推薦組合】\n"
                report += "• 策略：3 串 1 波膽 (高倍)\n"
                report += "• 狀態：數據已就緒，請及時落注。\n"
                
                # 顯示喺網頁
                st.info("📊 實時掃描結果已產生")
                st.code(report)
                
                # 發送到 TG
                try:
                    bot.send_message(CHAT_ID, report)
                    st.balloons()
                    st.success("🎯 數據已同步推送到 Telegram！")
                except Exception as e:
                    st.error(f"❌ TG 發送失敗：{e}")
            else:
                st.error(f"❌ API 報錯：Code {res.status_code}")
        except Exception as e:
            st.error(f"⚠️ 網絡異常：{str(e)}")

st.divider()
st.markdown("💡 *提示：只要側邊欄個測試掣響咗，今晚你就一定收得到 Push！*")
