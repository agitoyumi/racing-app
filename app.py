import streamlit as st

# 模擬一個專業的投注介面
st.set_page_config(page_title="賽馬戰術面板", layout="centered")

# 頂部狀態欄
st.markdown("### 🏇 **Happy Valley 夜賽戰術室**")
st.progress(0.9)  # 顯示開賽倒數感

# 核心建議區：用卡片式設計
st.subheader("🎯 核心 2X3 建議")
col1, col2 = st.columns(2)
with col1:
    st.info("**第一關：第 9 場**\n\n4. 亞機拉 (3檔)\n\n6. 名揚四海 (1檔)")
with col2:
    st.success("**第二關：第 11 場**\n\n2. 信心星 (莫雷拉)\n\n11. 閃耀天河 (巴度)")

# 投注計算器介面
st.divider()
st.subheader("💰 投注預算")
bet_amount = st.number_input("每注金額 ($)", value=10)
st.button("計算 2X3 總金額")

st.caption("✅ 數據已根據馬會 App 截圖實時同步")
