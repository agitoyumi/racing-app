# --- 戰時數據手冊 (直接複製，保證唔會黑) ---

# ⚽ 今晚歐聯 (03:00) 
# 波膽 3x1 過關：[ 2:2 / 3:2 / 1:2 ]

# 🏇 聽日 3T 單式 (每場三隻全入三甲)
# 格式: (馬號, 14:41賠率)

# --- 聽朝 10:00 AM 手動填入即時賠率對標 ---
r5_data = { 1: 7.0, 4: 3.4, 10: 8.7 }
r6_data = { 3: 6.4, 4: 15.0, 9: 5.7 }
r7_data = { 5: 4.2, 6: 3.0, 11: 14.0 }

print("="*30)
print("  PREDATOR CHECKLIST  ")
print("="*30)

def check(race, data, original):
    print(f"R{race}:")
    for no, old in original.items():
        now = data[no]
        bias = (now - old) / old * 100
        alert = " [!] 落飛" if bias <= -20 else ""
        print(f" #{no:<2} | {old:>4.1f} -> {now:>4.1f} ({bias:>+5.1f}%) {alert}")

# 14:41 原始數據對標
check(5, r5_data, {1: 7.0, 4: 3.4, 10: 8.7})
check(6, r6_data, {3: 6.4, 4: 15.0, 9: 5.7})
check(7, r7_data, {5: 4.2, 6: 3.0, 11: 14.0})
print("="*30)
