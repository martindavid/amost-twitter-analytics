#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime
from time import sleep
import tweepy
from app.db import DB, Keyword, TwitterToken
from app.tweet_store import TweetStore
from app.logger import LOGGER as log
from app.sentiment_analysis import SentimentAnalysis
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

        database = DB(settings.PG_DB_USER,
                      settings.PG_DB_PASSWORD, settings.PG_DB_NAME)
        database.connect()

        keyword = Keyword(database.con, database.meta)
        token = TwitterToken(database.con, database.meta)

        """Set tweepy api object and authentication"""
        token = token.find_by_group(group_name)
        auth = tweepy.OAuthHandler(
            token["consumer_key"], token["consumer_secret"])
        auth.set_access_token(token["access_token"], token["access_token_secret"])

        self.api = tweepy.API(auth)
        self.keyword = keyword
        self.keyword_list = keyword.find_by_group(group_name)
        self.tw_store = TweetStore(settings.COUCHDB_DB, settings.COUCHDB_SERVER)

    def execute(self):
        """Execute the twitter crawler, loop into the keyword_list"""
        while True:
            log.info("Star crawling back....")
            delay = 600
            for keyword in self.keyword_list:
                log.info('Crawl data for %s', keyword["keyword"])
                try:
                    self.crawl(keyword)
                except Exception as e:
                    log.error('Error in Crawling process', exc_info=True)
                    log.info("Sleeping for %ds", delay)
                    sleep(delay)
            # Sleep for 10 minutes after finishing crawl all of the keyword,
            # and start over again
            log.info("Sleeping for %ds...", delay)
            sleep(delay)

    def crawl(self, keyword):
        """ Crawl individual keyword """
        api = self.api
        max_id = -1
        since_id = None if keyword["since_id"] == -1 else keyword["since_id"]
        tweets = api.search(q=keyword["keyword"], include_entities=True,
                            lang="en", count=MAX_COUNT, since_id=since_id,
                            geocode=settings.GEO_CODE)

        # For the first time, run the search using since_id from database
        # update since_id in database with the first tweet id that we get
        if len(tweets) > 0:
            self.keyword.update_since_id(keyword["id"], tweets[0].id)
            for tweet in tweets:
                # If we have reach the since_id, break from loop
                if tweet.id == since_id:
                    break
                # Update sentiment score
                tweet._json["sentiment"] = SentimentAnalysis.get_sentiment(tweet_text=tweet.text)
                self.tw_store.save_tweet(tweet._json)
            max_id = tweets[-1].id
            self.test_rate_limit(api)
        else:
            return

        while True:
            tweets = api.search(q=keyword["keyword"], include_entities=True,
                                lang="en", count=MAX_COUNT, max_id=max_id - 1,
                                geocode=settings.GEO_CODE)

            # Check if the api return value, otherwise break from loop
            # continue crawl next keyword
            if len(tweets) > 0:
                for tweet in tweets:
                    # If we have reach the since_id, break from loop
                    if tweet.id == since_id:
                        break
                    # Update sentiment score
                    tweet._json["sentiment"] = SentimentAnalysis.get_sentiment(tweet_text=tweet.text)
                    self.tw_store.save_tweet(tweet._json)
                max_id = tweets[-1].id
            else:
                break
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
        # Get the number of remaining requests
        remaining = int(api.last_response.headers['x-rate-limit-remaining'])
        # Check if we have reached the limit
        if remaining == 0:
            limit = int(api.last_response.headers['x-rate-limit-limit'])
            reset = int(api.last_response.headers['x-rate-limit-reset'])
            # Parse the UTC time
            reset = datetime.fromtimestamp(reset)
            # Let the user know we have reached the rate limit
            log.info("0 of %d requests remaining until %d.", limit, reset)

            if wait:
                # Determine the delay and sleep
                delay = (reset - datetime.now()).total_seconds() + buffer
                log.info("Sleeping for %d", delay)
                sleep(delay)
                # We have waited for the rate limit reset. OK to proceed.
                return True
            else:
                # We have reached the rate limit. The user needs to handle the
                # rate limit manually.
                return False

        # We have not reached the rate limit
        return True
