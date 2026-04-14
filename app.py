import streamlit as st

st.set_page_config(page_title="Predator_Reborn", layout="centered")
st.title("🎯 掠食者：生存反擊戰")

# --- 1. 歐聯波膽 3x1 計數機 ---
st.header("⚽ 今晚歐聯波膽 3x1")

# 假設今晚三場波膽平均賠率 (你可以根據實際盤口修改)
# 2:2 (約12倍) | 3:2 (約22倍) | 1:2 (約8.5倍)
odds_list = [12.0, 22.0, 8.5]
total_odds = odds_list[0] * odds_list[1] * odds_list[2]

st.info(f"當前組合預計總倍率：約 **{total_odds:.1f}** 倍")

# 回報試算表
st.write("### 💰 投注回報預測")
bet_amounts = [100, 200, 500]
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("投注 $100", f"${int(100 * total_odds)}")
with col2:
    st.metric("投注 $200", f"${int(200 * total_odds)}")
with col3:
    st.metric("投注 $500", f"${int(500 * total_odds)}")

st.divider()

# --- 2. 聽日 3T 對標報告 ---
st.header("🏇 聽日 3T 對標報告")

live_odds = {
    1: 7.0, 4: 3.4, 10: 8.7,   # R5
    3: 6.4, 4: 15.0, 9: 5.7,  # R6
    5: 4.2, 6: 3.0, 11: 14.0  # R7
}

original = {
    1: 7.0, 4: 3.4, 10: 8.7, 
    3: 6.4, 4: 15.0, 9: 5.7, 
    5: 4.2, 6: 3.0, 11: 14.0
}

report = ""
for race, horses in [(5, [1, 4, 10]), (6, [3, 4, 9]), (7, [5, 6, 11])]:
    report += f"\n【第 {race} 場】\n"
    for h in horses:
        old = original[h]
        now = live_odds[h]
        bias = (now - old) / old * 100
        alert = " [!] 落飛" if bias <= -20 else ""
        report += f" 馬#{h:<2} : {old:>4.1f} -> {now:>4.1f} ({bias:>+5.1f}%) {alert}\n"
    report += "-" * 30 + "\n"

st.text(report)

st.warning("⚠️ 提醒：波膽中咗先係子彈，3T 係用嚟翻身。一星期中 3-4 次就夠。")
