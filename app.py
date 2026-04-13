import streamlit as st

# --- 配置：暴力獵頭模式 ---
st.set_page_config(page_title="Violence Hunter 3x1", layout="wide")
st.title("🔥 暴力波膽狙擊系統 (目標 100x+)")

# --- 今晚暴力 3x1 建議 (基於里昂 0:0 控場邏輯) ---
st.header("📋 今晚暴力 3x1 候選方案")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("第一關：西甲")
    st.write("**華倫西亞 vs 奧沙辛拿**")
    val_score = st.selectbox("建議波膽 A", ["1:0 (6.5x)", "2:0 (8.0x)", "1:1 (6.0x)"])

with col2:
    st.subheader("第二關：意甲")
    st.write("**佛羅倫斯 vs 熱拿亞**")
    flo_score = st.selectbox("建議波膽 B", ["2:0 (7.5x)", "2:1 (8.5x)", "1:0 (6.0x)"])

with col3:
    st.subheader("第三關：英超/法乙")
    st.write("**車路士 vs 愛華頓**")
    che_score = st.selectbox("建議波膽 C", ["2:1 (9.0x)", "3:1 (13.0x)", "2:0 (8.5x)"])

# --- 暴力獲利計算機 ---
st.divider()
st.header("💰 暴力回報試算")

bet_amt = st.number_input("輸入注碼 ($)", value=200)
# 假設平均賠率 (根據選擇自動調整邏輯可後續加入)
est_odds = 7.0 * 8.0 * 9.0  # 模擬 504 倍

potential = bet_amt * est_odds

st.metric("預計暴力派彩", f"${potential:,.0f}", f"{est_odds:.0f} 倍")

# --- 割禾青對沖提示 ---
if st.checkbox("啟動【里昂模式】即時監控"):
    st.info("💡 運作邏輯：若半場 0:0，代表控場劇本成形，波膽生存率提升。")
    if potential > 10000:
        hedge = potential * 0.1
        st.warning(f"🎯 **精準獲利指令**：若頭兩關已過，第三關 70' 仍未出波，建議反手對沖 ${hedge:,.0f} 確保今日體力勞動有回報！")

# --- 獵人筆記 ---
st.text_area("📝 臨場筆記 (如有連環進球即撤退)", placeholder="例如：馬略卡式 36', 40' 連入球 = 劇本暴走...")
