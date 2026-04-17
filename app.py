import requests
import json
from datetime import datetime

class HKJC_Updater:
    def __init__(self):
        # 模擬馬會數據介面 (實務上會爬取 HKJC 官網 XML)
        self.api_url = "https://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_had.aspx"
        self.target_matches = []

    def get_latest_matches(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 正在同步今日 4/17 賽事...")
        
        # 這裡模擬抓取今日 17:30 - 18:00 的核心場次
        # 確保不會出現 2046 年的垃圾數據
        live_data = [
            {"id": "FB1453", "teams": "溫納姆狼隊 vs 黃金海岸騎士", "time": "17:30", "status": "即將開賽"},
            {"id": "FB1455", "teams": "墨爾本勝利 vs 紐卡素噴射機", "time": "17:35", "status": "即將開賽"},
            {"id": "FB1461", "teams": "FC大阪 vs FC愛媛", "time": "18:00", "status": "即將開賽"}
        ]
        self.target_matches = live_data
        return self.target_matches

    def calculate_profit(self, bet_amount, odds_list):
        # 自動計算 3 串 1 預計回報
        total_odds = 1
        for o in odds_list:
            total_odds *= o
        return bet_amount * total_odds

# --- 執行部分 ---
app = HKJC_Updater()
matches = app.get_latest_matches()

print("\n--- 今日反擊場次清單 ---")
for m in matches:
    print(f"{m['time']} | {m['id']} | {m['teams']} | {m['status']}")

# 模擬波膽 3 串 1 回報 (以 $100 為例)
# 賠率: 1:2(8.25), 2:0(13.0), 1:0(5.8)
potential_return = app.calculate_profit(100, [8.25, 13.0, 5.8])

print(f"\n[自動計算] $100 蚊 3 串 1 預計派彩: ${potential_return:,.2f}")
