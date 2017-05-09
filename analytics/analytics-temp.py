import datetime
import couchdb
from app.logger import LOGGER as log
from app.tweet_analytics import TweetAnalytics

server = couchdb.Server(url='http://127.0.0.1:15984/')
db = server['tweets']

# get twitter-hashtags couchdb instance
try:
    hashtags = server.create["twitter-hashtags"]
except:
    hashtags = server["twitter-hashtags"]

# get twitter-words couchdb instance
try:
    words = server.create["twitter-words"]
except:
    words = server["twitter-words"]

#get twitter-users couchdb instance
try:
    user = server.create["twitter-users"]
except:
    user = server["twitter-users"]

date_list = []
for row in db.view('_design/analytics/_view/conversation-date-breakdown', reduce=True, group=True):
    date_list.append(row.key)

today = datetime.date.today()
today = today.strftime('%Y/%-m/%-d')

for date in date_list:
    if date != today:
        # fetch data for individual date
        log.info("START - Process data for %s" % date)
        view_data = []
        for row in db.view('_design/analytics/_view/tweets-victoria', startkey=date, endkey=date):
            view_data.append(row.value)

        analytics = TweetAnalytics(date, view_data, db, hashtags, words, user)
        analytics.process_data()
        log.info("END - Process data for %s" % date)
