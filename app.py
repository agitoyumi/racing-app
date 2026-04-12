import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 系統核心配置 ---
st.set_page_config(
    page_title="Golden Victory - 財富自由系統",
    page_icon="🏆",
    layout="wide"
)

# --- 2. 私人黑金風格 CSS ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #E0E0E0; }
    .gold-header {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 0px;
    }
    .stMetric {
        background: rgba(255, 215, 0, 0.05);
        border: 1px solid #332b00;
        border-radius: 10px;
        padding: 15px;
    }
    .status-card {
        background: #111;
        border-left: 5px solid #FFD700;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 側邊欄：進度管理與模式切換 ---
st.sidebar.markdown('<p style="font-size: 20px; font-weight: bold; color: #FFD700;">🏆 辭職倒數計時</p>', unsafe_allow_html=True)

# 財富目標設定
target_goal = 100000
current_profit = st.sidebar.number_input("目前累計淨利 (HKD)", value=0, step=100)
progress = min(current_profit / target_goal, 1.0)
st.sidebar.progress(progress)
st.sidebar.write(f"📊 目標達成率: {progress*100:.1f}%")
st.sidebar.write(f"🚩 距離十萬目標還差: **${target_goal - current_profit}**")

st.sidebar.markdown("---")
mode = st.sidebar.radio("切換狙擊頻道", ["⚽ 足球暴力過關", "🏇 賽馬冷門狙擊"])

# --- 4. 主介面邏輯 ---

if mode == "⚽ 足球暴力過關":
    st.markdown('<p class="gold-header">GV FOOTBALL SNIPER</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>專攻波膽過關 | 最小本金 · 最大回報</p>", unsafe_allow_html=True)

    # 今日實戰狀態
    st.markdown("""
    <div class="status-card">
        <h3 style="color:#FFD700; margin-top:0;">🎯 今日實戰：方案 A (12/4)</h3>
        <p><b>組合：</b> 幸運薛達 [1:1] x 熱拿亞 [1:0]</p>
        <p><b>預計派彩：</b> $7,936 (39.68 倍)</p>
        <p style="color:#00FF00;">⏳ 預計 21:00 揭曉結果</p>
    </div>
    """, unsafe_allow_html=True)

    # 數據指標區
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric("當前策略", "波膽 2x1", "暴力模式")
    with col_f2:
        st.metric("系統 EV 值", "1.85", "+0.45")
    with col_f3:
        st.metric("今日建議注碼", "HKD $200", "方案 A")

    st.write("---")

    # 暴力 3x1 監控區
    st.subheader("🚀 深夜暴力 3x1 預選 (目標 200倍+)")
    
    t1, t2, t3 = st.tabs(["🔒 悶戰連線 (和局)", "💣 強隊翻車 (爆冷)", "🎭 半全場偷雞"])
    with t1:
        st.write("建議組合：1:1 x 1:1 x 0:0")
        st.info("適合聯賽：意甲、西甲、法甲")
    with t2:
        st.write("建議組合：1:2 x 0:2 x 2:1")
        st.warning("適合聯賽：英超、德甲強隊作客")
    with t3:
        st.write("建議組合：和/主 x 和/客 x 客/主")
        st.error("極致賠率，建議使用方案 A 贏得的利潤進行。")

else:
    # --- 賽馬介面 ---
    st.markdown('<p class="gold-header">GV RACING ELITE</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>週三跑馬地 | C 賽道冷門偵測</p>", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("""
        <div class="status-card">
            <h4>🐎 冷門馬篩選器</h4>
            <ul>
                <li>鎖定 1-4 檔</li>
                <li>賠率 15倍 - 40倍</li>
                <li>監控：最後一分鐘綠燈資金</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_r2:
        st.markdown("""
        <div class="status-card">
            <h4>💰 賽馬策略</h4>
            <p>利用賽馬穩定贏取足球本金</p>
            <p><b>目標：</b> 每週穩定獲利 $3,000+</p>
        </div>
        """, unsafe_allow_html=True)

# --- 5. 系統足跡紀錄 (事業化基石) ---
st.write("---")
st.subheader("📝 實戰日誌 (以小博大數據庫)")
with st.expander("查看過往戰績錄"):
    data = {
        "日期": ["2024-04-12", "過往歷史"],
        "項目": ["足球 2x1", "傳奇記錄"],
        "本金": ["$200", "$2,000"],
        "結果": ["等待中", "+$70,000"],
        "備註": ["方案 A", "一個月達成"]
    }
    st.table(pd.DataFrame(data))

st.markdown("<p style='text-align:center; color:#444;'>過程唔重要，我只要結果。Golden Victory 系統持續運行中。</p>", unsafe_allow_html=True)
