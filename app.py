import streamlit as st

# --- 頁面配置 ---
st.set_page_config(page_title="Miracle Hunter 3.1", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { background-color: #11151c; border: 2px solid #2e3b4e; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Miracle Hunter 3.1：質變獵人模式")
st.write("「奇蹟只係一瞬間出現。捉到，你就唔再係普通賭徒。」")

# --- 側邊欄：獵人資金庫 ---
with st.sidebar:
    st.header("💰 獵人指令面板")
    bet_amount = st.select_slider(
        "選擇出擊注碼",
        options=[100, 200, 500],
        help="500 蚊級別建議僅限於有盈利時啟動"
    )
    st.divider()
    st.markdown(f"### 當前戰鬥注碼：**${bet_amount}**")
    st.info("💡 7k 門檻：已自動對標\n🚀 質變目標：$70,000+")

# --- 第一部分：直覺組合數據 (1:0 x 3:1 x 1:1) ---
st.header("🔭 今晚暴力 3x1 組合監控")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇮🇹 費倫天拿")
    o1 = st.number_input("1:0 賠率", value=7.0)
    st.caption("絕殺概率: 41% (76-90')")

with col2:
    st.subheader("🏴󠁧󠁢󠁥󠁮󠁧󠁿 曼聯 (暴力位)")
    o2 = st.number_input("3:1 賠率", value=13.0)
    st.caption("絕殺概率: 29% (宿敵對決)")

with col3:
    st.subheader("🇵🇹 唐迪拉")
    o3 = st.number_input("1:1 賠率", value=6.5)
    st.caption("絕殺概率: 28% (護級大戰)")

# --- 第二部分：奇蹟回報計算 ---
total_odds = o1 * o2 * o3
payout = bet_amount * total_odds

st.divider()
c_win, c_ratio = st.columns(2)

with c_win:
    st.metric("🚀 奇蹟預計派彩", f"${payout:,.0f}")
with c_ratio:
    st.metric("🔥 總賠率槓桿", f"{total_odds:.1f} 倍")

# --- 第三部分：獵人狀態判斷 ---
if payout >= 100000:
    st.error("🚨 【質變級警報】：呢鋪捕捉成功，直接進入人生新階段。")
    st.balloons()
elif payout >= 7000:
    st.success(f"✅ 【獵頭成功】：回報約 ${payout:,.0f}，大幅超越 7k 門檻。")

# --- 第四部分：絕殺時段監控器 (根據截圖數據) ---
st.divider()
st.header("🕵️ 劇本執行：76-90' 絕殺監控")
st.write("根據 18:39 數據截圖，三場波尾段均屬高危進球期。")

match_timer = st.select_slider(
    "比賽進度 (分鐘)",
    options=list(range(0, 91, 5)),
    value=0
)

if match_timer >= 75:
    st.warning("⚠️ 進入絕殺時段！數據顯示費倫天拿有 41% 機會喺呢度改寫劇本。")
    if st.button("偵測 5:1/3:2 暴力異動"):
        st.write("📡 掃描中... 若曼聯場波變 2:1，立即留意 3:1 奇蹟出現！")
