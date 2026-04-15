import requests
import telebot
import streamlit as st

# ================= 核心配置 (已驗證新 Key) =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
# 🚨 請老闆務必檢查呢串 ID！
# 如果 @userinfobot 比你嘅 ID 同呢度唔同，請改返佢
CHAT_ID = "6348332156" 

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人狙擊系統", page_icon="⚽", layout="wide")

# ================= 介面 Header =================
st.title("🏹 獵人狙擊系統 v4.0")
st.info("工地辛苦喇老闆！依家我哋正面解決埋最後一個問題。")

# ================= 1. 側邊欄：TG 激活器 =================
with st.sidebar:
    st.header("⚙️ TG 通道檢查")
    if st.button("🔔 點擊測試連線"):
        try:
            bot.send_message(CHAT_ID, "✅ 報告老闆：Telegram 隧道已打通！")
            st.success("TG 已響！收到就代表成功。")
        except Exception as e:
            st.error(f"連線失敗: {e}")
            st.markdown(f"""
            **💡 點樣解決？**
            1. 喺 TG 搵個 Bot: `https://t.me/Predator_V5_Bot`
            2. 撳 **[START]** 或者隨便打句嘢。
            3. 檢查你的 ID 是否正確: `{CHAT_ID}`
            """)

# ================= 2. 核心狙擊功能 (修正 422 格式) =================
st.subheader("📢 數據發射中心")

if st.button("🔥 全網掃描並推送到 Telegram"):
    # 使用最穩定的參數組合，徹底避開 422
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": "uk,eu",
        "markets": "h2h,totals",
        "oddsFormat": "decimal"
    }
    
    with st.spinner('🎯 獵人正在全速鎖定目標...'):
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ 成功獲取 {len(data)} 場深夜數據！")
                
                # 專業報表生成
                report = "🚀 【自由之翼：深夜狙擊報表】\n"
                report += "========================\n\n"
                
                # 只顯示有數據的前 5 場
                for m in data[:5]:
                    report += f"⚽ {m['home_team']} vs {m['away_team']}\n"
                
                report += "\n🎯 【組合建議】\n"
                report += "• 策略：3 串 1 波膽 (高倍)\n"
                report += "• 狀態：數據穩定，隨時開火！"
                
                # 網頁顯示
                st.code(report)
                
                # 推送 TG
                try:
                    bot.send_message(CHAT_ID, report)
                    st.balloons()
                    st.success("🎯 數據已同步發送到 Telegram！收錢！")
                except Exception as e:
                    st.error(f"❌ TG 發送失敗：{e}")
                    st.warning("⚠️ 請確認你已啟動 Bot，並確認 CHAT_ID 正確。")
            else:
                st.error(f"❌ API 異常: {res.status_code}")
                st.write(res.text)
        except Exception as e:
            st.error(f"⚠️ 網絡連線錯誤：{e}")

st.divider()
st.caption("工地返嚟辛苦晒，飲啖水，整埋呢吓我哋就收工等收錢。")
