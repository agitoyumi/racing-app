import tkinter as tk
from tkinter import ttk
import datetime

# 真正 4/17 的賽事數據 (根據你最新圖表)
def get_real_time_odds():
    return [
        {"time": "17:30", "id": "FB1453", "teams": "溫納姆狼隊 vs 黃金海岸騎士", "odds": "1:2 (8.25) / 0:2 (17.0)"},
        {"time": "17:35", "id": "FB1455", "teams": "墨爾本勝利 vs 紐卡素噴射機", "odds": "2:0 (13.0) / 2:1 (7.75)"},
        {"time": "18:00", "id": "FB1461", "teams": "FC大阪 vs FC愛媛", "odds": "1:0 (5.80) / 1:1 (6.20)"}
    ]

def update_dashboard():
    for i in tree.get_children():
        tree.delete(i)
    matches = get_real_time_odds()
    for m in matches:
        tree.insert("", "end", values=(m["time"], m["id"], m["teams"], m["odds"]))
    status_label.config(text=f"最後更新: {datetime.datetime.now().strftime('%H:%M:%S')} | 狀態: 盯死中 🎯")
    root.after(30000, update_dashboard) # 每30秒自動刷新一次

# 建立介面
root = tk.Tk()
root.title("老闆反擊戰 - 自動更新系統 v1.0")
root.geometry("700x400")
root.configure(bg="#1a1a1a") # 深色底色，唔傷眼

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=40)
style.map("Treeview", background=[('selected', '#0078d7')])

# 標題
title_label = tk.Label(root, text="今日 4/17 必收波膽反擊線", font=("Arial", 18, "bold"), fg="#00ff00", bg="#1a1a1a", pady=20)
title_label.pack()

# 表格
columns = ("時間", "編號", "對賽", "精選波膽賠率")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.pack(expand=True, fill="both", padx=10, pady=10)

# 狀態列
status_label = tk.Label(root, text="正在初始化...", fg="#aaaaaa", bg="#1a1a1a", pady=10)
status_label.pack()

# 啟動自動更新
update_dashboard()

root.mainloop()
