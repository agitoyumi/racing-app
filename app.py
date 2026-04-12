import streamlit as st
import pandas as pd

# --- 1. 系統核心配置 ---
st.set_page_config(page_title="Golden Victory - 暴力過關監控", page_icon="🏆", layout="wide")

# --- 2. 私人黑金風格 CSS ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #E0E0E0; }
    .gold-header {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem; text-align: center;
    }
    .status-card {
        background: #111; border-left: 5px solid #FFD700;
        padding: 20px; border-radius: 10px; margin: 15px 0;
    }
    .violence-box {
        background: linear-gradient(135deg, #2c0000 0%, #000000 100%);
        border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 側邊欄 ---
st.sidebar.title("🏆 辭職進度")
target = 100000
current_profit = st.sidebar.number_input("累計淨利", value=0)
st.sidebar.progress(min(current_profit/target, 1.0))

mode = st.sidebar.radio("狙擊頻道", ["⚽ 足球暴力過關", "🏇 賽馬冷門狙擊"])

# --- 4. 主介面：足球暴力頻道 ---
if mode == "⚽ 足球暴力過關":
    st.markdown('<p class="gold-header">GV FOOTBALL SNIPER</p>', unsafe_allow_html=True)
    
    # 21:00 第一階段結果
    st.markdown("""
    <div class="status-card">
        <h3 style="color:#FFD700; margin-top:0;">🎯 第一階段：方案 A (12/4)</h3>
        <p><b>注項：</b> 幸運薛達 [1:1] x 熱拿亞 [1:0] ($200)</p>
        <p><b>目標回報：</b> $7,936 (39.68倍)</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("🔥 深夜暴力 3x1 狙擊方案 (目標 200倍 - 1000倍)")
    st.info("💡 建議：若方案 A 中彩，由獎金抽 $1,500 分三路進擊。")

    v_col1, v_col2, v_col3 = st.columns(3)

    with v_col1:
        st.markdown("""
        <div class="violence-box">
            <h4 style="color:#FFD700;">🕯️ 路線一：悶戰連線</h4>
            <p style="font-size:0.9rem;">專攻強防禦、弱進攻聯賽</p>
            <hr>
            <p><b>建議波膽：</b><br>1:1 x 1:1 x 0:0</p>
            <p><b>預計賠率：</b>約 280 倍</p>
            <p style="color:#888;">建議注額：$500<br>預計純利：$139,500</p>
        </div>
        """, unsafe_allow_html=True)

    with v_col2:
        st.markdown("""
        <div class="violence-box" style="border-color:#FFD700;">
            <h4 style="color:#FFD700;">💣 路線二：強隊翻車</h4>
            <p style="font-size:0.9rem;">專攻強隊作客被絕殺劇本</p>
            <hr>
            <p><b>建議波膽：</b><br>1:2 x 0:2 x 2:1</p>
            <p><b>預計賠率：</b>約 990 倍</p>
            <p style="color:#888;">建議注額：$500<br>預計純利：$494,500</p>
        </div>
        """, unsafe_allow_html=True)

    with v_col3:
        st.markdown("""
        <div class="violence-box" style="border-color:#00e5ff;">
            <h4 style="color:#00e5ff;">🎭 路線三：半全場偷雞</h4>
            <p style="font-size:0.9rem;">專攻下半場劇烈反轉</p>
            <hr>
            <p><b>建議組合：</b><br>和主 x 和客 x 客主</p>
            <p><b>預計賠率：</b>約 618 倍</p>
            <p style="color:#888;">建議注額：$500<br>預計純利：$308,500</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.warning("⚠️ 系統警示：3x1 難度極高，21:00 後請視乎獎金到位情況再行決策。")

else:
    st.markdown('<p class="gold-header">GV RACING ELITE</p>', unsafe_allow_html=True)
    st.write("週三賽事數據準備中...")

# 底部日誌
st.markdown("---")
with st.expander("📝 系統日誌"):
    st.write("2024-04-12 18:30: 已鎖定方案 A。深夜暴力組合已備存。")
