# personal-finance
Application to demonstrate the use of an external API, Bootstrap CSS, Jinja templates, pagination and integration with RSS feeds

This is still a work in progress
## To-Do list
* Add a Mongo or Redis backend and allow the user to modify the cofniguration of the portfolio, ie ticker symbol and number of shares
* Read the RSS only once an hour and expire the data. Within that period don't read the news again. At moment it is read many times because of pagination and that makes it less responsive
```
import redis
from time import sleep
r = redis.Redis(host='127.0.0.1', port='6379') 
r.set('a', "Hi there")
r.expire('a', 10)
sleep(2)
print "TTL is : " + str(r.ttl('a'))
```
* Improve overall appearance by exploiting better the capabilities of Bootstrap CSS
* General tidying up of the code
