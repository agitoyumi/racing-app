import requests
import telebot
import streamlit as st

# 1. 基礎配置
API_KEY = "3a0784d142517860438150499e17006d"
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156"

# 2. 顯示網頁內容 (確保 Streamlit 唔會卡死)
st.title("⚽ 獵人系統：最後衝刺")
st.write("如果見到呢行字，代表網頁正常行緊。")
st.write("請喺 Telegram 試吓打 /hunt")

# 3. 初始化 Bot
bot = telebot.TeleBot(TG_TOKEN)

# 4. 數據獲取邏輯
def fetch_data():
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads,totals&oddsFormat=decimal"
    try:
        data = requests.get(url, timeout=10).json()
        report = "🚀 【自由之翼：狙擊報表】\n"
        # 簡化邏輯，先確保能出數據
        for match in data[:5]: # 只攞頭5場做測試
            report += f"• {match['home_team']} vs {match['away_team']}\n"
        report += "\n✅ 掃描成功，隨時準備開火！"
        return report
    except:
        return "⚠️ API 暫時攞唔到數據"

# 5. 指令處理
@bot.message_handler(commands=['start', 'hunt'])
def send_welcome(message):
    bot.reply_to(message, "🔎 收到指令！獵人正在掃描...")
    msg = fetch_data()
    bot.send_message(CHAT_ID, msg)

# 6. 強制啟動 (呢兩行最重要，唔好漏！)
if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
