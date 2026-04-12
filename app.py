def fetch_future_races(race_no):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'}
    
    # 策略：如果賠率頁面沒數據，就抓「排位表」
    # 排位表 URL (包含馬名、負磅、檔位、騎師)
    url_card = f"https://racing.hkjc.com/racing/information/Chinese/Racing/RaceCard.aspx?RaceNo={race_no}"
    
    try:
        r = requests.get(url_card, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        horse_data = []
        
        # 針對排位表表格進行抓取
        table = soup.find('table', {'class': 'is-tm'}) # 馬會排位表特有的 class
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 5:
                    num = cells[0].get_text(strip=True) # 馬號
                    name = cells[3].get_text(strip=True) # 馬名
                    weight = cells[5].get_text(strip=True) # 負磅
                    draw = cells[6].get_text(strip=True) # 檔位
                    
                    if num.isdigit():
                        horse_data.append({
                            "馬號": num,
                            "馬名": name,
                            "負磅": weight,
                            "檔位": draw
                        })
        
        if not horse_data:
            return pd.DataFrame()
            
        df = pd.DataFrame(horse_data).drop_duplicates()
        return ai_analyze_logic(df)
    except Exception as e:
        st.error(f"連線至排位表失敗: {e}")
        return pd.DataFrame()
