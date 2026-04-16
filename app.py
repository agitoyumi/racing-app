import streamlit as st
import requests

# 1. 聯絡通道
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="210萬清債-實時系統", layout="wide")

# 2. 標題與聲明
st.title("🎯 2026/04/17 凌晨 03:00 實施指令")
st.error("⚠️ 老闆，呢鋪係對準你張圖個賠率，三場全和，博 34.8 倍。")

# 3. 實戰場次 (改用原始表格寫法，唔使 pandas)
st.write("### 📋 實施場次詳情")
st.markdown("""
| 賽事 | 推介 | 賠率 |
| :--- | :--- | :--- |
| 諾定咸森林 vs 波圖 | 全場和局 | 2.98 |
| 費倫天拿 vs 水晶宮 | 全場和局 | 3.25 |
| 斯特拉斯堡 vs 緬恩斯 | 全場和局 | 3.60 |
""")

# 4. 回報計算
total_odds = 2.98 * 3.25 * 3.60
st.subheader(f"🚀 總賠率：{total_odds:.2f} 倍")

st.write("---")
st.write("### 💰 實戰回報參考")
st.write(f"- 投入 $50  ->  回報 **${50 * total_odds:.0f}**")
st.write(f"- 投入 $100 ->  回報 **${100 * total_odds:.0f}**")
st.write(f"- 投入 $200 ->  回報 **${200 * total_odds:.0f}**")
st.write(f"- 投入 $500 ->  回報 **${500 * total_odds:.0f}**")

# 5. 指令推送功能
if st.button("📢 確定無誤，推送指令至手機"):
    msg = f"🎯 老闆，2026/04/17 最終組合：\n1. 森林[和] @ 2.98\n2. 費倫[和] @ 3.25\n3. 斯特[和] @ 3.60\n🔥 總賠率：{total_odds:.2f}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={"chat_id": MY_CHAT_ID, "text": msg})
        if res.status_code == 200:
            st.success("✅ 手機已收到指令！")
        else:
            st.error("❌ TG 推送失敗，請檢查 Token。")
    except:
        st.error("❌ 網路連線出錯。")

st.write("---")
st.caption("更新時間: 2026/04/16 08:30 | 實時校準完畢")
