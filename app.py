import streamlit as st

# 在建議區域下方加入打賞模組
st.divider()
st.subheader("🧧 貼中咗？支持一下開發！")

col_pay1, col_pay2 = st.columns(2)

with col_pay1:
    st.image("你的PayMe_QR_Code.png", caption="PayMe 支持")
    st.button("複製轉數快 (FPS) ID")

with col_pay2:
    st.markdown("""
    **打賞清單：**
    * ☕️ 請飲咖啡 ($40)
    * 🍱 豐富午餐 ($100)
    * 🎰 研發基金 (自由金額)
    """)
