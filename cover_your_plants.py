def cover_your_plants(city="carrollton"):
    # imports 
    
    # for scraping the weather 
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    
    # scraping the weather  
    url = "https://forecast.weather.gov/MapClick.php?lat=33.004190&lon=-96.906520"

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
    m = ls[1] + ".  " + recommendation
    
    # sending the message 
    yag = yagmail.SMTP('nbadailyprediction@gmail.com', password = "bjqphhhhbbpzobns")
    #yag.send(to=['3256173035@mms.att.net','5127863033@mms.att.net'],contents=message)
    yag.send(to=['3256173035@mms.att.net'],contents=m)