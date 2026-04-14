# -*- coding: utf-8 -*-
"""
Predator 3T Precision System - Survival Edition
用於對標 14:41 原始數據與臨場賠率偏差
"""

def predator_app():
    # 1. 核心對標數據 (基於你的截圖)
    seeds = [
        {"r": 5, "n": 1, "name": "一起美麗", "old": 7.0, "pos": "Lead", "pace": "Slow"},
        {"r": 5, "n": 4, "name": "做好自己", "old": 3.4, "pos": "Fwd", "pace": "Slow"},
        {"r": 5, "n": 10, "name": "知道穩勝", "old": 8.7, "pos": "Mid", "pace": "Slow"},
        
        {"r": 6, "n": 3, "name": "勇霸龍", "old": 6.4, "pos": "Fwd", "pace": "Fast"},
        {"r": 6, "n": 4, "name": "天天友福", "old": 15.0, "pos": "Fwd", "pace": "Fast"},
        {"r": 6, "n": 9, "name": "快樂神駒", "old": 5.7, "pos": "Lead", "pace": "Fast"},
        
        {"r": 7, "n": 5, "name": "彩虹七色", "old": 4.2, "pos": "Fwd", "pace": "Slow"},
        {"r": 7, "n": 6, "name": "星運少爵", "old": 3.0, "pos": "Fwd", "pace": "Slow"},
        {"r": 7, "n": 11, "name": "環球英雄", "old": 14.0, "pos": "Mid", "pace": "Slow"}
    ]

    # 2. 聽朝 10:00 AM 更新區 (手動填入即時賠率)
    # 格式 -> 馬號: 賠率
    live_odds = {
        1: 7.0, 4: 3.4, 10: 8.7, 
        3: 6.4, 4: 15.0, 9: 5.7, 
        5: 4.2, 6: 3.0, 11: 14.0
    }

    print("\n" + "="*60)
    print("      PREDATOR SYSTEM: 3T PRECISION CALIBRATION")
    print("="*60)
    print(f"{'R':<3} {'No':<3} {'Horse':<10} {'14:41':<8} {'Live':<8} {'Bias%':<10} {'Logic'}")
    print("-" * 60)

    for s in seeds:
        now = live_odds.get(s['n'], s['old'])
        bias = ((now - s['old']) / s['old'] * 100)
        
        # 狀態判定
        indicator = "STABLE"
        if bias <= -25: indicator = "⚠️ ALERT (Drop)"
        elif bias >= 25: indicator = "COLD"

        # 物理優勢判定 (慢步速+前置)
        advantage = "PASS"
        if s['pace'] == "Slow" and s['pos'] in ["Lead", "Fwd"]:
            advantage = "★ ADV (Pace)"

        print(f"R{s['r']:<2} {s['n']:<3} {s['name']:<10} {s['old']:<8} {now:<8} {bias:>+6.1f}%    {advantage}")

    print("-" * 60)
    print("EXECUTION: [Single Ticket $10] - All 3 horses top 3 in each race.")
    print("="*60 + "\n")

if __name__ == "__main__":
    predator_app()
