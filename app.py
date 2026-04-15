import requests
import telebot
import streamlit as st

# ================= 1. 核心配置 (已鎖定老闆真 ID) =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" # 老闆 L 的正確 ID

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人狙擊系統", page_icon="⚽", layout="wide")
st.title("🏹 獵人狙擊系統：終極收割版")

# ================= 2. 強制診斷 (請務必撳呢個) =================
with st.sidebar:
    st.header("⚙️ 戰場通訊檢查")
    if st.button("🔔 點擊測試連線"):
        try:
            # 暴力測試：直接發一條訊息
            bot.send_message(CHAT_ID, "✅ 報告老闆：Telegram 隧道正式打通！今晚開火！")
            st.success("TG 已響！收到代表 100% 成功。")
        except Exception as e:
            st.error(f"連線失敗原因: {e}")
            st.info("💡 如果仲係失敗，請檢查你手機係咪 search 緊正確嘅 Bot 並撳咗 Start。")

# ================= 3. 核心數據發射 =================
st.subheader("📢 數據發射中心")

if st.button("🔥 立即全網掃描 (300x 策略)"):
    # 呢個 URL 組合已經喺 18:50 證實係 200 OK 攞到數據嘅
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": "uk,eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }
    
    with st.spinner('🎯 獵人正在全速鎖定目標...'):
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ 成功獲取 {len(data)} 場深夜數據！")
                
                # 專業報表
                report = "🚀 【自由之翼：深夜狙擊報表】\n"
                report += "========================\n\n"
                for m in data[:5]:
                    report += f"⚽ {m['home_team']} vs {m['away_team']}\n"
                report += "\n🎯 【組合建議】\n• 策略：3 串 1 波膽\n• 狀態：數據就緒，隨時開火！"
                
                # 網頁先出一次
                st.code(report)
                
                # 推送 TG
                try:
                    bot.send_message(CHAT_ID, report)
                    st.balloons()
                    st.success("🎯 數據已同步發送到 Telegram！收錢！")
                except Exception as tg_err:
                    st.error(f"❌ TG 推送失敗：{tg_err}")
            else:
                st.error(f"❌ API 異常: {res.status_code}")
        except Exception as e:
            st.error(f"⚠️ 執行出錯：{e}")

st.divider()
st.caption("老闆，一波三折終於完喇。辛苦晒，搞掂埋呢吓去休息，11 點見！")
