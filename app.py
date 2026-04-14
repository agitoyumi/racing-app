import pandas as pd
import numpy as np

class PredatorEngine:
    def __init__(self):
        # 載入你選定的 9 隻重生種子馬
        self.seeds = pd.DataFrame({
            'race': [5, 5, 5, 6, 6, 6, 7, 7, 7],
            'no': [1, 4, 10, 3, 4, 9, 5, 6, 11],
            'style': ['Lead', 'Forward', 'Mid', 'Forward', 'Forward', 'Lead', 'Forward', 'Forward', 'Mid'],
            'init_odds': [7.0, 3.4, 8.7, 6.4, 15.0, 5.7, 4.2, 3.0, 14.0]
        })

    def analyze_market_bias(self, current_odds_list):
        """
        對比 14:41 賠率與臨場賠率，找出異常資金流向
        """
        self.seeds['current_odds'] = current_odds_list
        # 計算偏差值：負數代表有人「落飛」
        self.seeds['bias'] = (self.seeds['current_odds'] - self.seeds['init_odds']) / self.seeds['init_odds']
        return self.seeds

    def pace_filter(self, pace_forecasts):
        """
        pace_forecasts: dict {race_no: 'Slow'/'Fast'}
        根據快活谷 A 欄物理特性加權
        """
        def calculate_weight(row):
            pace = pace_forecasts.get(row['race'], 'Normal')
            if pace == 'Slow':
                # 慢步速有利放頭 (Lead/Forward)
                return 1.2 if row['style'] in ['Lead', 'Forward'] else 0.8
            elif pace == 'Fast':
                # 快步速有利中後追 (Mid)
                return 1.2 if row['style'] == 'Mid' else 0.7
            return 1.0

        self.seeds['pace_weight'] = self.seeds.apply(calculate_weight, axis=1)
        return self.seeds

    def simulation_3t_precision(self):
        """
        模擬「包辦前三」的極限概率
        """
        # 假設基礎命中率 (基於 A 欄與騎師數據)
        base_prob = 0.25 
        # 三場都要「包辦前三」且三隻全中，難度係極致級
        total_prob = (base_prob ** 3) * 100
        print(f"--- 生存反擊戰模擬 ---")
        print(f"模組預測命中率: {total_prob:.4f}%")
        print(f"建議注碼: $10 (單式精確打擊)")
        print(f"目標彩池: $2,500,000 多寶")

    def execution_report(self):
        print("\n--- 聽朝 10:00 執行清單 ---")
        for race in [5, 6, 7]:
            horses = self.seeds[self.seeds['race'] == race]['no'].tolist()
            print(f"第 {race} 場: 鎖定馬匹 {horses} -> 目標: 包辦前三名")

# --- 實戰執行 ---
engine = PredatorEngine()

# 1. 模擬臨場賠率更新 (聽朝你需要輸入實際數據)
# 假設賠率變動不大
latest_odds = [6.5, 3.2, 9.0, 6.0, 14.5, 5.5, 4.0, 2.8, 15.0]
engine.analyze_market_bias(latest_odds)

# 2. 載入步速對標 (根據你張截圖：第 5 場慢、第 6 場快、第 7 場慢)
pace_data = {5: 'Slow', 6: 'Fast', 7: 'Slow'}
engine.pace_filter(pace_data)

# 3. 輸出報告
engine.simulation_3t_precision()
engine.execution_report()

# 4. 異常報警
anomalies = engine.seeds[engine.seeds['bias'] < -0.25]
if not anomalies.empty:
    print("\n⚠️ 警報：發現異常落飛馬匹！")
    print(anomalies[['race', 'no', 'bias']])
