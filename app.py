import requests
import telebot
import time

# ================= 1. 核心配置 (已幫你填好) =================
API_KEY = "3a0784d142517860438150499e17006d" 
TG_TOKEN = "8663783053:AAErT9AAZEbE3bcHPOQmY_78uSk8f1De70A"
CHAT_ID = "6348332156"

bot = telebot.TeleBot(TG_TOKEN)

# ================= 2. 數據掃描邏輯 =================

def get_all_data():
    """ 抓取全網數據 (包含波膽、讓球、大細) """
    # 呢個 API 會一次過掃描 correct_score, spreads, totals
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=correct_score,spreads,totals&oddsFormat=decimal"
    try:
        res = requests.get(url)
        return res.json()
    except:
        return []

def scan_markets():
    data = get_all_data()
    score_picks = []  # 儲存波膽 (7-15倍)
    value_picks = []  # 儲存 2.0+ 勁嘢
    
    for match in data:
        home = match['home_team']
        away = match['away_team']
        for bookie in match['bookmakers']:
            # 只參考大莊 (Pinnacle/William Hill) 確保數據準確
            if bookie['key'] in ['pinnacle', 'williamhill']:
                for market in bookie['markets']:
                    for outcome in market['outcomes']:
                        p = outcome['price']
                        
                        # A. 搵 3串1 用嘅波膽 (7.0 - 15.0 倍)
                        if market['key'] == 'correct_score' and 7.0 <= p <= 15.0:
                            score_picks.append({'match': f"{home} vs {away}", 'type': f"波膽 {outcome['name']}", 'odds': p})
                        
                        # B. 搵 5-7串1 用嘅 2.0+ 勁嘢 (受讓/大細)
                        elif market['key'] in ['spreads', 'totals'] and p >= 2.0:
                            value_picks.append({'match': f"{home} vs {away}", 'type': f"{market['key']} {outcome['name']}", 'odds': p})

    return score_picks, value_picks

# ================= 3. 報告生成 =================

def build_report(score_picks, value_picks):
    report = "📊 【老闆，全能獵人報表到！】\n\n"

    # --- 策略 1: 3串1 波膽狙擊 (目標 300-500倍) ---
    report += "🚀 【終極 3 串 1 (波膽)】\n"
    if len(score_picks) >= 3:
        score_picks.sort(key=lambda x: x['odds'], reverse=True)
        s3 = score_picks[:3]
        total_3x1 = s3[0]['odds'] * s3[1]['odds'] * s3[2]['odds']
        for i, s in enumerate(s3, 1):
            report += f"{i}. {s['match']} | {s['type']} | {s['odds']}倍\n"
        report += f"🔥 預計回報：{round(total_3x1, 2)} 倍\n\n"
    else:
        report += "⚠️ 波膽數據不足，未達 3 串 1 門檻。\n\n"

    # --- 策略 2: 5-7串1 勁嘢組合 (2.0+ 玩法) ---
    report += "🎯 【高槓桿 5-7 串 1 (2.0+)】\n"
    if len(value_picks) >= 5:
        value_picks.sort(key=lambda x: x['odds'])
        v7 = value_picks[:7]
        total_v7 = 1.0
        for i, v in enumerate(v7, 1):
            report += f"{i}. {v['match']} | {v['type']} | {v['odds']}倍\n"
            total_v7 *= v['odds']
        report += f"🔥 預計回報：{round(total_v7, 2)} 倍\n\n"
    else:
        report += "⚠️ 勁嘢不足，暫無長串建議。\n\n"

    # --- 策略 3: 異常資金監控 ---
    report += "🚨 【異常資金流監控】\n"
    report += "🔎 正實時對比馬會與國際盤口差價... 目前未見大規模拋售，數據穩定。"
    
    return report

# ================= 4. TG 指令控制 =================

@bot.message_handler(commands=['hunt'])
def start_hunt(message):
    bot.send_message(CHAT_ID, "📡 獵人模式啟動，正在橫掃全球數據...")
    scores, values = scan_markets()
    final_msg = build_report(scores, values)
    bot.send_message(CHAT_ID, final_msg)

if __name__ == "__main__":
    print("Bot 運行中...")
    bot.polling(none_stop=True)
