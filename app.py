import streamlit as st

st.set_page_config(page_title="Predator_Reborn", layout="wide")

# 強制顏色修正：金黃色數字，綠色標題
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 32px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 18px !important; }
    .match-header { color: #00ff00; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 掠食者：精確反擊控制台 (數據修正版)")

# --- 1. 歐聯及英甲/英乙 3X1 實戰清單 ---
st.header("⚽ 歐聯/聯賽 3x1 實戰場次")

# 根據你截圖的賠率與場次精確校正
games = [
    {"m": "英乙：高車士打 vs 域斯咸 (或其他對賽)", "b": "2:2", "o": 14.0},
    {"m": "歐聯：利物浦 vs 巴黎聖日耳門", "b": "3:2", "o": 22.0},
    {"m": "歐聯：馬德里體育會 vs 巴塞隆拿", "b": "1:2", "o": 14.0}
]

total_odds = 1.0
cols = st.columns(3)

for i, g in enumerate(games):
    total_odds *= g['o']
    with cols[i]:
        st.markdown(f"<div class='match-header'>{g['m']}</div>", unsafe_allow_html=True)
        st.metric(f"選擇: {g['b']}", f"{g['o']} 倍")

st.divider()

# --- 投注回報 ---
st.subheader(f"💰 總倍率：{total_odds:.1f} | 命中即重生")
r_cols = st.columns(3)
r_cols[0].metric("投注 $100", f"${int(100 * total_odds):,}")
r_cols[1].metric("投注 $200", f"${int(200 * total_odds):,}")
r_cols[2].metric("投注 $500", f"${int(500 * total_odds):,}")

st.divider()

# --- 2. 聽日 3T 對標組 (15/04) ---
st.header("🏇 聽日 3T 精確對標")

# 14:41 原始數據維持
original = {1: 7.0, 4: 3.4, 10: 8.7, 3: 6.4, 4: 15.0, 9: 5.7, 5: 4.2, 6: 3.0, 11: 14.0}
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
