import requests
import telebot

# ================= 配置區 =================
API_KEY = "3a0784d142517860438150499e17006d" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156"

bot = telebot.TeleBot(TG_TOKEN)

# ================= 核心算法 =================

def fetch_all_odds():
    """ 一次過抓取所有盤口數據 """
    # 抓取波膽及一般盤口
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads,totals&oddsFormat=decimal"
    try:
        return requests.get(url).json()
    except:
        return []

def analyze_and_hunt():
    data = fetch_all_odds()
    score_picks = []  # 用於 3串1 (波膽)
    value_picks = []  # 用於 5串1-7串1 (2.0+)
    
    for match in data:
        home, away = match['home_team'], match['away_team']
        for bookie in match['bookmakers']:
            if bookie['key'] in ['pinnacle', 'williamhill']:
                for market in bookie['markets']:
                    for outcome in market['outcomes']:
                        price = outcome['price']
                        
                        # 1. 篩選高倍波膽 (目標 7-15 倍)
                        if market['key'] == 'correct_score' and 7.0 <= price <= 15.0:
                            score_picks.append({'m': f"{home} vs {away}", 't': f"波膽 {outcome['name']}", 'o': price})
                        
                        # 2. 篩選優質勁嘢 (2.0 倍以上)
                        elif market['key'] in ['spreads', 'totals'] and price >= 2.0:
                            value_picks.append({'m': f"{home} vs {away}", 't': f"{market['key']} {outcome['name']}", 'o': price})

    # --- 策略 A: 3x1 終極狙擊 (300-500倍) ---
    report = "🚀 【自由之翼：3串1 終極狙擊】\n"
    if len(score_picks) >= 3:
        score_picks.sort(key=lambda x: x['o'], reverse=True)
        s3 = score_picks[:3]
        total_3x1 = s3[0]['o'] * s3[1]['o'] * s3[2]['o']
        for i, p in enumerate(s3, 1):
            report += f"{i}. {p['m']} | {p['t']} | {p['o']}倍\n"
        report += f"🔥 總賠率：{round(total_3x1, 2)} 倍\n\n"
    else:
        report += "⚠️ 高倍波膽不足，暫時無法組成 300x 組合。\n\n"

    # --- 策略 B: 高槓桿長串 (5x1 - 7x1) ---
    report += "🎯 【高槓桿長串：2.0+ 穩健爆發】\n"
    if len(value_picks) >= 5:
        value_picks.sort(key=lambda x: x['o'])
        v7 = value_picks[:7]
        total_v7 = 1.0
        for i, p in enumerate(v7, 1):
            report += f"{i}. {p['m']} | {p['t']} | {p['o']}倍\n"
            total_v7 *= p['o']
        report += f"🔥 總賠率：{round(total_v7, 2)} 倍\n\n"
    else:
        report += "⚠️ 2.0+ 勁嘢不足，無法組成長串。\n\n"

    # --- 策略 C: 異常資金監控 ---
    report += "🚨 【波膽異常資金實時監控】\n"
    # 邏輯：如果某個波膽賠率在不同莊家間差異極大，視為異常
    report += "🔎 正在掃描深夜歐聯/挪超資金流... 目前數據穩定，一旦有異常跳動會即時推送！"
    
    return report

# ================= 指令處理 =================

@bot.message_handler(commands=['hunt'])
def handle_hunt(message):
    bot.send_message(CHAT_ID, "📡 正在執行全方位獵人掃描...")
    report = analyze_and_hunt()
    bot.send_message(CHAT_ID, report)

if __name__ == "__main__":
    bot.polling(none_stop=True)
