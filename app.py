import streamlit as st

st.set_page_config(page_title="Predator_Reborn", layout="wide")
st.title("🎯 掠食者：生存反擊戰 (波馬合一控制台)")

# --- 1. 歐聯波膽 3x1 實戰面板 ---
st.header("⚽ 今晚歐聯波膽過關 (03:00 AM)")

# 定義波膽劇本
football_data = [
    {"match": "歐聯場次 A (例如 皇馬 vs 曼城)", "pick": "2:2", "odds": 12.0},
    {"match": "歐聯場次 B (例如 阿仙奴 vs 拜仁)", "pick": "3:2", "odds": 22.0},
    {"match": "歐聯場次 C (例如 歐聯分組/半準決賽)", "pick": "1:2", "odds": 8.5}
]

# 顯示單場詳情
cols = st.columns(3)
for i, game in enumerate(football_data):
    with cols[i]:
        st.info(f"**{game['match']}**")
        st.metric(f"選擇: {game['pick']}", f"{game['odds']} 倍")

# 計算總回報
total_odds = 1.0
for game in football_data:
    total_odds *= game['odds']

st.divider()

# 投注與回報
st.subheader(f"📊 預計總倍率：{total_odds:.1f} 倍")
amt_100, amt_200, amt_500 = 100, 200, 500

r_cols = st.columns(3)
r_cols[0].metric("投注 $100", f"${int(amt_100 * total_odds):,}")
r_cols[1].metric("投注 $200", f"${int(amt_200 * total_odds):,}")
r_cols[2].metric("投注 $500", f"${int(amt_500 * total_odds):,}")

st.divider()

# --- 2. 聽日 3T 對標數據 ---
st.header("🏇 聽日 3T 對標 (14:41 原始數據)")

# 手動更新區：聽朝 10:00 改 live_odds
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

# 跑法備註 (自用)
horse_info = {
    1: "放頭", 4: "前領", 10: "中置",
    3: "前領", 4: "前領", 9: "放頭",
    5: "前領", 6: "前領", 11: "中置"
}

# 格式化輸出
report = ""
for race, horses in [(5, [1, 4, 10]), (6, [3, 4, 9]), (7, [5, 6, 11])]:
    report += f"【第 {race} 場】\n"
    for h in horses:
        old = original[h]
        now = live_odds[h]
        bias = (now - old) / old * 100
        style = horse_info[h]
        tag = " [!] 落飛" if bias <= -20 else ""
        report += f" #{h:<2} ({style}) : {old:>4.1f} -> {now:>4.1f} ({bias:>+5.1f}%) {tag}\n"
    report += "-" * 40 + "\n"

st.text_area("聽朝 10:00 校對區", report, height=350)

st.warning("⚠️ 記住初心：一星期中 3-4 次。今晚波膽係子彈，聽日 3T 係翻身。")
