from __future__ import print_function
import json
import time
import tweepy
from tweepy.streaming import StreamListener
from app.logger import LOGGER as log
from app.db import DB, Keyword, TwitterToken
from app.tweet_store import TweetStore
from app.sentiment_analysis import SentimentAnalysis
import settings

# Get the box coordinates from http://boundingbox.klokantech.com/
AUS_GEO_CODE = [113.03, -39.06, 154.73, -12.28]

class TwitterStream(StreamListener):
    """A listener class that will listen twitter streaming data"""

    def __init__(self, tw_store):
        self.tw_store = tw_store

    def on_data(self, data):
        """ Method to passes data from statuses to the on_status method"""
        if 'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            log.warning(warning['message'])
            return False

    def on_status(self, status):
        """ Handle logic when the data coming """
        try:
            tweet = json.loads(status)
            # Update sentiment score
            tweet["sentiment"] = SentimentAnalysis.get_sentiment(tweet_text=tweet["text"])
            self.tw_store.save_tweet(tweet)
        except Exception as e:
            log.error(e)

    def on_error(self, status):
        """ Handle any error throws from stream API """
        if status == 420:
            self.on_timeout()

    def on_timeout(self):
        """ Handle time out when API reach its limit """
        log.info("API Reach its limit, sleep for 10 minutes")
        time.sleep(600)
        return


class TwitterStreamRunner(object):
    """ Main class to run twitter stream listener

    Args:
        group_name: a group that used to fetch a list of keyword
    """

    def __init__(self, group_name):
        database = DB(settings.PG_DB_USER,
                      settings.PG_DB_PASSWORD, settings.PG_DB_NAME)
        database.connect()

        keyword = Keyword(database.con, database.meta)
        token = TwitterToken(database.con, database.meta)

        # Set tweepy api object and authentication
        token = token.find_by_group(group_name)
        self.auth = tweepy.OAuthHandler(
            token["consumer_key"], token["consumer_secret"])
        self.auth.set_access_token(token["access_token"], token["access_token_secret"])

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        keyword_list = keyword.find_by_group(group_name)
        # Construct keywords array from keyword_list dict
        self.keywords = [keyword["keyword"] for keyword in keyword_list]

        self.tw_store = TweetStore(settings.COUCHDB_DB, settings.COUCHDB_SERVER)

    def execute(self):
        """Execute the twitter crawler, loop into the keyword_list
        """
        listen = TwitterStream(self.tw_store)
        stream = tweepy.Stream(self.auth, listen)
        loop = True
        while loop:
            try:
                log.info("Start stream tweets data")
                stream.filter(locations=AUS_GEO_CODE)
                loop = False
                log.info("End stream tweets data")
            except Exception as e:
                log.error("There's an error, sleep for 10 minutes")
                log.error(e)
                loop = True
                stream.disconnect()
                time.sleep(600)
                continue
