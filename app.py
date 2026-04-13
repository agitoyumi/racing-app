import streamlit as st
import pandas as pd

# --- 核心配置 ---
st.set_page_config(page_title="Hunter System 2.0", layout="wide")
st.title("🎯 精準獵頭：馬波雙核決策系統")

# --- 側邊欄：資金熔斷 (基於這兩日損血經驗) ---
with st.sidebar:
    st.header("🛡️ 資金安全閥")
    loss_limit = 1000
    today_loss = st.number_input("今日已損血 ($)", value=0)
    if today_loss >= loss_limit:
        st.error("🛑 熔斷！今日體力勞動辛苦，唔准再下注。")
    
    st.markdown("---")
    st.info("💡 經驗總結：\n1. 避開連環進球場次\n2. 專注下半場控場劇本")

# --- 第一部分：動態劇本篩選 ---
st.header("🕵️ 獵頭場次過濾")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚽ 足球：劇本修正")
    half_score = st.text_input("半場比數 (例如 0:0, 2:0)", value="0:0")
    
    # 自動化建議邏輯
    if half_score == "0:0":
        st.success("🎯 里昂模式：下半場發力機會高，考慮 1:0 / 2:0 波膽。")
    elif "2" in half_score or "3" in half_score:
        st.warning("🚨 屠殺警告：劇本已偏離，唔好追悶局，考慮放棄此場。")
    else:
        st.info("⚖️ 平衡劇本：觀察 65' 後有無賠率異常下挫。")

with col2:
    st.subheader("🏇 賽馬：重注過濾")
    horse_type = st.radio("賽馬性質：", ["重心過關", "冷門摸索"])
    market_move = st.checkbox("臨場賠率瘋狂跳動？")
    if market_move:
        st.warning("⚠️ 人為因素介入：建議將注碼減半，或改為單場投注。")

# --- 第二部分：獲利對沖計算機 (最短時間獲利關鍵) ---
st.header("💰 過關鎖定利潤 (割禾青模組)")

with st.expander("📊 3x1 / 2x1 對沖模擬", expanded=True):
    total_odds = st.number_input("組合總賠率", value=400.0)
    bet_amount = st.number_input("下注金額 ($)", value=500)
    potential_payout = total_odds * bet_amount
    
    st.metric("預計回報", f"${potential_payout:,.0f}")
    
    st.markdown("### 🏹 走地操作指引")
    if st.button("計算對沖位"):
        hedge_amt = potential_payout * 0.15
        st.write(f"👉 如果前兩關已過，第三關進入 75' 分鐘：")
        st.write(f"✅ 建議反手對沖注碼：**${hedge_amt:,.0f}**")
        st.write(f"🔒 確保利潤：**${(potential_payout * 0.4):,.0f}** (無論結果如何)")

# --- 第三部分：兩日數據覆盤日誌 ---
st.header("📝 數據庫：人為因素規律")
history_data = {
    '日期': ['04/12', '04/13', '04/13', '04/13'],
    '場次': ['全日', '馬略卡', '畢爾包', '里昂'],
    '劇本特徵': ['全線殺熱', '連環進球破壞', '上半場崩潰', '完美下半場控場'],
    '獲利啟示': ['損血 800', '避開連環球', '不可輕信主場', '0:0 是機會']
}
st.table(pd.DataFrame(history_data))
