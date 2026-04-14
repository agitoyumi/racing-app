# -*- coding: utf-8 -*-

def run_predator_system():
    # --- 14:41 原始對標數據 (你的重生種子) ---
    seeds = [
        {"race": 5, "no": 1, "name": "一起美麗", "old": 7.0, "pos": "放頭", "pace": "慢"},
        {"race": 5, "no": 4, "name": "做好自己", "old": 3.4, "pos": "前領", "pace": "慢"},
        {"race": 5, "no": 10, "name": "知道穩勝", "old": 8.7, "pos": "中置", "pace": "慢"},
        
        {"race": 6, "no": 3, "name": "勇霸龍", "old": 6.4, "pos": "前領", "pace": "快"},
        {"race": 6, "no": 4, "name": "天天友福", "old": 15.0, "pos": "前領", "pace": "快"},
        {"race": 6, "no": 9, "name": "快樂神駒", "old": 5.7, "pos": "放頭", "pace": "快"},
        
        {"race": 7, "no": 5, "name": "彩虹七色", "old": 4.2, "pos": "前領", "pace": "慢"},
        {"race": 7, "no": 6, "name": "星運少爵", "old": 3.0, "pos": "前領", "pace": "慢"},
        {"race": 7, "no": 11, "name": "環球英雄", "old": 14.0, "pos": "中置", "pace": "慢"}
    ]

    # --- 聽朝 10:00 AM 手動輸入最新賠率 ---
    # 請根據馬會 App 即時更新以下數值
    new_odds = {
        1: 7.0, 4: 3.4, 10: 8.7,   # 第 5 場
        3: 6.4, 4: 15.0, 9: 5.7,   # 第 6 場
        5: 4.2, 6: 3.0, 11: 14.0   # 第 7 場
    }

    print("\n" + "="*50)
    print("      掠食者系統：3T 精確對標報告 (自用版)")
    print("="*50)
    print(f"{'場次':<4} {'馬號':<4} {'馬名':<10} {'偏差%':<8} {'狀態'}")
    print("-" * 50)

    for s in seeds:
        now = new_odds.get(s['no'], s['old'])
        # 計算賠率變動百分比
        diff = ((now - s['old']) / s['old']) * 100
        
        # 判定異常狀態
        status = "穩定"
        if diff <= -20: 
            status = "⚠️ 落飛 (大戶介入)"
        elif diff >= 20: 
            status = "⚖️ 冷落 (被市場忽視)"
            
        # 物理邏輯檢核
        logic_check = ""
        if s['pace'] == "慢" and s['pos'] in ["放頭", "前領"]:
            logic_check = " [有利]"

        print(f"R{s['race']:<3} {s['no']:<4} {s['name']:<10} {diff:>6.1f}%    {status}{logic_check}")

    print("-" * 50)
    print(">>> 執行指令：")
    print("1. 確保每一場 3 隻馬全部跑入前三名 (單式 $10)")
    print("2. 排除情緒干擾，專注物理數據偏差")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_predator_system()
