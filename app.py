import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# 1. 頁面基礎配置
st.set_page_config(page_title="精準賽馬 AI", layout="wide")

# 2. 爬蟲函數
def get_data(race_no):
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', {'class': 'is-tm'})
        
        rows = table.find_all('tr')
        data = []
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 10:
                num = cols[0].text.strip()
                if num.isdigit():
                    data.append({
                        "馬號": int(num),
                        "馬名": cols[3].text.strip(),
                        "負磅": int(re.sub(r'\D', '', cols[5].text.strip())),
                        "檔位": int(cols[6].text.strip()) if cols[6].text.strip().isdigit() else 0
                    })
        return pd.DataFrame(data)
    except:
        return pd.DataFrame() # 失敗回傳空表

# 3. 介面與邏輯
st.title("🏇 精準 AI 賽馬助手")

race_no = st.sidebar.selectbox("選擇場次", range(1, 12), index=4)

df = get_data(race_no)

if not df.empty:
    # AI 評分邏輯
    df['AI 評分'] = df.apply(lambda x: (2 if x['負磅'] <= 120 else 0) + (1 if x['檔位'] <= 4 else 0), axis=1)
    st.dataframe(df.sort_values("AI 評分", ascending=False), use_container_width=True)
    
    # 獲利提醒
    top_pick = df.sort_values("AI 評分", ascending=False).iloc[0]
    st.success(f"🔥 AI 推薦：{top_pick['馬號']} 號 {top_pick['馬名']} (輕磅優勢)")
else:
    st.error("馬會數據讀取中或暫時無法連線... 請確認場次或稍後重試。")
    # 這裡是防黑屏的保險：顯示按鈕手動刷新
    if st.button("手動重新加載數據"):
        st.rerun()
