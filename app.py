import datetime

# --- 核心修正：唔用 pytz，直接用 timedelta 處理香港時間 (UTC+8) ---
def get_clean_real_money_data(raw_data):
    """
    1. 徹底殺掉 4.15 殘留過期數據
    2. 只准輸出『未來』且『有志氣』的場次
    """
    # 獲取 UTC 時間並轉為香港時間
    utc_now = datetime.datetime.utcnow()
    hk_now = utc_now + datetime.timedelta(hours=8)
    
    clean_list = []
    
    for match in raw_data:
        try:
            # 強制轉換賽事時間
            match_time = datetime.datetime.fromisoformat(match['start_time'])
            
            # 修正：如果賽事已經開始或過期，直接剔除
            if match_time <= hk_now:
                continue
                
            # 修正：志氣過濾器 (只選賠率 > 2.0 的 Value Bet)
            if float(match['odds']) >= 2.0:
                match['status'] = "🔥 實質翻身核武"
                clean_list.append(match)
        except Exception:
            continue
            
    # 按賠率價值排序
    clean_list.sort(key=lambda x: x['odds'], reverse=True)
    return clean_list

def generate_boss_report(refined_data):
    if not refined_data:
        return "⚠️ 目前無高勝算場次，系統監控中..."
    
    report = "🚨 【修正版：真錢翻身報告】 🚨\n"
    report += "--------------------------------------\n"
    
    for m in refined_data[:3]:
        report += f"賽事：{m['home']} vs {m['away']}\n"
        report += f"目標：{m['pick']} | 賠率：{m['odds']}\n"
        report += "--------------------------------------\n"
    
    return report
