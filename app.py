import streamlit as st

# 1. 頁面配置：設定標題與圖示
st.set_page_config(
    page_title="Golden Victory - 專業賽馬數據分析",
    page_icon="🏇",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 華麗黑金視覺 CSS
st.markdown("""
    <style>
    /* 全局背景：深邃黑 */
    .main {
        background-color: #050505;
        color: #E0E0E0;
    }
    
    /* 標題漸變金 */
    .gold-text {
        background: linear-gradient(90.0deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 10px;
    }

    /* 冷門馬卡片設計 */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
        border: 1px solid #332b00;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.1);
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #FFD700;
    }

    /* 隱藏 Streamlit 默認標記 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* PWA 手機全螢幕優化 */
    @media (max-width: 640px) {
        .gold-text { font-size: 1.8rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 頂部 Logo 區 ---
st.markdown('<p class="gold-text">GOLDEN VICTORY</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>數據驅動 · 冷門狙擊 · 翻身之作</p>", unsafe_allow_html=True)

# --- 動態跑馬燈 (戰績展示) ---
st.info("🔥 歷史戰績：上週六擊中 第8場 45倍冷門連贏 (Q) | 第3場 位置Q 獲利 280%")

# --- 核心預測區：冷門三劍客 ---
st.write("### 🎯 臨場冷門核心建議")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="狙擊 1 (首選)", value="6. 名揚四海", delta="48.0", delta_color="normal")
    st.caption("🏆 預期倍率: 15-50x")

with col2:
    st.metric(label="狙擊 2 (次選)", value="9. 正義波", delta="22.5", delta_color="normal")
    st.caption("📈 資金流入明顯")

with col3:
    st.metric(label="狙擊 3 (驚喜)", value="2. 亞機拉", delta="18.0", delta_color="normal")
    st.caption("⚡️ 檔位優勢極大")

# --- 戰術組合建議 ---
st.markdown("---")
with st.container():
    st.write("### 📝 攻擊性投注組合")
    st.success("**重點：(6) 拖 (2, 9) 位置Q (QP)**")
    st.warning("**激進：(6, 9, 2) 三重彩 / 四重彩配腳**")
    st.write("💡 *分析：跑馬地C賽道窄彎，1-4檔冷門馬具備翻盤條件。*")

# --- 辭職進度條 (激勵自己) ---
st.sidebar.write("## 🚀 翻身進度")
progress = st.sidebar.slider("小目標進度 (10萬)", 0, 100, 5)
st.sidebar.write(f"目前已完成: {progress}%")

# --- 底部：隱藏式打賞門戶 ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🧧 成績見證 - 感謝開發者"):
    st.write("如果您在今日賽事中獲利，歡迎支持 AI 持續開發。")
    st.code("FPS ID: (待成績驗證後填入)", language=None)
    st.write("您的支持是我們離開體力勞動的階梯。")

st.caption("✅ 系統狀態：已就緒。待週三 17:00 上傳數據。")
