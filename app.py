import streamlit as st
import pandas as pd

# 設置深色頁面與自定義 CSS
st.set_page_config(page_title="賽馬冷門狙擊手 v3.0", layout="centered")

# 強制深色模式風格
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stMetric { background-color: #1F2937; padding: 15px; border-radius: 10px; border: 1px solid #FFD700; }
    .stAlert { background-color: #111827; border: 1px solid #00FFA3; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 跑馬地夜賽：冷門狙擊工具")

# --- 每場建議 3 匹冷門區 (最置頂) ---
st.subheader("🎯 本場 3 匹「冷門機會馬」")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="冷門 1 (首選)", value="6. 名揚四海", delta="55.0倍")
    st.caption("1 檔 | 123 磅 | 內欄優勢")

with col2:
    st.metric(label="冷門 2 (次選)", value="9. 正義波", delta="21.0倍")
    st.caption("2 檔 | 121 磅 | 輕磅利好")

with col3:
    st.metric(label="冷門 3 (搏爆)", value="4. 亞機拉", delta="19.0倍")
    st.caption("3 檔 | 125 磅 | 前速跟前")

st.divider()

# --- 投注組合區 ---
with st.expander("📝 投注組合建議 (2X3 / 連贏)"):
    st.success("建議組合：(4, 6, 9) 互串位置Q")
    st.write("總注數：3 注")
    st.info("💡 邏輯：跑馬地 C 賽道極利 1-4 檔，此 3 匹馬皆符合好檔+冷門條件。")

# --- 底部數據核對區 ---
st.caption("✅ 數據已與馬會 App 15:50 截圖同步校對")
