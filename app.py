import streamlit as st
import pandas as pd
from datetime import datetime

# 設定頁面
st.set_page_config(page_title="老闆翻身中樞", layout="centered")

st.title("🏹 4/17 真實命根飛監測")
st.warning("嚴禁虛構！依家對準晒你張 $100 蚊 4 串 1 實飛數據。")

# 1. 真實注項數據 (根據 07:52 截圖)
# 唔再有阿德萊德，唔再有神戶！
real_data = [
    {"編號": "FB7560", "對賽": "彭美拉斯 vs 士砵亭水晶", "注項": "半全場 [和-主]", "賠率": 3.50, "狀態": "✅ 已過關"},
    {"編號": "FB7557", "對賽": "聖羅倫素 vs 昆卡", "注項": "主客和 [和]", "賠率": 3.70, "狀態": "等待開賽 (08:30)"},
    {"編號": "FB7517", "對賽": "墨爾本勝利 vs 紐卡素噴射機", "注項": "主客和 [和]", "賠率": 3.75, "狀態": "等待開賽 (17:35)"},
    {"編號": "FB7147", "對賽": "吉達艾阿里 vs 柔佛DT", "注項": "主客和 [和]", "賠率": 4.55, "狀態": "等待開賽 (02:00)"}
]

df = pd.DataFrame(real_data)

# 2. 顯示真實表格
st.table(df)

# 3. 真正派彩計算器
st.divider()
total_odds = 3.50 * 3.70 * 3.75 * 4.55
bet_amount = 100

st.metric(label="這條 4 串 1 總賠率", value=f"{total_odds:.2f} 倍")

col1, col2 = st.columns(2)
with col1:
    st.info(f"投入本金：${bet_amount}")
with col2:
    st.success(f"全中預計收：${bet_amount * total_odds:,.2f}")

# 4. 老闆提醒
st.error("🚨 提醒：墨爾本勝利 (17:35) 係關鍵對沖位，另一張波膽飛要盯緊！")
st.caption(f"系統最後校準：{datetime.now().strftime('%H:%M:%S')}")
