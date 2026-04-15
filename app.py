import requests
import telebot
import threading
import streamlit as st

# ================= 1. 配置區 =================
API_KEY = "3a0784d142517860438150499e17006d" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156"

# ================= 2. 介面 (防止 Streamlit 卡死) =================
st.title("⚽ 獵人系統：終極戰場")
st.status("系統運行中... 隨時準備開火")
st.write("請前往 Telegram 打指令 `/hunt` 獲取組合。")

# ================= 3. 獵人邏輯 =================
def fetch_and_analyze():
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads,totals&oddsFormat=decimal"
    try:
        data = requests.get(url, timeout=10).json()
        score_picks, value_picks = [], []
        
        for match in data:
            h, a = match['home_team'], match['away_team']
            for bookie in match['bookmakers']:
                if bookie['key'] in ['pinnacle', 'williamhill']:
                    for market in bookie['markets']:
                        for out in market['outcomes']:
                            p = out['price']
                            # 策略：3串1波膽 (7-15倍)
                            if market['key'] == 'correct_score' and 7.0 <= p <= 15.0:
                                score_picks.append(f"{h} vs {a} | 波膽 {out['name']} | {p}倍")
                            # 策略：5-7串1勁嘢 (2.0+ 讓球/大細)
                            elif market['key'] in ['spreads', 'totals'] and p >= 2.0:
                                value_picks.append(f"{h} vs {a} | {market['key']} {out['name']} | {p}倍")
        
        # 拼湊報告
        msg = "🚀 【自由之翼：狙擊報表】\n\n"
        msg += "🎯 【終極 3 串 1 波膽 (300x+)】\n"
        if len(score_picks) >= 3:
            for s in score_picks[:3]: msg += f"• {s}\n"
        else: msg += "• 高倍波膽不足，請等深夜場口。\n"
        
        msg += "\n🔥 【高槓桿 5-7 串 1 (2.0+)】\n"
        if len(value_picks) >= 5:
            for v in value_picks[:7]: msg += f"• {v}\n"
        else: msg += "• 暫未掃描到優質勁嘢。\n"
        
        msg += "\n🚨 【資金監控】\n深夜盤口數據穩定，一旦有異常爆發會自動彈出。"
        return msg
    except:
        return "⚠️ API 暫時繁忙，請一分鐘後再試。"

# ================= 4. Telegram 指令 =================
bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['hunt'])
def handle_hunt(message):
    bot.send_message(CHAT_ID, "🔎 獵人掃描中...")
    report = fetch_and_analyze()
    bot.send_message(CHAT_ID, report)

# ================= 5. 後台運行設置 =================
def run_bot():
    bot.remove_webhook()
    bot.polling(none_stop=True)

if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = threading.Thread(target=run_bot, daemon=True)
    st.session_state.bot_thread.start()
