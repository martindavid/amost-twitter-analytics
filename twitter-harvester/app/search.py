from __future__ import print_function
import tweepy
import logging
from pprint import pprint
from datetime import datetime
from time import sleep
from app.db import DB, Keyword, TwitterToken
from app.tweet_store import TweetStore
import settings

MAX_COUNT = 100

class TwitterSearch(object):
    """Main class to handle harvesting twitter data

    Args:
        group_name: group name used to filter the keyword

    Attributes:
        api: tweepy.API object
        keyword_list: list of keyword object from Keyword class
        tw_store = TweetStore instance (manage data access to couchdb)
    """

    def __init__(self, group_name):

        database = DB(settings.PG_DB_USER, settings.PG_DB_PASSWORD, settings.PG_DB_NAME)
        database.connect()

        keyword = Keyword(database.con, database.meta)
        token = TwitterToken(database.con, database.meta)

        """Set tweepy api object and authentication"""
        token = token.find_by_group(group_name)
        auth = tweepy.OAuthHandler(token["consumer_key"], token["consumer_secret"])
        auth.set_access_token(token["access_token"], token["access_token_secret"])

        self.api = tweepy.API(auth)
        self.keyword_list = keyword.find_by_group(group_name)
        self.tw_store = TweetStore('tweets', settings.COUCHDB_SERVER)

    def execute(self):
        """Execute the twitter crawler, loop into the keyword_list"""
        for keyword in self.keyword_list:
            logging.info('Crawl data for %s' % keyword["keyword"])
            self.crawl(keyword)

    def crawl(self, keyword):
        """ Crawl individual keyword """
        api = self.api
        max_id = -1
        count = 1
        tweets = api.search(q=keyword["keyword"], include_entities=True, \
                                lang="en", count=MAX_COUNT)
        for tweet in tweets:
            if count == MAX_COUNT:
                max_id = tweet.id

            self.tw_store.save_tweet(tweet)

            count = count + 1
            self.test_rate_limit(api)

        while True:
            count = 1
            cursor = api.search(q=keyword["keyword"], include_entities=True, \
                            lang="en", count=MAX_COUNT, max_id=max_id-1)
            for tweet in cursor:
                if count == MAX_COUNT:
                    max_id = tweet.id
                self.tw_store.save_tweet(tweet)

                count = count + 1
            self.test_rate_limit(api)


    def test_rate_limit(self, api, wait=True, buffer=.1):
        """
        Tests whether the rate limit of the last request has been reached.
        :param api: The `tweepy` api instance.
        :param wait: A flag indicating whether to wait for the rate limit reset
                    if the rate limit has been reached.
        :param buffer: A buffer time in seconds that is added on to the waiting
                    time as an extra safety margin.
        :return: True if it is ok to proceed with the next request. False otherwise.
        """
        #Get the number of remaining requests
        remaining = int(api.last_response.headers['x-rate-limit-remaining'])
        #Check if we have reached the limit
        if remaining == 0:
            limit = int(api.last_response.headers['x-rate-limit-limit'])
            reset = int(api.last_response.headers['x-rate-limit-reset'])
            #Parse the UTC time
            reset = datetime.fromtimestamp(reset)
            #Let the user know we have reached the rate limit
            print("0 of {} requests remaining until {}.".format(limit, reset))

            if wait:
                #Determine the delay and sleep
                delay = (reset - datetime.now()).total_seconds() + buffer
                print("Sleeping for {}s...".format(delay))
                sleep(delay)
                #We have waited for the rate limit reset. OK to proceed.
                return True
            else:
                #We have reached the rate limit. The user needs to handle the rate limit manually.
                return False

        #We have not reached the rate limit
        return True

