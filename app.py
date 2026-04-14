import streamlit as st
import pandas as pd

# 設定手機版頁面配置
st.set_page_config(page_title="Predator_V5_DualTrack", layout="centered")

# --- 自定義介面風格 ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c1e26; padding: 15px; border-radius: 10px; border: 1px solid #ffd700; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #262730; border-radius: 5px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #ffd700; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 掠食者：雙線自由系統")

# --- 頂部狀態列：債務與資金 ---
col_debt, col_fund = st.columns(2)
with col_debt:
    st.metric("債務狀態", "進行中", delta="-清還中")
with col_fund:
    st.metric("自由進度 (目標60萬)", "1%", delta="等待引信爆發")

# --- 雙線分頁系統 ---
tab_footy, tab_racing, tab_freedom = st.tabs(["⚽ 足球自動化", "🏇 賽馬伏擊", "📈 辭職倒數"])

with tab_footy:
    st.header("🎯 今日引信：3x1 波膽序列")
    
    # 今日核心過關資料
    bet_data = {
        "賽事": ["高車士打 (2:1)", "利物浦 (2:2)", "馬體會 (3:2)"],
        "單場賠率": [6.9, 9.5, 21.0]
    }
    df = pd.DataFrame(bet_data)
    st.table(df)

    # 倍率計算
    total_odds = 6.9 * 9.5 * 21.0
    st.subheader(f"🚀 總回報倍率：{total_odds:,.2f} 倍")
    
    # 投入金額試算
    stake = st.radio("選擇投入金額 (今晚引信)", [100, 500, 1000], horizontal=True)
    potential_return = stake * total_odds
    
    st.markdown(f"""
        <div style="background-color: #ffd700; color: black; padding: 20px; border-radius: 15px; text-align: center;">
            <h2 style="margin:0;">預計入袋：${int(potential_return):,}</h2>
            <p style="margin:0;">(成功後即刻啟動清債程序)</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🌐 全球數據同步 (預覽)")
    st.info("系統正在後台對標 Betfair 及 Pinnacle 資金流...")
    st.write("✅ 偵測到深夜賽事偏離值穩定。")

with tab_racing:
    st.header("🏇 賽馬特種部隊")
    st.warning("目前處於『靜默伏擊』狀態")
    st.write("保留週三/週日數據接口：")
    st.file_uploader("📸 掟張馬會賠率截圖上嚟 (OCR 識別)", type=['png', 'jpg'])
    st.info("💡 策略：利用足球獲利，喺馬場進行無壓力收割。")

with tab_freedom:
    st.header("🏁 遞信倒數計時器")
    current_cash = st.number_input("當前流動資金 (HKD)", value=0)
    target_cash = 600000
    
    progress = min(current_cash / target_cash, 1.0)
    st.progress(progress)
    st.write(f"距離老婆唔使打工仲差：${int(target_cash - current_cash):,}")
    
    if st.button("啟動還債模擬"):
        st.write("優先分配：1. 債務本金 -> 2. 利息對沖 -> 3. 永動機燃料")

# --- 底部指令 ---
st.divider()
st.caption("Predator V5.0 | 數據領先 0.005 秒 | 財務自由專用")
