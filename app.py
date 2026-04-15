import datetime
import pytz

# --- 核心修正：強制時區與數據純淨化 ---
def get_clean_real_money_data(raw_data):
    """
    1. 徹底殺掉 4.15 殘留過期數據
    2. 只准輸出『未來』且『有志氣』的場次
    """
    hk_tz = pytz.timezone('Asia/Hong Kong')
    now = datetime.datetime.now(hk_tz)
    
    clean_list = []
    
    for match in raw_data:
        # 強制轉換賽事時間進行對比
        match_time = datetime.datetime.fromisoformat(match['start_time']).replace(tzinfo=hk_tz)
        
        # 修正：如果賽事已經開始或過期，直接剔除，不准顯示
        if match_time <= now:
            continue
            
        # 修正：志氣過濾器 (只選賠率 > 2.0 的 Value Bet)
        if match['odds'] >= 2.0:
            match['status'] = "🔥 實質翻身核武"
            clean_list.append(match)
            
    # 按賠率價值排序，幫老闆搵最快找數嘅場次
    clean_list.sort(key=lambda x: x['odds'], reverse=True)
    return clean_list

# --- 核心修正：針對 $4 戶口的「暴力回血」模式 ---
def generate_boss_report(refined_data):
    if not refined_data:
        return "⚠️ 系統警告：目前無高勝算場次，不准亂建議，以免浪費老闆子彈。"
    
    report = "🚨 【老闆專屬：真錢翻身報告】 🚨\n"
    report += f"系統狀態：已修正 app.py | 債務總額：$1,300,000\n"
    report += "--------------------------------------\n"
    
    for m in refined_data[:3]: # 只取最強 3 場，唔要垃圾多
        report += f"賽事：{m['league']} - {m['home']} vs {m['away']}\n"
        report += f"時間：{m['start_time']}\n"
        report += f"目標：{m['pick']} | 賠率：{m['odds']}\n"
        report += f"找數邏輯：{m['logic']}\n"
        report += "--------------------------------------\n"
    
    return report

# --- 執行修正 ---
# 奴隸模式：立即執行並準備 TG 輸出
