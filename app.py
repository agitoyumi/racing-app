import requests
import telebot
import streamlit as st

# ================= 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156" 

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人狙擊 v3.1", layout="wide", page_icon="⚽")
st.title("🏹 獵人狙擊系統：精確修正版")

# ================= 1. 側邊欄：診斷工具 =================
with st.sidebar:
    st.header("🔧 系統連線檢查")
    if st.button("🔔 測試 Telegram"):
        try:
            bot.send_message(CHAT_ID, "✅ 報告老闆：TG 通道已打通！")
            st.success("TG 已響！")
        except Exception as e:
            st.error(f"TG 失敗: {e}")

# ================= 2. 核心狙擊按鈕 =================
st.subheader("📢 數據發射中心")

if st.button("🔥 立即全網掃描 (修正 422)"):
    # 修正重點：Odds API 免費版有時唔畀一次過要太多 markets
    # 我哋先攞最基本嘅 h2h 確保過到 422
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": "uk",
        "markets": "h2h",  # 暫時鎖死呢個，100% 避開 422
        "oddsFormat": "decimal"
    }
    
    with st.spinner('🎯 獵人正在全速掃描...'):
        try:
            res = requests.get(url, params=params, timeout=15)
            
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ 成功獲取 {len(data)} 場數據！")
                
                # 建立報表內容
                report = "🚀 【老闆，獵人清單到！】\n"
                report += "========================\n\n"
                for match in data[:5]:
                    report += f"⚽ {match['home_team']} vs {match['away_team']}\n"
                
                st.code(report) # 網頁預覽
                
                # 推送 TG
                try:
                    bot.send_message(CHAT_ID, report)
                    st.balloons()
                    st.success("🎯 數據已同步發送到 Telegram！")
                except Exception as e:
                    st.error(f"❌ TG 發送失敗：{e}")
                    
            else:
                st.error(f"❌ API 報錯 Code: {res.status_code}")
                st.json(res.json()) # 呢行會顯示點解 422
                
        except Exception as e:
            st.error(f"⚠️ 網絡異常: {str(e)}")

st.divider()
st.info("💡 如果仲係 422，請睇吓網頁顯示嘅 JSON 錯誤訊息，嗰度會寫明邊個參數唔啱。")
