import requests
import telebot
import math

# --- 基礎配置 (保持你原本的 Token) ---
API_KEY = "你的_ODDS_API_KEY"
TG_TOKEN = "你的_TELEGRAM_BOT_TOKEN"
CHAT_ID = "你的_TELEGRAM_CHAT_ID"

bot = telebot.TeleBot(TG_TOKEN)

# --- 戰略配置 ---
MIN_SINGLE_ODDS = 2.0      # 每場最低 2.0 倍，確保成本效益
TARGET_TOTAL_ODDS = 300.0  # 目標總賠率（300-500倍）

def fetch_premium_picks():
    """ 掃描符合「勁嘢」標準的盤口 """
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=uk,eu&markets=spreads,totals&oddsFormat=decimal"
    try:
        response = requests.get(url).json()
        picks = []
        for match in response:
            home = match['home_team']
            away = match['away_team']
            for bookie in match['bookmakers']:
                if bookie['key'] in ['pinnacle', 'betfair_ex', 'williamhill']:
                    for market in bookie['markets']:
                        for outcome in market['outcomes']:
                            # 只取賠率 >= 2.0 的單場
                            if outcome['price'] >= MIN_SINGLE_ODDS:
                                picks.append({
                                    'match': f"{home} vs {away}",
                                    'type': f"{market['key']} ({outcome['name']} {outcome.get('point', '')})",
                                    'odds': outcome['price']
                                })
        return picks
    except:
        return []

def build_mega_parlay(picks):
    """ 自動組合成 300倍-500倍 嘅長串 """
    if len(picks) < 5:
        return "⚠️ 目前符合 2.0+ 條件嘅場次不足，無法組成高槓桿長串。"

    # 按照賠率由低到高排，先取相對穩的 2.0+
    picks.sort(key=lambda x: x['odds'])
    
    selected = []
    current_total_odds = 1.0
    
    for p in picks:
        selected.append(p)
        current_total_odds *= p['odds']
        # 當達到目標倍數 (如 300倍) 就停止，或者最多取 8 場 (8串1)
        if current_total_odds >= TARGET_TOTAL_ODDS or len(selected) >= 8:
            break

    if current_total_odds < 100:
        return f"⚠️ 目前掃描到嘅最高組合僅 {round(current_total_odds, 2)} 倍，未達 300 倍門檻，建議再等等。"

    msg = f"🚩 【絕殺 300x+ 自由長串】\n"
    msg += "--------------------------\n"
    for i, s in enumerate(selected, 1):
        msg += f"{i}. {s['match']}\n   👉 {s['type']} | {s['odds']}倍\n"
    
    msg += "--------------------------\n"
    msg += f"🔥 總賠率：{round(current_total_odds, 2)} 倍\n"
    msg += f"💰 投注 $100 預計收回：${round(100 * current_total_odds, 2)}\n"
    msg += "📢 「呢張飛，就係你聽日唔使返工嘅理由。」"
    return msg

@bot.message_handler(commands=['hunt'])
def run_mega_hunt(message):
    bot.send_message(CHAT_ID, "🚀 正在掃描全網「勁嘢」，目標：300倍-500倍終極長串...")
    picks = fetch_premium_picks()
    report = build_mega_parlay(picks)
    bot.send_message(CHAT_ID, report)

if __name__ == "__main__":
    bot.polling(none_stop=True)
