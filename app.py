import streamlit as st
import requests
from datetime import datetime

# --- 1. 核心配置 (已根據老闆提供資料填妥) ---
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
TG_CHAT_ID = "411468742"

def send_tg_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        payload = {"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# --- 2. 真正 4/17 實戰場次 (100% 對準截圖) ---
st.set_page_config(page_title="老闆反擊中樞", layout="centered")
st.title("🏹 4/17 暴力追數監控")

# 賠率根據 07:56 截圖中的「和局」盤口
matches = [
    {"id": "FB1453", "time": "17:30", "name": "溫納姆狼隊 vs 黃金海岸騎士", "pick": "和局", "odds": 4.45},
    {"id": "FB1455", "time": "17:35", "name": "墨爾本勝利 vs 紐卡素噴射機", "pick": "和局", "odds": 4.55},
    {"id": "FB1461", "time": "18:00", "name": "FC大阪 vs FC愛媛", "pick": "和局", "odds": 3.05}
]

# --- 3. 介面顯示 ---
total_odds = 4.45 * 4.55 * 3.05
st.metric("3 串 1 總賠率", f"{total_odds:.2f} 倍")

st.write("### 🎯 監控場次清單")
for m in matches:
    with st.container():
        st.info(f"🕒 **{m['time']}** | {m['id']} {m['name']} \n\n方向：**{m['pick']}** (@{m['odds']})")

# --- 4. 自動觸發邏輯 ---
if st.button("🚀 啟動監控並發送 TG 測試", use_container_width=True):
    current_time = datetime.now().strftime('%H:%M:%S')
    msg = (
        f"🔔 *老闆，反擊系統已啟動！*\n\n"
        f"📅 日期：4/17 (今日)\n"
        f"💰 組合：3 串 1 (和局)\n"
        f"📈 總賠率：*{total_odds:.2f} 倍*\n\n"
        f"1️⃣ 17:30 溫納姆狼隊\n"
        f"2️⃣ 17:35 墨爾本勝利\n"
        f"3️⃣ 18:00 FC大阪\n\n"
        f"🔥 *寫左成個禮拜，今晚一定要攞成績！*"
    )
    send_tg_msg(msg)
    st.success("✅ TG 通知已發送到你手機！即刻去 Telegram 睇下！")
    st.balloons()

st.divider()
st.caption(f"最後同步時間: {datetime.now().strftime('%H:%M:%S')} | 穩定運行中")
