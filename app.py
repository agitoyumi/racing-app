import streamlit as st
import pandas as pd

# 1. 系統核心配置
st.set_page_config(
    page_title="Golden Victory Pro - 系統優化版",
    page_icon="🏇",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. 深度優化 CSS：強化數據可讀性
st.markdown("""
    <style>
    .main { background-color: #050505; color: #E0E0E0; }
    .gold-header {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 5px;
    }
    .status-box {
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #333;
        background: #111;
        text-align: center;
        margin-bottom: 20px;
    }
    /* 強化指標卡片 */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        border: 1px solid #444;
        border-radius: 12px;
        padding: 15px;
    }
    /* 自定義按鈕 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #B8860B, #FFD700);
        color: black;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 系統頂部狀態 ---
st.markdown('<p class="gold-header">GOLDEN VICTORY PRO</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>系統版本：v2.1 (跑馬地 C 賽道優化)</p>", unsafe_allow_html=True)

# --- 側邊欄：獲利追蹤與開支扣除 ---
st.sidebar.title("💰 辭職進度管理")
target = 100000
current_profit = st.sidebar.number_input("目前累計淨利 (HKD)", value=0)
daily_expense = st.sidebar.number_input("預計每日開支扣除 (HKD)", value=500)

progress = (current_profit / target) if current_profit < target else 1.0
st.sidebar.progress(progress)
st.sidebar.write(f"距離十萬小目標還差: HKD {target - current_profit}")
st.sidebar.markdown("---")
st.sidebar.info("系統提示：週三跑馬地為『攻擊型』主場，建議鎖定位置Q。")

# --- 主界面：實戰分析 ---
tabs = st.tabs(["🎯 即時狙擊", "📈 數據模型", "📋 投注紀錄"])

with tabs[0]:
    st.markdown('<div class="status-box">🏁 下一仗：4/15 跑馬地夜賽 (C 賽道)</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="內檔放頭 (C欄優勢)", value="待掃描", delta="High EV")
    with col2:
        st.metric(label="大戶綠燈 (資金流)", value="待掃描", delta="Smart Money")
    with col3:
        st.metric(label="賠率偏差 (冷門)", value="待掃描", delta="Value Pick")

    st.write("---")
    st.write("### 🧠 系統建議組合")
    st.info("請於週三 17:00 後上傳賠率截圖，啟動系統自動分析...")

with tabs[1]:
    st.write("### 📊 跑馬地 C 賽道權重分配")
    model_data = {
        "指標": ["1-4檔位", "騎練急進度", "末段爆發力", "負磅優勢", "資金異動"],
        "當前權重": ["+35%", "+20%", "+15%", "+10%", "+20%"]
    }
    st.table(pd.DataFrame(model_data))
    st.write("💡 *註：C 賽道窄彎短直路，檔位權重已調至最高層級。*")

with tabs[2]:
    st.write("### 📓 本季獲利紀錄")
    # 這裡未來可以對接你的投注歷史
    st.caption("尚無紀錄。首場實戰測試預計：週三夜賽。")

# --- 頁腳 ---
st.markdown("<br><hr><p style='text-align:center; color:#555;'>數據模型已優化，準備迎接暑假前衝刺。</p>", unsafe_allow_html=True)
