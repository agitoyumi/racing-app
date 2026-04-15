import streamlit as st

st.set_page_config(page_title="Predator_Full_Control", layout="wide")

# CSS 強制：金黃色數字，確保一眼睇到回報同變動
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 32px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; }
    .match-header { color: #00ff00; font-weight: bold; font-size: 20px; }
    .stTable { background-color: #1e1e1e; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 掠食者：反擊全功能控制台")

# --- 1. 歐聯/英乙 3X1 實戰清單 (鎖定劇本) ---
st.header("⚽ 今晚實戰波膽 3x1")

# 根據你最後確定的數據：高車士打 2:1(6.9), 利記 2:2(9.5), 馬體會 3:2(21)
football_games = [
    {"m": "英乙：高車士打 vs 域斯咸", "b": "2:1", "o": 6.9},
    {"m": "歐聯：利物浦 vs 巴黎聖日耳門", "b": "2:2", "o": 9.5},
    {"m": "歐聯：馬德里體育會 vs 巴塞隆拿", "b": "3:2", "o": 21.0}
]

total_odds = 6.9 * 9.5 * 21.0
f_cols = st.columns(3)

for i, g in enumerate(football_games):
    with f_cols[i]:
        st.markdown(f"<div class='match-header'>{g['m']}</div>", unsafe_allow_html=True)
        st.metric(f"選擇: {g['b']}", f"{g['o']} 倍")

st.divider()

# --- 投注回報預測 ---
st.subheader(f"💰 總倍率：{total_odds:.1f} | 命中即重生")
r_cols = st.columns(3)
r_cols[0].metric("投注 $100", f"${int(100 * total_odds):,}")
r_cols[1].metric("投注 $200", f"${int(200 * total_odds):,}")
r_cols[2].metric("投注 $500", f"${int(500 * total_odds):,}")

# --- 2. 聽日 3T 臨場變動分析 (已更新最新賠率) ---
st.divider()
st.header("🏇 聽日 3T 賠率臨場對標")

# 14:41 原始種子數據
original = {
    1: 7.0, 4: 3.4, 10: 8.7,   # R5
    3: 6.4, 4: 15.0, 9: 5.7,  # R6
    5: 4.2, 6: 3.0, 11: 14.0  # R7
}

# 你剛報過嚟嘅最新賠率
live_odds = {
    1: 6.9, 4: 3.4, 10: 8.8, 
    3: 6.8, 4: 11.0, 9: 6.0, 
    5: 4.0, 6: 3.2, 11: 16.0
}

results = []
for race, horses in [(5, [1, 4, 10]), (6, [3, 4, 9]), (7, [5, 6, 11])]:
    for h in horses:
        old = original[h]
        now = live_odds[h]
        bias = (now - old) / old * 100
        
        if bias <= -20:
            status = "🔥 大戶重注"
        elif bias > 10:
            status = "📈 變冷"
        else:
            status = "穩定"
            
        results.append({
            "場次": f"R{race}",
            "馬號": h,
            "14:41": old,
            "最新": now,
            "偏差 (%)": f"{bias:+.1f}%",
            "狀態": status
        })

st.table(results)

st.warning("⚠️ 筆記：R6-4號 由15倍跌至11倍 (-26.7%)，絕對係今場焦點。今晚波膽 3x1 係子彈，中咗就係贏 4 次入面最爽嗰次。")
