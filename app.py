import streamlit as st
import requests

# 1. 唯一聯絡通道 (你的 TG)
BOT_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
MY_CHAT_ID = "411468742"

st.set_page_config(page_title="今晚必須見錢")

st.title("🎯 4月17日 03:00 找數組合")

# 2. 完全對準你張圖，不再甩轆
st.markdown("""
### 📊 鎖定目標 (3 串 1)
- **諾定咸森林 vs 波圖** -> 【和局】@ 2.98
- **費倫天拿 vs 水晶宮** -> 【和局】@ 3.25
- **斯特拉斯堡 vs 緬恩斯** -> 【和局】@ 3.60

### 🚀 預計倍數：34.8 倍
""")

# 3. 推送指令到 TG (確保你買嗰陣有紀錄對準場次)
if st.button("📢 確定今晚場次，推送指令到手機"):
    text = "🎯 今晚 03:00 絕地找數指令：\n1. 森林 vs 波圖 [和] 2.98\n2. 費倫 vs 水晶宮 [和] 3.25\n3. 斯特 vs 緬恩斯 [和] 3.60\n🔥 總倍率：34.8"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={MY_CHAT_ID}&text={text}"
    
    try:
        res = requests.get(url)
        if res.status_code == 200:
            st.success("✅ 手機收到！今晚 03:00，就係呢三場。")
        else:
            st.error("❌ 推送失敗，請檢查網路。")
    except:
        st.error("❌ 連線出錯。")

st.write("---")
st.write("💰 $100 -> $3,480 | $200 -> $6,960")
