import streamlit as st
import pandas as pd
import requests
import re

st.set_page_config(page_title="AI 賽馬分析助手", layout="wide")

# --- 1. 動態數據抓取函數 ---
def fetch_any_race(race_no):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'}
    # 這裡的 URL 會根據 race_no 變化
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = 'utf-8'
        # 使用 pandas 的 read_html 自動掃描所有場次表格
        dfs = pd.read_html(r.text)
        for df in dfs:
            # 透過列名關鍵字（如：馬名、騎師）來鎖定正確的排位表
            if "馬名" in str(df.columns) or "騎師" in str(df.columns):
                return df
        return None
    except:
        return None

# --- 2. 側邊欄：切換場次 ---
st.sidebar.header("📊 場次選擇")
selected_race = st.sidebar.selectbox(
    "你想看哪一場？", 
    range(1, 12), 
    index=4  # 預設顯示第 5 場
)

st.title(f"🏇 第 {selected_race} 場 AI 即時分析")

# --- 3. 執行抓取與顯示 ---
race_df = fetch_any_race(selected_race)

if race_df is not None:
    st.success(f"✅ 已成功載入第 {selected_race} 場數據")
    
    # 清理數據 (將標題對齊)
    if isinstance(race_df.columns, pd.MultiIndex):
        race_df.columns = race_df.columns.get_level_values(-1)
    
    st.dataframe(race_df, use_container_width=True)
    
    # AI 提示區
    st.info(f"💡 AI 提醒：觀察第 {selected_race} 場中，負磅較輕且排內檔的冷門馬。")
else:
    st.warning(f"目前無法取得第 {selected_race} 場數據。可能原因：場次尚未受注或馬會網頁更新中。")
    if st.button("手動嘗試重新連線"):
        st.rerun()
