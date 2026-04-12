import streamlit as st
import pandas as pd

# 1. 頁面配置
st.set_page_config(page_title="賽馬冷門狙擊手 v3.1", layout="centered")

# 2. 強制深色模式與自定義樣式 (CSS)
st.markdown("""
    <style>
    /* 背景與文字顏色 */
    .main { background-color: #0E1117; color: #FFFFFF; }
    
    /* 冷門馬卡片樣式 */
    [data-testid="stMetric"] {
        background-color: #1F2937;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #FFD700;
        text-align: center;
    }
    
    /* 標題與文字顏色 */
    h1, h2, h3 { color: #FFD700 !important; }
    
    /* 投注建議區顏色 */
    .stAlert {
        background-color: #111827;
        border: 1px solid #00FFA3;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 Happy Valley 冷門狙擊手")

# --- 核心建議區 (最置頂) ---
st.subheader("🎯 臨場 3 匹「冷門機會馬」")
col_bet1, col_bet2, col_bet3 = st.columns(3)

# 這裡的馬匹數據會在週三根據你的截圖進行實時更新
with col_bet1:
    st.metric(label="冷門 1 (首選)", value="6. 名揚四海", delta="55 倍")
    st.caption("1 檔 | 123 磅 | 內欄優勢")

with col_bet2:
    st.metric(label="冷門 2 (次選)", value="9. 正義波", delta="21 倍")
    st.caption("2 檔 | 121 磅 | 輕磅模式")

with col_bet3:
    st.metric(label="冷門 3 (搏爆)", value="4. 亞機拉", delta="19 倍")
    st.caption("3 檔 | 125 磅 | 前速跟前")

st.divider()

# --- 戰術部署區 ---
with st.expander("📝 投注策略與組合 (2X3 / 連贏)", expanded=True):
    st.success("✅ **推薦方案：(4, 6, 9) 互串位置Q (QP)**")
    st.info("💡 **核心邏輯：** 今日 C 賽道利內欄，此 3 匹冷門皆佔好檔，具備極高博彩價值。")

st.divider()

# --- 打賞模組 (方案 A：純文字與代碼版) ---
st.subheader("🧧 貼中咗？支持一下 AI 研發！")

col_pay1, col_pay2 = st.columns(2)

with col_pay1:
    st.markdown("### 💰 打賞方式")
    st.write("如果您覺得預測準確，歡迎請開發者飲杯咖啡支持！")
    
    # 使用 st.code 讓用戶方便點擊複製 FPS ID
    st.markdown("**轉數快 (FPS) ID:**")
    st.code("在此輸入你的轉數快ID", language=None)
    
    st.markdown("**PayMe 打賞連結:**")
    st.info("暫未設置連結 (週三可加入)")

with col_pay2:
    st.markdown("""
    **您的支持是 AI 進化的動力：**
    * ☕️ 請飲咖啡 ($40)
    * 🍱 豐富午餐 ($100)
    * 🎰 研發基金 (自由金額)
    """)

# --- 底部聲明 ---
st.divider()
st.caption("⚠️ 免責聲明：本 App 提供之數據僅供參考，不保證獲利，投注請量力而為。")
st.caption("✅ 數據校對：臨場馬會 App 截圖讀取模式 (準備中)")
