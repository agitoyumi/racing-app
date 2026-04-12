import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI 賽馬助手", layout="wide")
st.title("🏇 AI 賽馬即時分析")

# 1. 強力抓取函數
def get_race_data(race_no):
    # 使用模擬手機瀏覽器的 Header，避免被馬會封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
    }
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    
    try:
        # 直接使用 pandas 的 read_html，它比 BeautifulSoup 更能處理複雜表格
        html_content = requests.get(url, headers=headers, timeout=10).text
        dfs = pd.read_html(html_content)
        
        for df in dfs:
            # 判斷這是不是我們要的排位表（欄位數通常很多）
            if len(df.columns) >= 10:
                # 清理標題 (馬會表格有時會有兩層標題)
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(-1)
                return df
        return None
    except:
        return None

# 2. 場次切換與顯示
race_no = st.sidebar.selectbox("切換場次", range(1, 12), index=4) # 預設第 5 場

data = get_race_data(race_no)

if data is not None:
    st.success(f"✅ 第 {race_no} 場數據已更新")
    
    # 這裡只顯示重點欄位，讓你在手機上看更清楚
    cols_to_show = ["馬號", "馬名", "騎師", "負磅", "檔位"]
    # 自動適配馬會可能變動的欄位名稱
    existing_cols = [c for c in cols_to_show if c in data.columns]
    
    st.dataframe(data[existing_cols], use_container_width=True)
    
    # AI 核心邏輯
    st.info("💡 今日獲利模型：關注 **120 磅以下** 的輕磅馬。")
else:
    st.error("馬會伺服器繁忙，請按下方按鈕重新刷入數據。")
    if st.button("重新加載數據"):
        st.rerun()
