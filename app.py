def fetch_race_data(race_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
    }
    
    # 這是最穩定的排位表連結
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml') # 使用 lxml 提高解析速度
        
        # 尋找頁面上所有表格，通常排位表是最大的那個或帶有特定 ID
        tables = soup.find_all('table')
        target_table = None
        
        for t in tables:
            # 排位表通常包含 "騎師" 或 "負磅" 這些關鍵字
            if "騎師" in t.text and "負磅" in t.text:
                target_table = t
                break
        
        if not target_table:
            return None
            
        rows = target_table.find_all('tr')
        horse_list = []
        
        for row in rows:
            cells = row.find_all('td')
            # 確保這行有足夠的格數 (馬會排位表通常超過 10 格)
            if len(cells) >= 10:
                num = cells[0].get_text(strip=True)
                # 只有當第一格是數字時才是馬匹數據
                if num.isdigit():
                    name = cells[3].get_text(strip=True)
                    jockey = cells[4].get_text(strip=True)
                    weight = cells[5].get_text(strip=True)
                    draw = cells[6].get_text(strip=True)
                    
                    horse_list.append({
                        "馬號": int(num),
                        "馬名": name,
                        "騎師": jockey,
                        "負磅": int(re.sub(r'\D', '', weight)) if weight else 0,
                        "檔位": int(draw) if draw.isdigit() else 0
                    })
        
        return pd.DataFrame(horse_list)
    except Exception as e:
        # 在開發階段，把具體錯誤印出來能幫我們更快解決問題
        st.error(f"偵測到問題: {str(e)}")
        return None
