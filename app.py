def get_data(race_no):
    # 這裡加入更強的模擬瀏覽器標頭
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
        'Referer': 'https://racing.hkjc.com/'
    }
    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 尋找所有表格，找出那個帶有馬匹編號的
        all_tables = soup.find_all('table')
        target_table = None
        for t in all_tables:
            if "馬名" in t.text and "負磅" in t.text:
                target_table = t
                break
        
        if not target_table:
            return pd.DataFrame()
        
        rows = target_table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            # 只要該行第一個字是純數字，就是馬匹數據
            if len(cols) >= 8:
                num = cols[0].get_text(strip=True)
                if num.isdigit():
                    # 抓取馬名 (通常在第 4 格) 和 負磅 (通常在第 6 格)
                    data.append({
                        "馬號": int(num),
                        "馬名": cols[3].get_text(strip=True),
                        "負磅": int(re.sub(r'\D', '', cols[5].get_text(strip=True))),
                        "檔位": int(cols[6].get_text(strip=True)) if cols[6].get_text(strip=True).isdigit() else 0
                    })
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()
