import streamlit as st

# 1. 頁面基礎設定
st.set_page_config(page_title="Predator_Control", layout="wide")

# 2. 強制 CSS：確保黑底金字，數字極大化，方便公司偷睇
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 35px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 18px !important; }
    .match-header { color: #00ff00; font-weight: bold; font-size: 20px; margin-bottom: 5px; }
    div[data-testid="metric-container"] { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 掠食者：精確反擊控制台")

# --- 1. 歐聯/英乙 3X1 實戰清單 ---
st.header("⚽ 03:00 AM 實戰劇本 (1,376.5 倍)")

# 嚴格校對數據
games = [
    {"m": "英乙：高車士打 vs 域斯咸", "b": "2:1", "o": 6.9},
    {"m": "歐聯：利物浦 vs 巴黎聖日耳門", "b": "2:2", "o": 9.5},
    {"m": "歐聯：馬德里體育會 vs 巴塞隆拿", "b": "3:2", "o": 21.0}
]

total_odds = 6.9 * 9.5 * 21.0
cols = st.columns(3)

for i, g in enumerate(games):
    with cols[i]:
        st.markdown(f"<div class='match-header'>{g['m']}</div>", unsafe_allow_html=True)
        st.metric(f"選擇: {g['b']}", f"{g['o']} 倍")

st.divider()

# --- 投注回報計算 ---
st.subheader(f"💰 總倍率：{total_odds:.1f} | 撬動命運")
r_cols = st.columns(3)
r_cols[0].metric("投注 $100", f"${int(100 * total_odds):,}")
r_cols[1].metric("投注 $200", f"${int(200 * total_odds):,}")
r_cols[2].metric("投注 $500", f"${int(500 * total_odds):,}")

st.divider()

# --- 2. 聽日 3T 對標組 (14:41 原始初心) ---
st.header("🏇 聽日 3T 精確對標 (自用)")

original = {1: 7.0, 4: 3.4, 10: 8.7, 3: 6.4, 4: 15.0, 9: 5.7, 5: 4.2, 6: 3.0, 11: 14.0}
# 聽朝 10:00 根據臨場賠率改呢度
live_odds = {1: 7.0, 4: 3.4, 10: 8.7, 3: 6.4, 4: 15.0, 9: 5.7, 5: 4.2, 6: 3.0, 11: 14.0}

results = []
for race, horses in [(5, [1, 4, 10]), (6, [3, 4, 9]), (7, [5, 6, 11])]:
    for h in horses:
        old = original[h]
        now = live_odds[h]
        bias = (now - old) / old * 100
        tag = "⚠️ 落飛" if bias <= -20 else "穩定"
        results.append({"場次": f"R{race}", "馬號": h, "14:41": old, "最新": now, "偏差%": f"{bias:+.1f}%", "狀態": tag})

st.table(results)
