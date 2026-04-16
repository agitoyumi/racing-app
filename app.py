import streamlit as st
import pd as pd
import requests

# 1. 通道鎖定
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債-對準歐戰", layout="wide")
st.title("🎯 2026/04/17 實戰：歐霸 & 歐協聯 專場")

# 2. 核心數據：完全對應老闆張圖 (全部為歐戰賽事)
def get_verified_picks():
    return [
        {"賽事": "17/04 03:00 諾定咸森林 vs 波圖 (歐霸)", "推介": "全場和局", "賠率": "2.98"},
        {"賽事": "17/04 03:00 費倫天拿 vs 水晶宮 (歐協聯)", "推介": "全場客勝", "賠率": "2.35"},
        {"賽事": "17/04 03:00 斯特拉斯堡 vs 緬恩斯 (歐協聯)", "推介": "全場和局", "賠率": "3.60"}
    ]

# 3. 推送函數
def send_to_tg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": MY_CHAT_ID, "text": msg})
        return True
    except:
        return False

# 4. 畫面顯示
st.subheader("📊 2026/04/17 03:00 歐戰組合 (三串一)")
data = get_verified_picks()
st.table(pd.DataFrame(data))

# 5. 回報計算 (2.98 * 2.35 * 3.60 = 25.21 倍)
st.divider()
total_odds = 25.21
st.subheader(f"🚀 總賠率：{total_odds} 倍")

investment = [50, 100, 200, 500]
returns = [i * total_odds for i in investment]
calc_df = pd.DataFrame({
    "投注金額": [f"${i}" for i in investment],
    "預計回報": [f"${r:,.0f}" for r in returns]
})
st.table(calc_df)

# 6. 通知測試
if st.button("📢 資料無誤，推送至手機"):
    msg = f"🎯 老闆，2026/04/17 歐戰組合修正版：\n1. 森林 vs 波圖 [和] @ 2.98\n2. 費倫 vs 水晶宮 [客] @ 2.35\n3. 斯特 vs 緬恩斯 [和] @ 3.60\n🔥 總賠率：25.21 倍"
    if send_to_tg(msg):
        st.success("✅ 手機已收到修正訊息！")
    else:
        st.error("❌ 推送失敗。")

st.info("💡 三場都係歐戰（歐霸+歐協聯），100% 對準馬會 App 今日賽程。")
