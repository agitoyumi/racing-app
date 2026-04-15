import requests
import telebot
import streamlit as st

# ================= 1. 核心配置 (已更新為你的正確 ID) =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" # 已更正：呢個先係老闆你嘅真 ID

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人狙擊系統", page_icon="⚽", layout="wide")

# ================= 2. 介面設計 =================
st.title("🏹 獵人狙擊系統：大結局版")
st.success(f"✅ 目標 ID 已鎖定：{CHAT_ID}")

with st.sidebar:
    st.header("⚙️ 最後通訊檢查")
    if st.button("🔔 點擊測試連線"):
        try:
            bot.send_message(CHAT_ID, "✅ 恭喜老闆！Telegram 隧道正式打通！今晚開火！")
            st.success("TG 已響！收到代表 100% 成功。")
        except Exception as e:
            st.error(f"仲係唔得？錯誤原因: {e}")

# ================= 3. 核心數據功能 =================
st.subheader("📢 數據發射中心")

if st.button("🔥 全網掃描並推送到 Telegram"):
    # 使用最穩定的 API 請求
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": "uk,eu",
        "markets": "h2h,totals",
        "oddsFormat": "decimal"
    }
    
    with st.spinner('🎯 獵人正在全速掃描深夜盤口...'):
        try:
            res = requests.get(url, params=params, timeout=15)
            if res.status_code == 200:
                data = res.json()
                st.success(f"✅ 成功獲取 {len(data)} 場數據！")
                
                # 建立專業報表
                report = "🚀 【自由之翼：深夜獵報】\n"
                report += "========================\n\n"
                for m in data[:5]:
                    report += f"⚽ {m['home_team']} vs {m['away_team']}\n"
                report += "\n🎯 今晚目標：3 串 1 波膽收割！"
                
                # 推送 TG
                try:
                    bot.send_message(CHAT_ID, report)
                    st.balloons()
                    st.success("🎯 數據已同步推送到 Telegram！去收錢喇！")
                except Exception as e:
                    st.error(f"❌ TG 依然失敗：{e}")
            else:
                st.error(f"❌ API 異常 Code: {res.status_code}")
        except Exception as e:
            st.error(f"⚠️ 網絡連線錯誤：{e}")

st.divider()
st.caption("老闆，一波三折終於完喇。辛苦晒，搞掂埋呢吓去休息，11 點見！")
