import streamlit as st

st.set_page_config(page_title="今日賽馬即時看板", layout="wide")

st.title("🏇 官方即時排位表 (第 6-11 場)")

# 使用側邊欄提示今日邏輯
st.sidebar.header("🎯 AI 獲利邏輯")
st.sidebar.info("今日 C 賽道重點：關注負磅 120 磅以下的馬匹，尤其是排在 1-4 檔的冷門馬。")

# 選擇場次
race_no = st.selectbox("切換場次查看", range(1, 12), index=5)

# 這裡是馬會官方排位表的連結
hkjc_url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"

st.markdown(f"**正在查看第 {race_no} 場次**")

# 核心：使用 iframe 直接嵌入官網頁面，解決數據錯誤與連線封鎖問題
st.components.v1.iframe(hkjc_url, height=800, scrolling=True)

st.warning("💡 提示：如果上方表格載入較慢，請直接向下滾動查看完整馬匹名單。")
