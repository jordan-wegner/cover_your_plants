def cover_your_plants():
    # imports 
    
    # for scraping the weather 
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    
    # for sending the email 
    import yagmail 
    
    # for today's date 
    from datetime import datetime 
    
    # scraping the weather  
    url = "https://forecast.weather.gov/MapClick.php?lat=33.004190&lon=-96.906520"
    
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for f in soup.select("li.forecast-tombstone"):
        print(f.select_one(".period-name").get_text(strip=True, separator=" "))
        print(f.select_one(".short-desc").get_text(strip=True, separator=" "))
        print(f.select_one(".temp").text)
        print("-" * 80)

    tls = []
    for f in soup.select("li.forecast-tombstone"):
        a = f.select_one(".period-name").get_text(strip=True, separator=" ")
        b = f.select_one(".short-desc").get_text(strip=True, separator=" ")
        c = f.select_one(".temp").text
        tl = [a,b,c]
        tls.append(tl)
    TL1 = pd.DataFrame(tls)
    TL = TL1.copy()
    TL.columns = ['Time','DESCR','TEMP']
    tl_temp_splits = TL['TEMP'].str.split(': ')
    hl = [i[0] for i in tl_temp_splits]
    t = [i[1] for i in tl_temp_splits]
    TL['HIGH_LOW'] = hl
    TL['DEG'] = t
    TL['DEG_INT'] = [int(i.split(" ")[0]) for i in t]
    night_low = TL[(TL['Time']=='Tonight')&(TL['HIGH_LOW']=='Low')]['DEG_INT'].values[0]
    
    if night_low <=32:
        recommendation = "Cover the plants!"
    elif night_low >32:
        recommendation = "No need to cover the plants tonight."
    else:
        recommendation = "Something is wrong! Check your code!"
    
    # formatting the message 
    ls = []
    for i in range(0,len(TL1)):
        x = TL1.iloc[i,:].values[0]
        y = TL1.iloc[i,:].values[1]
        z = TL1.iloc[i,:].values[2]
        l1 = "{} will be {} with {}".format(x,y,z)
        ls.append(l1)
    m_all = '\n'.join(ls)
    
    # writing everything to log 
    td = datetime.today().strftime('%Y%m%d')
    file_id = "{}_weather_report.txt".format(td)
    with open(file=file_id,mode='w') as f: 
        f.write(m_all)
    
    # sending the message 
    yag = yagmail.SMTP('nbadailyprediction@gmail.com', password = "bjqphhhhbbpzobns")
    yag.send(to=['3256173035@mms.att.net','5127863033@mms.att.net'],contents=recommendation,attachments=file_id)
    #yag.send(to=['3256173035@mms.att.net'],contents=recommendation,attachments=file_id)
    
cover_your_plants()