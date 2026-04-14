import streamlit as st

# 1. 強制設定頁面，減少 Loading
st.set_page_config(page_title="Predator_Reborn", layout="centered")

st.title("🎯 掠食者：生存反擊戰")

# ⚽ 今晚歐聯 (劇本備忘)
st.subheader("今晚波膽 3x1")
st.code("2:2 | 3:2 | 1:2", language="text")

# 🏇 聽日 3T 對標 (14:41 盤口)
# 手動更新區：請喺下面 live_odds 改數字
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

st.subheader("聽日 3T 對標報告")

# 用最原始嘅文字格式，防止黑屏
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

# 用 st.text 直接噴出數據，唔會出錯
st.text(report)

st.warning("指令：$10 單式 3T | 專注物理優勢 | 贏 4 次就夠")
