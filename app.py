import streamlit as st

st.set_page_config(page_title="Predator_Control", layout="wide")

# 強制 CSS：確保黑底金字，一眼睇晒落飛變動
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 32px !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; }
    .stTable { background-color: #1e1e1e; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 掠食者：臨場對標控制台")

# --- 1. 歐聯/英甲 3X1 實戰紀錄 ---
st.header("⚽ 今晚實戰 3x1 (1,376.5 倍)")
t_odds = 6.9 * 9.5 * 21.0
st.subheader(f"預計總回報：投注 $200 -> **${int(200 * t_odds):,}**")

# --- 2. 聽日 3T 臨場變動分析 ---
st.divider()
st.header("🏇 聽日 3T 賠率對標 (最新更新)")

# 14:41 原始種子數據
original = {
    1: 7.0, 4: 3.4, 10: 8.7,   # R5
    3: 6.4, 4: 15.0, 9: 5.7,  # R6
    5: 4.2, 6: 3.0, 11: 14.0  # R7
}

# 🚀 根據你剛報過嚟嘅數據自動更新
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
        # 標記：落飛超過 20% 即係黃色警報
        if bias <= -20:
            status = "🔥 重注落飛"
        elif bias > 10:
            status = "📈 回飛 (變冷)"
        else:
            status = "穩定"
            
        results.append({
            "場次": f"R{race}",
            "馬號": h,
            "14:41 賠率": old,
            "最新賠率": now,
            "偏差 (%)": f"{bias:+.1f}%",
            "狀態": status
        })

st.table(results)

# --- 戰術備忘 ---
st.divider()
st.warning("⚠️ 戰術筆記：R6-4號 落飛跡象最明顯 (-26.7%)，必須盯緊。今晚波膽係種子，中咗就有子彈聽日掃 3T。")
