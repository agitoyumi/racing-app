import streamlit as st
import pandas as pd

# --- 核心配置 ---
st.set_page_config(page_title="Hunter Pro: 3x1 vs 3x7", layout="wide")
st.title("🎯 獵頭決策板：3x1 與 3x7 同步監控")

# --- 數據初始化 (今晚場次) ---
matches = [
    {"name": "華倫西亞", "main_odds": 6.5, "sub_odds": 8.5, "main_score": "1:0", "sub_score": "2:0"},
    {"name": "佛羅倫斯", "main_odds": 8.0, "sub_odds": 9.0, "main_score": "2:0", "sub_score": "2:1"},
    {"name": "車路士", "main_odds": 9.5, "sub_odds": 13.0, "main_score": "2:1", "sub_score": "3:1"}
]

# --- 第一部分：同步決策儀表板 ---
st.header("⚖️ 投資效率對比")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🔥 3x1 重注模式 (一擊必殺)")
    bet_3x1 = st.number_input("3x1 總注碼 ($)", value=200, step=50)
    total_odds_3x1 = matches[0]['main_odds'] * matches[1]['main_odds'] * matches[2]['main_odds']
    potential_3x1 = bet_3x1 * total_odds_3x1
    
    st.metric("3x1 預期派彩", f"${potential_3x1:,.0f}", f"{total_odds_3x1:.0f} 倍")
    st.info("⚠️ 優點：命中後利潤最大化。\n❌ 缺點：斷一場即全損。")

with col_b:
    st.subheader("🛡️ 3x7 暴力模式 (容錯收割)")
    unit_3x7 = st.number_input("3x7 每注金額 ($)", value=20, step=10)
    total_cost_3x7 = unit_3x7 * 7
    st.write(f"總成本: ${total_cost_3x7}")
    
    # 模擬中兩場(最低賠率)與中三場(最高賠率)
    min_2x1 = unit_3x7 * (matches[0]['main_odds'] * matches[1]['main_odds'])
    max_3x1 = unit_3x7 * (matches[0]['sub_odds'] * matches[1]['sub_odds'] * matches[2]['sub_odds'])
    
    st.metric("3x7 保底派彩 (中2場)", f"${min_2x1:,.0f}")
    st.metric("3x7 極限派彩 (中3場)", f"${max_3x1:,.0f}")
    st.info("✅ 優點：中兩場已回本翻倍。\n⭐ 特點：大幅降低『人為爆冷』風險。")

# --- 第二部分：今晚暴力波膽建議 ---
st.divider()
st.header("📋 今晚「里昂模式」精選組合")

cols = st.columns(3)
for i, m in enumerate(matches):
    with cols[i]:
        st.markdown(f"### {m['name']}")
        st.write(f"**主力：{m['main_score']}** ({m['main_odds']}x)")
        st.write(f"**次選：{m['sub_score']}** ({m['sub_odds']}x)")
        st.progress(0.4) # 模擬信心值

# --- 第三部分：動態劇本監控 (同步更新) ---
st.divider()
st.subheader("🕵️ 走地動態偵測")
match_progress = st.select_slider("當前比賽狀態", options=["未開賽", "半場 0:0", "已入1球", "劇本暴走"])

if match_progress == "半場 0:0":
    st.balloons()
    st.success("🎯 偵測到『里昂控場劇本』！波膽生存率大幅飆升，請鎖定 3x7 回報。")
elif match_progress == "劇本暴走":
    st.error("🛑 偵測到連環進球！建議放棄對沖，保留體力勞動本金。")

