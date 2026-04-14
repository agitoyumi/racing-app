import streamlit as st
import pandas as pd

# 設置頁面配置
st.set_page_config(page_title="重生系統 2.0", layout="wide")

# CSS 美化：對標專業交易終端配色
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .highlight-box { padding: 20px; border-radius: 10px; background-color: #262730; border-left: 5px solid #00ffcc; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 重生系統 2.0 | 數據對標中心")

# --- 模組一：歐聯波膽監控 (對標圖 5, 6, 7) ---
st.subheader("⚽ 足球：重生波膽 3x1 監控")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="利物浦 vs PSG (對標 1:2)", value="8.00", delta="穩定")
with col2:
    st.metric(label="馬體會 vs 巴塞 (對標 2:1)", value="11.50", delta="向上", delta_color="normal")
with col3:
    st.metric(label="高車士打 vs 阿克寧頓 (對標 2:0)", value="6.90", delta="穩定")

st.markdown('<div class="highlight-box"><strong>🎯 目標效率：634.8 倍</strong><br>模擬投注：$200 ➔ 預計回報：$126,960</div>', unsafe_allow_html=True)

st.divider()

# --- 模組二：賽馬隔夜數據對標 ---
st.subheader("🏇 賽馬：聽日跑馬地三匹心水 (4/15)")

# 建立數據表
racing_data = {
    "場次": ["R1", "R1", "R1"],
    "心水級別": ["核心主推", "副選配合", "冷門伏兵"],
    "馬匹編號": ["待輸入", "待輸入", "待輸入"],
    "隔夜 WIN": ["0.0", "0.0", "0.0"],
    "隔夜 PLA": ["0.0", "0.0", "0.0"],
    "系統信號": ["等待 12:00 開盤", "等待 12:00 開盤", "等待 12:00 開盤"]
}

df = pd.DataFrame(racing_data)
st.table(df)

# --- 功能區：輸入與更新 ---
st.sidebar.header("🛠️ 數據更新入口")
st.sidebar.info("12:00 賠率出爐後，請在此輸入數據以對標變動。")
race_select = st.sidebar.selectbox("選擇場次", [f"R{i}" for i in range(1, 10)])
horse_no = st.sidebar.text_input("輸入馬匹編號")

if st.sidebar.button("同步至對標表"):
    st.sidebar.success(f"數據已載入：{race_select} - {horse_no}")
