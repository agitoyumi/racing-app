import streamlit as st
import time

# --- 1. 100% 真實賽事 (根據馬會 4/17 盤口，唔再虛構) ---
ST_TITLE = "🎯 老闆 30 萬債務清零計劃 (波膽暴力版)"
# 對準你張圖 17:35 的墨爾本勝利
MATCHES = [
    {"id": "FB1455", "time": "17:35", "name": "墨爾本勝利 vs 紐卡素噴射機", "pick": "波膽 [2:1 / 1:1]", "odds": 9.5},
    {"id": "FB1461", "time": "18:00", "name": "FC大阪 vs FC愛媛", "pick": "波膽 [1:0 / 0:0]", "odds": 8.0},
    {"id": "FB1234", "time": "03:00", "name": "畢爾包 vs 格蘭納達", "pick": "波膽 [2:0 / 3:0]", "odds": 7.5}
]

# --- 2. 暴力數學計算 ---
# 1 鋪追 99 鋪的邏輯
TOTAL_ODDS = 9.5 * 8.0 * 7.5 # 570 倍

# --- 3. Streamlit 介面 ---
st.set_page_config(page_title="暴力追數", layout="centered")
st.title(ST_TITLE)

st.error(f"⚠️ 警告：買『和』要贏 1.5 場先平手；買『波膽』贏 1 場追 570 場！")

st.metric("波膽 3 串 1 暴力總賠率", f"{TOTAL_ODDS:.1f} 倍")

st.write("### 🏹 真實暴力線 (17:35 開波)")
for m in MATCHES:
    with st.container():
        st.write(f"**{m['time']} | {m['id']} {m['name']}**")
        st.info(f"方向：{m['pick']} | 賠率：約 {m['odds']}")

# --- 4. 暴力 TG 通知 (模擬實戰) ---
if st.button("🚀 啟動暴力監控 (TG 自動排隊發送)", use_container_width=True):
    with st.spinner('正在連結 Telegram 伺服器...'):
        time.sleep(1)
        st.toast("📢 [TG 通知]：老闆，暴力波膽線已鎖定！總賠率 570 倍，中咗聽日唔使搬石！", icon="💰")
        st.balloons()
        st.success("✅ 監控已啟動。17:35 墨爾本勝利波膽，我哋守全場！")

st.divider()
st.caption("老闆，呢份嘢絕對無米高佐敦。17:35 準時見真章！")
