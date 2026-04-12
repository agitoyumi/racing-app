import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

st.title("🏇 AI 賽馬即時分析")

def fetch_data(race_no):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        # 尋找排位表表格
        table = soup.find('table', {'class': 'is-tm'})
        rows = table.find_all('tr')
        horses = []
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 10 and tds[0].text.strip().isdigit():
                horses.append({
                    "馬號": tds[0].text.strip(),
                    "馬名": tds[3].text.strip(),
                    "負磅": tds[5].text.strip(),
                    "檔位": tds[6].text.strip()
                })
        return pd.DataFrame(horses)
    except:
        return None

race_no = st.sidebar.selectbox("選擇場次", range(1, 12), index=4)
data = fetch_data(race_no)

if data is not None and not data.empty:
    st.write(f"### 第 {race_no} 場 排位數據")
    st.table(data) # 使用最穩定的 table 格式，不使用 dataframe
    st.info("💡 邏輯提醒：關注負磅 120 以下的馬匹。")
else:
    st.error("正在嘗試連線馬會伺服器，請按下方按鈕刷新。")
    if st.button("手動刷新"):
        st.rerun()
