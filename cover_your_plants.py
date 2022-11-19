def cover_your_plants(city="carrollton"):
    # imports 
    
    # for scraping the weather 
    from bs4 import BeautifulSoup
    import requests
    # for sending the text 
    import yagmail
    
    # scraping the weather 
    
    # create url
    url = "https://www.google.com/search?q="+"weather"+city
    # requests instance
    html = requests.get(url).content
    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    # getting the temperature 
    # get the temperature
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    # this contains time and sky description
    string = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    # format the data
    data = string.split('\n')
    time = data[0]
    sky = data[1]
    # list having all div tags having particular class name
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    # particular list with required data
    strd = listdiv[5].text
    # formatting the string
    pos1 = strd.find('Wind')
    other_data = strd[pos1:]
    hilo = strd[strd.find('High'):strd.find('Wind')-3]
    
    # setting the recommendation
    low = int(hilo[-3:-1])
    if low <=32:
        recommendation = "Cover the plants!"
    elif low >32:
        recommendation = "No need to cover the plants tonight."
    else:
        recommendation = "Something is wrong! Check your code!"
    
    # formatting the message 
    message = "Current Temperature is {}. Current Time: {}. Sky Description: {}. {}. {}. {}".format(temp,time,sky,other_data,hilo,recommendation)
    
    # sending the message 
    yag = yagmail.SMTP('nbadailyprediction@gmail.com', password = "bjqphhhhbbpzobns")
    yag.send(to=['3256173035@mms.att.net','5127863033@mms.att.net'],contents=message)

cover_your_plants()

