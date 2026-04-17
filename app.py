import streamlit as st
import pandas as pd
from datetime import datetime

# 設定網頁標題
st.set_page_config(page_title="老闆反擊戰 - 數據中樞", layout="centered")

st.title("🚀 今日 4/17 數據反擊線")
st.subheader("寫咗成個禮拜，今晚一定要攞成績！")

# 1. 核心場次數據 (根據你 07:56 的截圖)
matches = [
    {"時間": "17:45", "編號": "FB7147", "對賽": "阿德萊德聯 vs 麥克阿瑟", "玩法": "主客和 [和]", "賠率": 3.65},
    {"時間": "18:00", "編號": "FB7273", "對賽": "神戶勝利船 vs 名古屋鯨魚", "玩法": "主客和 [和]", "賠率": 3.40},
    {"時間": "02:30", "編號": "FB8350", "對賽": "法蘭克福 vs 奧格斯堡", "玩法": "讓球主客和 [讓主]", "賠率": 2.05}
]

df = pd.DataFrame(matches)

# 2. 顯示表格
st.table(df)

# 3. 自動利潤計算器
st.divider()
st.sidebar.header("💰 利潤計算器")
bet_amount = st.sidebar.number_input("輸入注碼 ($)", min_value=10, value=100, step=10)

# 計算總賠率
total_odds = 1
for m in matches:
    total_odds *= m["賠率"]

estimated_payout = bet_amount * total_odds

st.metric(label="總賠率 (3 串 1)", value=f"{total_odds:.2f} 倍")
st.success(f"🎯 若全中，預計派彩：${estimated_payout:,.2f}")

# 4. 狀態更新
st.caption(f"最後更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.info("老闆，場次已鎖定：阿德、神戶、法蘭。今晚守住 17:45 開波！")
