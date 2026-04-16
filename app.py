import streamlit as st
import pandas as pd
import requests

# 1. 指令傳送通道 (已確認)
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債-最後校準", layout="wide")
st.title("🏹 2026/04/17 凌晨 03:00：馬會實時對沖")

# 2. 根據截圖與實時數據：三場全和 (歐霸+歐協聯)
def get_final_data():
    return [
        {"賽事": "17/04 03:00 諾定咸森林 vs 波圖 (歐霸)", "推介": "全場和局", "賠率": "2.98"},
        {"賽事": "17/04 03:00 費倫天拿 vs 水晶宮 (歐協聯)", "推介": "全場和局", "賠率": "3.35"},
        {"賽事": "17/04 03:00 斯特拉斯堡 vs 緬恩斯 (歐協聯)", "推介": "全場和局", "賠率": "3.60"}
    ]

# 3. 推送函數
def send_to_tg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": MY_CHAT_ID, "text": msg})

# 4. 畫面顯示
st.subheader("📋 2026/04/17 實戰組合 (目標 35.9 倍)")
df = pd.DataFrame(get_final_data())
st.table(df)

# 5. 回報計算 (不畫大餅，只列事實)
total_odds = 2.98 * 3.35 * 3.60
st.info(f"當前 3 串 1 總賠率：{total_odds:.2f}")

if st.button("📢 將此組合推送至 TG 備份"):
    msg = f"🎯 2026/04/17 最終指令：\n1. 森林 vs 波圖 [和]\n2. 費倫 vs 水晶宮 [和]\n3. 斯特 vs 緬恩斯 [和]\n🔥 總倍率：{total_odds:.2f}"
    send_to_tg(msg)
    st.success("✅ 手機收到訊息即代表對焦成功。")

st.divider()
st.caption("老闆，呢份係我最後能做嘅校準。03:00 開波，天亮見結果。")
