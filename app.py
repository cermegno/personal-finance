import os
from flask import Flask, render_template, flash
import feedparser
import math
import requests
import json
import locale

locale.setlocale( locale.LC_ALL, '' )

portfolio = [
    {
        'e' : 'ASX',
        't' : 'TLS',
        'n' : 1000
    },
    {
        'e' : 'ASX',
        't' : 'CBA',
        'n' : 150
    },
        {
        'e' : 'ASX',
        't' : 'ANZ',
        'n' : 110
    }
]

app = Flask(__name__)
app.secret_key = 'random string'

user = ""

@app.route('/')
@app.route('/<user>')
def index(user=None):

    total = 0
    stocks = {}  # Use a dictionary and do "for s in stocks"
    
    for i in range(0,len(portfolio)):
        tkr = portfolio[i]['t']
        num = portfolio[i]['n']
        exc = portfolio[i]['e']
        url = "https://www.google.com/finance/info?client=ig&q=" + exc + ":" + tkr
        response = requests.get(url)
        response = str(response.content).replace('\n','').replace('[','').replace(']','').strip('/').strip()
        obj = json.loads(response)
        ## Add the share price to the json 
        portfolio[i]['p'] = obj['l']
        price = float(obj['l'])
        value = float(num) * float(price)
        total += value
        #print "Stock : " + tkr + "\tNumber of shares : " + str(num) + "\t= $" + str(value)

    total = locale.currency( total, grouping=True )
    print "Total value of your holdings ............ $" + str(total)

    return render_template('portfolio.html',
                           stocks=portfolio,
                           total=total)

@app.route('/news/')
@app.route('/news/page/<int:page>')
def news(page=1):
    results = []
    links = []
    feed_url="http://www.abc.net.au/news/feed/51892/rss.xml"
    feed = feedparser.parse(feed_url)
    RSSitems = feed["items"]
    for item in RSSitems:
        category = item['category']
        if category == "Business, Economics and Finance":
            headlines = item['title']
            link = item['link']
            #print headlines
            #print link
            results.append(headlines)
            links.append(link.encode('ascii'))
            
    #print links
    npp = 5 # We will show 5 News Per Page
    top = (page * npp)
    bottom = top - npp
    maxpage = int(math.ceil(float(len(results)) / float(npp)))
    print "List length is :" + str(len(results))
    #print "Max page is : " + str(maxpage)
    #print "Top = " + str(top) + ", Bottom = " + str(bottom)
    results = results[bottom:top]
    links = links[bottom:top]
    #print results
    return render_template('news.html',
                           news=results,
                           links=links,
                           page=page,
                           maxpage=maxpage)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
