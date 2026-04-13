import streamlit as st

# --- 頁面風格配置：獵人黑紅主題 ---
st.set_page_config(page_title="Miracle Hunter 3.6", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #161b22; border: 1px solid #ff4b4b; border-radius: 12px; padding: 20px; }
    div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 標題與核心精神 ---
st.title("🎯 Miracle Hunter 3.6：重生計畫")
st.markdown("### 「是但中一條，就是重生的開始。」")

# --- 側邊欄：獵人資金控制 ---
with st.sidebar:
    st.header("🛡️ 獵人資金庫")
    unit_bet = st.select_slider("單線注碼 (HKD)", options=[100, 200, 500], value=100)
    total_investment = unit_bet * 3
    st.divider()
    st.markdown(f"📊 **今晚總投入：${total_investment}**")
    st.write("---")
    st.info("💡 戰略：用 $300 買三個重生機會。不囂不燥，用結果說話。")

# --- 重生方案數據對標 (基於你的直覺與截圖數據) ---
# 方案 A: 你的核心直覺 (1:0 x 3:1 x 1:1)
# 方案 B: 暴力質變位 (2:0 x 3:2 x 2:1)
# 方案 C: 數據防反位 (1:0 x 2:1 x 1:0)

plans = {
    "🎯 方案 A (直覺核心)": {
        "desc": "費倫 1:0 | 曼聯 3:1 | 唐迪拉 1:1",
        "odds": 7.0 * 13.0 * 6.5,
        "note": "最吻合 76-90' 絕殺數據與個人直覺。"
    },
    "🔥 方案 B (極致暴力)": {
        "desc": "費倫 2:0 | 曼聯 3:2 | 唐迪拉 2:1",
        "odds": 8.5 * 22.0 * 9.5,
        "note": "挑戰 1700+ 倍回報，專博打吡爆發瞬間。"
    },
    "🛡️ 方案 C (數據防反)": {
        "desc": "費倫 1:0 | 曼聯 2:1 | 唐迪拉 1:0",
        "odds": 7.0 * 9.5 * 7.5,
        "note": "利用控場慣性建立的備選暴力線。"
    }
}

# --- 介面呈現 ---
col1, col2, col3 = st.columns(3)
plan_keys = list(plans.keys())

for i, col in enumerate([col1, col2, col3]):
    key = plan_keys[i]
    with col:
        st.subheader(key)
        st.markdown(f"🎭 **劇本：** `{plans[key]['desc']}`")
        payout = unit_bet * plans[key]['odds']
        st.metric("預計回報", f"${payout:,.0f}", f"{plans[key]['odds']:.0f} 倍")
        st.caption(plans[key]['note'])
        st.divider()

# --- 聽朝驗證區 ---
st.header("🔍 聽朝驗證區 (用結果說話)")
st.write("起身後，只睇有無任何一條「全中」。")

c1, c2, c3 = st.columns(3)
with c1:
    res_a = st.checkbox("方案 A 全中？")
with c2:
    res_b = st.checkbox("方案 B 全中？")
with c3:
    res_c = st.checkbox("方案 C 全中？")

if res_a or res_b or res_c:
    st.balloons()
    st.success("🎉 重生開始！準備辭職。")
elif st.button("紀錄今晚測試"):
    st.write("📡 數據已儲存。若未中，明晚收工繼續優化。")

st.markdown("---")
st.caption("平常心測試模式 | 嚴禁囂張 | 數據導向")
