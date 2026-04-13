import streamlit as st

# --- 全局風格設定 ---
st.set_page_config(page_title="Miracle Hunter 3.0", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Miracle Hunter 3.0：不再平庸模式")

# --- 第一部分：暴力槓桿配置 (固定注碼) ---
with st.sidebar:
    st.header("🛡️ 獵人資金指令")
    bet_level = st.select_slider(
        "選擇出擊級別",
        options=[100, 200, 500],
        help="500 蚊級別僅限於有盈利時啟動"
    )
    st.markdown(f"**目前注碼：${bet_level}**")
    st.divider()
    st.info("💡 奇蹟門檻：$7,000\n🚀 質變目標：$70,000+")

# --- 第二部分：今晚「奇蹟瞬間」場次設定 ---
st.header("🔭 暴力 3x1 劇本掃描")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("⚽ 西甲：華倫西亞")
    odds_1 = st.number_input("賠率 (1:0/2:0)", value=7.5, key="o1")
    st.caption("里昂模式：半場 0:0 係收割信號")

with col2:
    st.subheader("⚽ 意甲：佛羅倫斯")
    odds_2 = st.number_input("賠率 (2:0/2:1)", value=9.0, key="o2")
    st.caption("控場模式：主隊戰意壓制")

with col3:
    st.subheader("⚽ 英超：車路士")
    odds_3 = st.number_input("賠率 (2:1/3:1)", value=12.0, key="o3")
    st.caption("暴力模式：必失波但火力強")

# --- 第三部分：同步對比 (3x1 奇蹟 vs 3x7 容錯) ---
total_odds = odds_1 * odds_2 * odds_3
payout_3x1 = bet_level * total_odds
payout_3x7_top = (bet_level / 7) * total_odds # 假設將同等預算拆分

st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("🚀 3x1 奇蹟模式 (單點爆破)")
    st.metric("預計派彩", f"${payout_3x1:,.0f}", f"{total_odds:.0f} 倍")
    if payout_3x1 >= 100000:
        st.warning("🔥 偵測到『質變級』回報：準備脫離平庸！")

with c2:
    st.subheader("🛡️ 3x7 暴力容錯 (每注 ${:.0f})".format(bet_level/7))
    st.metric("最高回報", f"${payout_3x7_top:,.0f}")
    st.write("適合：捕捉 5:1 類痴線波，即使斷一場仍能獲利 7k+。")

# --- 第四部分：極端劇本 (5:1) 預警系統 ---
st.divider()
st.header("🚨 暴力異動：5:1 屠殺偵測器")

col_a, col_b = st.columns(2)
with col_a:
    early_goals = st.checkbox("15分鐘內出現進球？")
    half_time_chaos = st.checkbox("半場出現 3 球或以上？")

with col_b:
    if early_goals and half_time_chaos:
        st.error("🛑 警告：偵測到桑坦德式屠殺！")
        st.write("👉 3x1 波膽失效，建議立即單場補『其他』或『5:1』！")
    elif early_goals:
        st.warning("⚠️ 劇本加速：密切留意大球盤口。")
    else:
        st.success("✅ 控場中：里昂 0:0 模式觀察中。")

st.markdown("---")
st.caption("奇蹟只係一瞬間出現。當你捉到，你就唔再係普通賭徒。")
