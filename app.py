import streamlit as st

# 1. 頁面配置
st.set_page_config(
    page_title="Golden Victory - 專業賽馬數據分析",
    page_icon="🏇",
    layout="centered"
)

# 2. 核心視覺 CSS (包含 Icon 樣式)
st.markdown("""
    <style>
    .main { background-color: #050505; color: #E0E0E0; }
    
    /* 置頂 Icon 容器 */
    .logo-container {
        display: flex;
        justify-content: center;
        padding-top: 20px;
        margin-bottom: -10px;
    }
    
    .logo-img {
        width: 120px;
        height: 120px;
        border-radius: 25px; /* 像 App Icon 的圓角 */
        border: 2px solid #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        object-fit: cover;
    }

    /* 漸變金標題 */
    .gold-text {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        margin-top: 15px;
        letter-spacing: 2px;
    }

    /* 隱藏多餘 UI */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 指標卡片自定義 */
    div[data-testid="stMetric"] {
        background: #111;
        border: 1px solid #332b00;
        border-radius: 15px;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 置頂 Icon 顯示區 ---
# 注意：你需要將之前生成的 Icon 圖片上傳到 GitHub 同一目錄下，命名為 'logo.png'
# 如果還沒上傳，這裡會先預留空間
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("logo.png", width=120) # 這裡會抓取你 GitHub 裡的 logo.png
except:
    # 如果找不到圖片，先顯示一個金色的佔位符
    st.markdown('<div style="width:120px; height:120px; background:#1a1a1a; border:2px solid #FFD700; border-radius:25px; display:flex; align-items:center; justify-content:center; color:#FFD700;">LOGO</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="gold-text">GOLDEN VICTORY</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; font-size: 0.9rem;'>數據驅動 · 專業狙擊 · 翻身之作</p>", unsafe_allow_html=True)

st.divider()

# --- 核心預測內容 (週三更新) ---
st.write("### 🎯 臨場冷門核心建議")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="狙擊 1 (首選)", value="待更新", delta="--")
with col2:
    st.metric(label="狙擊 2 (次選)", value="待更新", delta="--")
with col3:
    st.metric(label="狙擊 3 (驚喜)", value="待更新", delta="--")

# --- 側邊欄：目標進度 ---
st.sidebar.markdown("## 🚀 辭職倒數")
st.sidebar.progress(5)
st.sidebar.write("目標：HKD 100,000")
st.sidebar.write("目前進度：5%")
