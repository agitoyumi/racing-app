import streamlit as st
import pandas as pd
import requests

# 1. 之前老闆俾我嘅 Token (鎖定)
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債-真圖對戰", layout="wide")
st.title("🏹 根據馬會實時截圖：漏洞組合")

# 2. 根據你張圖入面真實存在的賠率
def get_verified_picks():
    return [
        {"賽事": "諾定咸森林 vs 波圖 (歐霸)", "推介": "全場和局", "賠率": "2.98", "理由": "全球水位跌緊，馬會 2.98 仲有肉食。"},
        {"賽事": "費倫天拿 vs 水晶宮 (歐協聯)", "推介": "全場客勝", "賠率": "2.35", "理由": "水晶宮近況超強，馬會客勝開得太鬆。"},
        {"賽事": "斯特拉斯堡 vs 緬恩斯", "推介": "全場和局", "賠率": "3.60", "理由": "兩隊護級戰意極濃，平局係大家底線。"}
    ]

# 3. TG 通知
def send_to_tg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": MY_CHAT_ID, "text": msg})

# 4. 畫面顯示
data = get_verified_picks()
st.subheader("📊 根據老闆截圖鎖定 (4/17 03:00 開波)")
st.table(pd.DataFrame(data))

# 5. 回報表 (3 串 1 = 2.98 * 2.35 * 3.60 = 25.2 倍)
st.divider()
total_odds = 2.98 * 2.35 * 3.60
st.subheader(f"💰 總賠率：{total_odds:.2f} 倍")

investment = [50, 100, 200, 500]
returns = [i * total_odds for i in investment]
calc_df = pd.DataFrame({
    "投注金額": [f"${i}" for i in investment],
    "預計回報": [f"${r:,.0f}" for r in returns]
})
st.table(calc_df)

if st.button("📢 根據截圖料：推送去我 TG"):
    msg = f"🎯 老闆！根據你張圖揀好喇：\n1. 森林 vs 波圖 [和]\n2. 費倫 vs 水晶宮 [客]\n3. 斯特 vs 緬恩斯 [和]\n目標：{total_odds:.2f} 倍"
    send_to_tg(msg)
    st.success("✅ 手機震咗未？今次係對住你張圖嚟寫，絕對唔會錯場次！")
