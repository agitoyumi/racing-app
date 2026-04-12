import streamlit as st
import pandas as pd

# 1. 系統核心配置
st.set_page_config(
    page_title="Golden Victory Pro - 雙核心系統",
    page_icon="🏆",
    layout="centered"
)

# 2. 核心視覺 CSS (黑金風格)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #E0E0E0; }
    .gold-header {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0px;
    }
    .status-box {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #332b00;
        background: #111;
        text-align: center;
        margin-bottom: 20px;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        border: 1px solid #444;
        border-radius: 12px;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 側邊欄：模式切換與進度 ---
st.sidebar.title("🎮 控制中心")
mode = st.sidebar.selectbox("切換分析領域", ["🏇 賽馬分析 (Racing)", "⚽ 足球狙擊 (Football)"])

st.sidebar.markdown("---")
st.sidebar.title("💰 辭職進度")
target = 100000
current_profit = st.sidebar.number_input("目前累計淨利 (HKD)", value=0)
progress = min((current_profit / target), 1.0)
st.sidebar.progress(progress)
st.sidebar.write(f"距離十萬目標：HKD {target - current_profit}")

# --- 主界面邏輯 ---

if mode == "🏇 賽馬分析 (Racing)":
    st.markdown('<p class="gold-header">GOLDEN VICTORY</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>v2.1 - 跑馬地 C 賽道優化版</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="status-box">🏁 下一仗：週三跑馬地夜賽 | 鎖定 1-4 檔冷門</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="內檔權重", value="待掃描", delta="+35%")
    with col2:
        st.metric(label="綠燈資金", value="待掃描", delta="監控中")
    with col3:
        st.metric(label="爆冷指數", value="待掃描", delta="EV計算")

    st.info("💡 提示：請於賽事前上傳賠率圖，系統將自動過濾『假熱門』。")

else:
    # --- 足球頁面 ---
    st.markdown('<p class="gold-header">GV FOOTBALL</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>高賠率過關 & 波膽策略模組</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="status-box">⚽ 策略：波膽 2x1 / 高賠率 3x4 過關偵測中</div>', unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.metric(label="波膽期望值", value="待分析", delta="高回報")
    with f_col2:
        st.metric(label="水位背離", value="監控中", delta="爆冷訊號")
    with f_col3:
        st.metric(label="絕殺機率", value="即時數據", delta="Live")

    st.write("### 🎯 今日高賠率建議組合")
    tab1, tab2 = st.tabs(["🚀 波膽過關", "📊 爆冷 X 過關"])
    with tab1:
        st.write("等待截圖上傳以分析特定場次...")
    with tab2:
        st.write("系統將針對『受讓』與『平手』賠率進行配搭...")

# --- 通用頁腳 ---
st.markdown("<br><hr><p style='text-align:center; color:#555;'>雙核心系統運行中。數據即權力，冷門即財富。</p>", unsafe_allow_html=True)
