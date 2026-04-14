import streamlit as st

# 1. 強制頁面設定
st.set_page_config(page_title="Predator_Control", layout="wide")

# 2. 核心 CSS 修正：強制數字顯示為金黃色，背景為深灰色
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 30px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }
    div[data-testid="metric-container"] {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #464b5d;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 掠食者：生存反擊控制台")

# --- 1. 歐聯波膽實戰組 ---
st.header("⚽ 今晚歐聯波膽 (03:00)")

# 場次資料 (你可以隨時改名同賠率)
games = [
    {"m": "歐聯 A: 拜仁 vs 兵工廠", "b": "2:2", "o": 12.0},
    {"m": "歐聯 B: 皇馬 vs 曼城", "b": "3:2", "o": 22.0},
    {"m": "歐聯 C: 其他精選", "b": "1:2", "o": 8.5}
]

cols = st.columns(3)
total_odds = 1.0
for i, g in enumerate(games):
    total_odds *= g['o']
    with cols[i]:
        st.markdown(f"**{g['m']}**")
        st.metric(f"選擇: {g['b']}", f"{g['o']} 倍")

st.divider()

# --- 回報計算 (修正顏色版) ---
st.subheader(f"💰 總回報估算 (總倍率: {total_odds:.1f})")
r_cols = st.columns(3)
r_cols[0].metric("投注 $100", f"${int(100 * total_odds):,}")
r_cols[1].metric("投注 $200", f"${int(200 * total_odds):,}")
r_cols[2].metric("投注 $500", f"${int(500 * total_odds):,}")

st.divider()

# --- 2. 聽日 3T 對標組 ---
st.header("🏇 聽日 3T 精確對標")

original = {1: 7.0, 4: 3.4, 10: 8.7, 3: 6.4, 4: 15.0, 9: 5.7, 5: 4.2, 6: 3.0, 11: 14.0}
# 聽朝 10:00 改呢度
live_odds = {1: 7.0, 4: 3.4, 10: 8.7, 3: 6.4, 4: 15.0, 9: 5.7, 5: 4.2, 6: 3.0, 11: 14.0}

results = []
for race, horses in [(5, [1, 4, 10]), (6, [3, 4, 9]), (7, [5, 6, 11])]:
    for h in horses:
        old = original[h]
        now = live_odds[h]
        bias = (now - old) / old * 100
        results.append({"場次": f"R{race}", "馬號": h, "14:41": old, "最新": now, "偏差%": f"{bias:+.1f}%"})

st.table(results)
