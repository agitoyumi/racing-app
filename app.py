import streamlit as st

st.set_page_config(page_title="Predator_Control", layout="wide")

# CSS 調整：確保手機睇得清楚
st.markdown("""<style>.stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }</style>""", unsafe_allow_html=True)

st.title("🎯 掠食者：生存反擊控制台")

# --- 1. 歐聯波膽 3x1 攻擊組 (03:00 AM) ---
st.header("⚽ 歐聯波膽戰備")
col_a, col_b, col_c = st.columns(3)

# 根據今晚對賽手動輸入 (範例：皇馬 vs 曼城, 兵工廠 vs 拜仁)
with col_a:
    st.subheader("場次 A")
    m1 = st.text_input("對賽 1", "皇馬 vs 曼城")
    b1 = st.selectbox("波膽 1", ["2:2", "3:2", "1:2", "其他"], index=0)
    o1 = st.number_input("賠率 1", value=12.0)

with col_b:
    st.subheader("場次 B")
    m2 = st.text_input("對賽 2", "兵工廠 vs 拜仁")
    b2 = st.selectbox("波膽 2", ["2:2", "3:2", "1:2", "其他"], index=1)
    o2 = st.number_input("賠率 2", value=22.0)

with col_c:
    st.subheader("場次 C")
    m3 = st.text_input("對賽 3", "歐聯精選")
    b3 = st.selectbox("波膽 3", ["2:2", "3:2", "1:2", "其他"], index=2)
    o3 = st.number_input("賠率 3", value=8.5)

total_odds = o1 * o2 * o3

st.divider()
st.subheader(f"💰 總回報估算 (總倍率: {total_odds:.1f})")
r_cols = st.columns(3)
r_cols[0].metric("投注 $100", f"${int(100 * total_odds):,}")
r_cols[1].metric("投注 $200", f"${int(200 * total_odds):,}")
r_cols[2].metric("投注 $500", f"${int(500 * total_odds):,}")

# --- 2. 聽日 3T 翻身組 (14:41 對標) ---
st.divider()
st.header("🏇 聽日 3T 精確對標")

# 原始數據 (14:41)
original = {
    1: 7.0, 4: 3.4, 10: 8.7,   # R5
    3: 6.4, 4: 15.0, 9: 5.7,  # R6
    5: 4.2, 6: 3.0, 11: 14.0  # R7
}

# 聽朝 10:00 改呢度
live_odds = {
    1: 7.0, 4: 3.4, 10: 8.7, 
    3: 6.4, 4: 15.0, 9: 5.7, 
    5: 4.2, 6: 3.0, 11: 14.0
}

# 顯示表格
st.write("### 臨場偏差監控")
results = []
for race, horses in [(5, [1, 4, 10]), (6, [3, 4, 9]), (7, [5, 6, 11])]:
    for h in horses:
        old = original[h]
        now = live_odds[h]
        bias = (now - old) / old * 100
        status = "⚠️ 落飛" if bias <= -20 else "穩定"
        results.append({"場次": f"R{race}", "馬號": h, "14:41": old, "最新": now, "偏差%": f"{bias:+.1f}%", "狀態": status})

st.table(results)

st.sidebar.markdown("""
### 🏁 掠食者心法
1. **排空情緒**：只睇數據，唔聽馬評。
2. **物理優勢**：A 欄 + 慢步速 = 放頭馬命根。
3. **金錢意志**：今晚波膽係種子，聽日 3T 係重生。
""")
