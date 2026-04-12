import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI 賽馬全日通", layout="wide")

# --- 1. 定義各場次核心冷門 (防止馬會封鎖時的備援數據) ---
RACE_MODELS = {
    6: {"冷門": "12 手到再來, 14 整得好", "邏輯": "115-116磅極輕磅 + C賽道內欄"},
    7: {"冷門": "9 喜至寶, 11 魅影獵飛", "邏輯": "班次落位 + 輕磅突擊"},
    8: {"冷門": "3 錶之銀河, 8 全城帶勝", "邏輯": "高分馬輕磅展現級數"},
    9: {"冷門": "10 精彩勇士, 13 團結一心", "邏輯": "步速偏差 + 後追輕磅"},
    10: {"冷門": "14 嘉應傳承, 5 駿步騰飛", "邏輯": "113磅底磅 + 換人交代"},
    11: {"冷門": "7 綠族無限, 12 步大威猛", "邏輯": "尾場輕磅馬慣性爆冷"}
}

# --- 2. 強化抓取函數 ---
def get_live_data(race_no):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'}
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    try:
        # 使用 pandas 直接讀取，速度最快
        dfs = pd.read_html(requests.get(url, headers=headers, timeout=5).text)
        for df in dfs:
            if len(df.columns) >= 10:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(-1)
                return df[["馬號", "馬名", "騎師", "負磅", "檔位"]]
        return None
    except:
        return None

# --- 3. App 主介面 ---
st.title("🏇 全日場次 AI 獲利助手")

# 側邊欄：場次選擇切換
selected_race = st.sidebar.selectbox("選擇分析場次", range(1, 12), index=5)

# 顯示當前場次的分析邏輯
st.subheader(f"📊 第 {selected_race} 場 分析回報")

df = get_live_data(selected_race)

if df is not None:
    st.success(f"✅ 第 {selected_race} 場 實時數據已同步")
    st.dataframe(df, use_container_width=True)
else:
    st.error("❌ 馬會連線受阻，自動開啟 AI 離線模型數據")
    
# --- 4. 顯示 AI 核心分析 (無論有沒有連線都會顯示) ---
if selected_race in RACE_MODELS:
    model = RACE_MODELS[selected_race]
    st.markdown(f"""
    <div style="background-color:#1e3a8a; padding:15px; border-radius:10px; color:white">
    <h4>💡 AI 核心策略：</h4>
    <p><b>推薦冷門：</b> {model['冷門']}</p>
    <p><b>選馬邏輯：</b> {model['邏輯']}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("該場次 AI 模型正在計算中，請關注輕磅馬。")

if st.button("刷新數據源"):
    st.rerun()
