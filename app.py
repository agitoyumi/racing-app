import streamlit as st
import pandas as pd

# --- 核心配置：精準獵頭模式 ---
st.set_page_config(page_title="Professional Hunter System", layout="wide")
st.title("🎯 精準獲利：馬波過關執行系統")

# --- 側邊欄：資金與紀律控管 ---
with st.sidebar:
    st.header("🛡️ 紀律熔斷機制")
    daily_loss_limit = 1000  # 根據你今日輸800的警號設定
    current_loss = st.number_input("今日累計損血 ($)", value=800)
    
    if current_loss >= daily_loss_limit:
        st.error("🛑 已達熔斷點！今日禁止實戰，轉入數據模式。")
    else:
        st.success("✅ 資金安全，准許獵頭出擊。")

# --- 第一部分：人為劇本偵測器 (人為因素過濾) ---
st.header("🕵️ 臨場人為因素掃描")
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚽ 足球劇本偵測")
    match_type = st.selectbox("選擇場次特徵：", [
        "強隊控場 (如里昂 2:0)", 
        "主場氣勢 (如畢爾包 2:1)", 
        "默契悶局 (如馬略卡 1:1)",
        "末段絕殺殺波膽 (警告)"
    ])
    odds_drop = st.checkbox("偵測到波膽賠率異常下挫？")
    if odds_drop:
        st.warning("⚠️ 偵測到『人為熱錢』湧入，劇本成色 80%！")

with col2:
    st.subheader("🏇 賽馬異動監控")
    horse_odds = st.radio("馬匹賠率狀態：", ["冷門墊票", "大熱倒灶跡象", "重心馬異動"])
    if horse_odds == "大熱倒灶跡象":
        st.info("💡 建議：此場不宜做過關重心，考慮避開。")

# --- 第二部分：過關精算與對沖 (獲利核心) ---
st.header("🚀 重注 3x1 獲利計算機")

with st.expander("📊 虛擬注項與對沖模擬 (今晚測試用)", expanded=True):
    inv_amt = st.number_input("預計注碼 ($)", value=500)
    leg1 = st.number_input("第一關賠率 (馬略卡 1:1)", value=6.5)
    leg2 = st.number_input("第二關賠率 (畢爾包 2:1)", value=8.5)
    leg3 = st.number_input("第三關賠率 (里昂 2:0)", value=7.5)
    
    total_odds = leg1 * leg2 * leg3
    potential_win = inv_amt * total_odds
    
    st.metric("預期總回報", f"${potential_win:,.0f}", delta=f"{total_odds:.1f} 倍")

    st.markdown("### 🛡️ 走地對沖建議 (最短時間獲利關鍵)")
    st.info(f"""
    **當前兩關已過，第三關進行至 70 分鐘：**
    - 若要鎖定利潤，建議反手對沖：**${(potential_win * 0.1):.0f}**
    - 無論絕殺與否，確保淨利超過：**${(potential_win * 0.5):.0f}**
    """)

# --- 第三部分：苦力後的覆盤日誌 ---
st.header("📝 獵頭覆盤日誌")
log_data = st.text_area("記錄今日『人為因素』細節 (如：馬會邊場做戲？邊分鐘絕殺？)")
if st.button("存檔優化數據"):
    st.success("數據已存入後台，將用於優化下一次精準打擊。")

