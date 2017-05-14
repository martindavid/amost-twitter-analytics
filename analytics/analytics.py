import datetime
import couchdb
from app.logger import LOGGER as log
from app.tweet_analytics import TweetAnalytics
from app.db import DB, AnalyticsLog
import settings

database = DB(settings.PG_DB_USER,
              settings.PG_DB_PASSWORD, settings.PG_DB_NAME)
database.connect()

server = couchdb.Server(url=settings.COUCHDB_SERVER)
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

# get twitter-users couchdb instance
try:
    user = server.create["twitter-users"]
except:
    user = server["twitter-users"]

log.info("START - Processing analytics data")

analytic_db = AnalyticsLog(database.con, database.meta)
date_list = analytic_db.fetch_unprocessed_data()

# fetch data for individual date
for date_for_analysis in date_list:
    log.info("START - Process data for %s", date_for_analysis)
    view_data = []

    for row in db.view('_design/analytics/_view/tweets-victoria',\
                         startkey=date_for_analysis, endkey=date_for_analysis):
        view_data.append(row.value)

    log.info("Processing %d row of data", len(view_data))

    analytics = TweetAnalytics(
        date_for_analysis, view_data, db, hashtags, words, user)
    analytics.process_data()
    analytic_db.update_timestamp_data(date_for_analysis)
    log.info("END - Process data for %s", date_for_analysis)

log.info("END - Processing analytics data")