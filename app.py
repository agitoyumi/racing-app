from flask import Flask, render_template, request

app = Flask(__name__)

# 模擬數據結構：包含賽馬與足球的對標模組
dashboard_data = {
    "racing": {
        "title": "跑馬地夜馬 - 隔夜數據對標 (4/15)",
        "matches": [
            {
                "race_no": 1,
                "horses": [
                    {"no": "1", "name": "核心心水", "win_p": "0.0", "pla_p": "0.0", "status": "待更新"},
                    {"no": "5", "name": "副心水", "win_p": "0.0", "pla_p": "0.0", "status": "待更新"},
                    {"no": "9", "name": "冷門伏兵", "win_p": "0.0", "pla_p": "0.0", "status": "待更新"}
                ],
                "combinations": {"q": "0.0", "qp": "0.0"}
            }
        ]
    },
    "football": {
        "title": "歐聯重生方案 - 波膽監控",
        "games": [
            {"match": "利物浦 vs PSG", "type": "波膽", "target": "1:2", "odds": "8.00", "trend": "穩定"},
            {"match": "馬體會 vs 巴塞", "type": "波膽", "target": "2:1", "odds": "11.50", "trend": "向上"},
            {"match": "高車士打 vs 阿克寧頓", "type": "波膽", "target": "2:0", "odds": "6.90", "trend": "穩定"}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', data=dashboard_data)

if __name__ == '__main__':
    app.run(debug=True)
