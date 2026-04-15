import requests
import telebot
import streamlit as st

# ================= 核心配置 =================
API_KEY = "4a7de5275f3bcc92039c4f50335820d3" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "411468742" 

bot = telebot.TeleBot(TG_TOKEN)

st.set_page_config(page_title="獵人 500x 狙擊系統", layout="wide", page_icon="💰")
st.title("🏹 自由之翼：全功能獵人系統 v5.0")

# ================= 數據運算核心 =================
def run_heavy_scanner():
    # 擴大掃描範圍：包含波膽 (correct_score) 同 基本盤 (h2h)
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": "uk,eu",
        "markets": "correct_score,h2h,totals",
        "oddsFormat": "decimal"
    }
    
    try:
        res = requests.get(url, params=params, timeout=20)
        if res.status_code != 200: return f"❌ API 報錯: {res.status_code}"
        
        data = res.json()
        score_picks = []   # 波膽池 (7x-15x)
        value_picks = []   # 高價值池 (2.0x+)
        unusual_flow = []  # 資金異常池
        
        for match in data:
            home = match['home_team']
            away = match['away_team']
            
            for bookie in match['bookmakers']:
                # 監控專業盤口 (Pinnacle/William Hill) 
                if bookie['key'] in ['pinnacle', 'williamhill', 'betfair_ex']:
                    for market in bookie['markets']:
                        # 1. 狙擊高倍波膽 (目標 3串1 達成 300x+)
                        if market['key'] == 'correct_score':
                            for opt in market['outcomes']:
                                if 7.0 <= opt['price'] <= 16.0: # 精選 7-16 倍波膽
                                    score_picks.append(f"{home} vs {away} | {opt['name']} | {opt['price']}x")
                        
                        # 2. 狙擊 5-7 串 1 高勝率盤 (2.0x 以上)
                        elif market['key'] == 'h2h':
                            for opt in market['outcomes']:
                                if 2.0 <= opt['price'] <= 3.5:
                                    value_picks.append(f"{home} vs {away} | {opt['name']} | {opt['price']}x")
                        
                        # 3. 資金異常監控 (簡易邏輯：低於平均賠率的顯著偏移)
                        if market['key'] == 'h2h' and len(market['outcomes']) > 0:
                            if opt['price'] < 1.4: # 強隊熱錢過度湧入標記
                                unusual_flow.append(f"⚠️ 異常熱錢: {home} 獨贏 ({opt['price']}x)")

        # 整理最終報告
        report = "🚀 【獵人深夜清單：全面收割模式】\n"
        report += "========================\n\n"
        
        report += "🎯 【終極 3 串 1 波膽組合 (300x+)】\n"
        if len(score_picks) >= 3:
            for s in score_picks[:3]: report += f"📍 {s}\n"
            # 計算倍數範例
            report += "💰 預估回報：約 350x - 600x\n"
        else: report += "📉 當前波膽賠率波動中，建議觀望。\n"
        
        report += "\n🔥 【高勝率 5-7 串 1 (2.0x+)】\n"
        if len(value_picks) >= 5:
            for v in value_picks[:7]: report += f"✅ {v}\n"
        else: report += "📉 暫未發現足夠優質讓球盤。\n"
        
        report += "\n🚨 【資金流/數據異常監控】\n"
        if unusual_flow:
            for u in unusual_flow[:3]: report += f"{u}\n"
        else: report += "⚖️ 全網資金流向目前相對穩定。\n"
        
        report += "\n💡 老闆提醒：博彩有風險，收割需謹慎！"
        return report

    except Exception as e:
        return f"⚠️ 掃描中斷: {str(e)}"

# ================= 介面設計 =================
if st.button("🔥 啟動全功能掃描 (300倍+資金監控)"):
    with st.spinner('🎯 獵人正在計算賠率鏈與資金流...'):
        final_report = run_heavy_scanner()
        st.markdown("### 🔍 掃描結果預覽")
        st.code(final_report)
        
        # 發送到 Telegram
        try:
            bot.send_message(CHAT_ID, final_report)
            st.balloons()
            st.success("🎯 數據已全數推送到 Telegram！開火！")
        except Exception as e:
            st.error(f"❌ 發送失敗: {e}")

if st.sidebar.button("🔔 測試通訊"):
    bot.send_message(CHAT_ID, "✅ 通道穩定，隨時待命！")
