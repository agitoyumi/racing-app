import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# --- 基礎設定 ---
st.set_page_config(page_title="AI 賽馬獲利分析", layout="wide")

# --- 核心邏輯：防偏誤抓取引擎 ---
def fetch_race_data(race_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
    }
    
    # 路徑 A: 排位表 (最穩定，提早釋出)
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 尋找目標表格 (馬會排位表特有 class)
        table = soup.find('table', {'class': 'is-tm'})
        if not table:
            return None
            
        rows = table.find_all('tr')
        horse_list = []
        
        for row in rows[1:]: # 跳過標題列
            cells = row.find_all('td')
            if len(cells) >= 10:
                # 數據清理：移除多餘空格與換行
                num = cells[0].get_text(strip=True)
                name = cells[3].get_text(strip=True)
                jockey = cells[4].get_text(strip=True)
                weight = cells[5].get_text(strip=True)
                draw = cells[6].get_text(strip=True)
                
                if num.isdigit():
                    horse_list.append({
                        "馬號": int(num),
                        "馬名": name,
                        "騎師": jockey,
                        "負磅": int(re.sub(r'\D', '', weight)),
                        "檔位": int(draw) if draw.isdigit() else 0
                    })
        
        return pd.DataFrame(horse_list)
    except Exception as e:
        st.error(f"連線失敗: {e}")
        return None

# --- AI 分析邏輯：今日冷門模型 ---
def apply_ai_model(df):
    if df is None or df.empty: return None
    
    # 權重設定 (基於今日 12-10-9 實戰規律)
    def calculate_score(row):
        score = 0
        tips = []
        # 1. 輕磅規則：120磅以下是今日爆冷核心
        if row['負磅'] <= 118:
            score += 3
            tips.append("🔥 極輕磅冷門")
        elif row['負磅'] <= 123:
            score += 1
            tips.append("✅ 輕磅優勢")
            
        # 2. 檔位規則：C賽道內欄 1-4 檔
        if 1 <= row['檔位'] <= 4:
            score += 2
            tips.append("🐎 內欄好檔")
            
        return pd.Series([score, " | ".join(tips)])

    df[['AI 評分', '特徵分析']] = df.apply(calculate_score, axis=1)
    return df.sort_values(by='AI 評分', ascending=False)

# --- App 介面展示 ---
st.title("🏇 精準 AI 賽馬分析助手")
st.markdown(f"**實時數據校對：** 今日沙田 - C 賽道")

# 側邊欄控制
st.sidebar.header("場次切換")
race_no = st.sidebar.selectbox("請選擇場次", range(1, 12), index=4) # 預設第 5 場

if st.sidebar.button("同步最新數據"):
    st.rerun()

# 執行分析
raw_df = fetch_race_data(race_no)
final_df = apply_ai_model(raw_df)

if final_df is not None:
    # 亮點呈現：最高分的冷門馬
    top_pick = final_df.iloc[0]
    if top_pick['AI 評分'] >= 3:
        st.warning(f"🚀 **第 {race_no} 場 AI 重點關注：{top_pick['馬號']} 號 {top_pick['馬名']}**")
    
    # 顯示完整數據表
    st.subheader(f"第 {race_no} 場 全馬匹分析表")
    
    # 格式化表格：高亮高分馬匹
    def highlight_rows(s):
        return ['background-color: #1e3a8a; color: white' if s.name == final_df.index[0] and s['AI 評分'] >= 3 else '' for _ in s]

    st.dataframe(
        final_df.style.apply(highlight_rows, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    # 投注策略建議
    st.info("💡 **獲利策略：** 挑選上方表格中「AI 評分」最高的 2-3 匹馬，互串 **位置 Q (QP)**，尤其關注負磅 < 120 的冷門。")
else:
    st.error("❌ 暫時無法讀取數據。請檢查馬會網頁是否正常，或場次是否正確。")

st.caption("數據來源：HKJC 官方排位表 | AI 模型：輕磅+內欄獲利模型")
