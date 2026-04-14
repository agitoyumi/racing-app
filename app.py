# -*- coding: utf-8 -*-

def reborn_engine():
    # ⚽ 今晚歐聯波膽劇本 (03:00)
    football = ["2:2", "3:2", "1:2"]

    # 🏇 聽日 3T 對標種子 (14:41 盤口)
    # 格式: (馬號, 舊賠率, 跑法)
    r5 = [(1, 7.0, "放頭"), (4, 3.4, "前領"), (10, 8.7, "中置")]
    r6 = [(3, 6.4, "前領"), (4, 15.0, "前領"), (9, 5.7, "放頭")]
    r7 = [(5, 4.2, "前領"), (6, 3.0, "前領"), (11, 14.0, "中置")]

    # 聽朝 10:00 AM 更新區 (手動改呢度)
    live = {
        1: 7.0, 4: 3.4, 10: 8.7, 
        3: 6.4, 4: 15.0, 9: 5.7, 
        5: 4.2, 6: 3.0, 11: 14.0
    }

    print("\n" + "!"*40)
    print("    SURVIVAL MISSION: REBORN")
    print("!"*40)
    
    print(f"【今晚波膽 3x1】: {' | '.join(football)}")
    print("-" * 40)

    # 執行對標
    for race, horses in [(5, r5), (6, r6), (7, r7)]:
        print(f"R{race} (3T 目標: 包辦三甲)")
        for no, old, pos in horses:
            now = live.get(no, old)
            bias = (now - old) / old * 100
            alert = " [!] 落飛" if bias <= -20 else ""
            # 簡潔輸出：馬號 | 跑法 | 變動%
            print(f"  #{no:<2} {pos:<4} | {old:>4.1f} -> {now:>4.1f} ({bias:>+5.1f}%) {alert}")
        print("-" * 40)

    print("指令: $10 單式 3T | 專注物理優勢")
    print("!"*40 + "\n")

if __name__ == "__main__":
    reborn_engine()
