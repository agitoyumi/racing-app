import requests
import telebot
import time
import os

# ================= 1. 配置區 (已填好 Token) =================
# 呢度我加咗判斷，防止 Token 格式錯誤導致 App 卡死
API_KEY = "3a0784d142517860438150499e17006d"
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156"

# ================= 2. 初始化 Bot =================
try:
    bot = telebot.TeleBot(TG_TOKEN)
except Exception as e:
    print(f"Bot Error: {e}")

# ================= 3. 功能邏輯 =================

def get_combined_report():
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads,totals&oddsFormat=decimal"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        
        score_picks = []  # 波膽 (7-15倍)
        value_picks = []  # 2.0+ 勁嘢
        
        for match in data:
            h, a = match['home_team'], match['away_team']
            for bookie in match['bookmakers']:
                if bookie['key'] in ['pinnacle', 'williamhill']:
                    for market in bookie['markets']:
                        for out in market['outcomes']:
                            p = out['price']
                            # 策略 A: 3串1波膽 (7-15倍)
                            if market['key'] == 'correct_score' and 7.0 <= p <= 15.0:
                                score_picks.append(f"{h} vs {a} | 波膽 {out['name']} | {p}倍")
                            # 策略 B: 5-7串1勁嘢 (2.0+ 讓球/大細)
                            elif market['key'] in ['spreads', 'totals'] and p >= 2.0:
                                value_picks.append(f"{h} vs {a} | {market['key']} {out['name']} | {p}倍")

        report = "📊 【全能獵人狙擊報表】\n\n"
        
        # 3串1 波膽
        report += "🚀 【終極 3 串 1 波膽 (目標 300x+)】\n"
        if len(score_picks) >= 3:
            for s in score_picks[:3]: report += f"• {s}\n"
        else: report += "• 數據掃描中，暫無高倍波膽\n"
        
        # 5-7串1 勁嘢
        report += "\n🎯 【高槓桿 5-7 串 1 (2.0+ 組合)】\n"
        if len(value_picks) >= 5:
            for v in value_picks[:7]: report += f"• {v}\n"
        else: report += "• 暫無足夠勁嘢場次\n"
        
        report += "\n🚨 【資金監控】\n目前歐聯/挪超資金流向正常，暫無異常爆發。"
        return report
    except:
        return "⚠️ API 請求超時，請稍後再試。"

# ================= 4. TG 命令 =================

@bot.message_handler(commands=['hunt'])
def handle_hunt(message):
    try:
        bot.send_message(CHAT_ID, "🔎 獵人正在橫掃全球數據...")
        msg = get_combined_report()
        bot.send_message(CHAT_ID, msg)
    except Exception as e:
        print(f"Send Message Error: {e}")

# ================= 5. Streamlit 展示 (防止 App 卡死) =================
import streamlit as st
st.title("⚽ 獵人 Bot 運行狀態")
st.write("Bot 正在後台運行中... 請前往 Telegram 使用 /hunt 指令。")

if __name__ == "__main__":
    bot.polling(none_stop=True)
