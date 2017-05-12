from __future__ import print_function
import couchdb
import json
from app.logger import LOGGER as log

DEFAULT_URL = 'http://127.0.0.1:5984/'


class TweetStore(object):
    """ Main class to handle interaction with CouchDB database

    Args:
        db_name: database name in couchdb
        url: connection url for couchdb, by default 'http://127.0.0.1:5984/'

    Attributes:
        server: couchdb server instance
        dbase: database instance of couchdb server
    """

    def __init__(self, db_name, url=DEFAULT_URL):
        try:
            self.server = couchdb.Server(url=url)
            self.dbase = self.server.create(db_name)
        except couchdb.http.PreconditionFailed:
            self.dbase = self.server[db_name]

    def save_tweet(self, twitter):
        """Save tweet data into database
        Will check if data is not exists then save it, if exists ignore it

        Args:
            twitter: tweepy status object
        """
        if isinstance(twitter, dict):
            json_data = twitter
        else:
            json_data = json.loads(twitter)
        doc = self.dbase.get(json_data["id_str"])
        if doc is None:
            try:
                data = self._construct_tweet_data(json_data)
                self.dbase.save(data)
            except couchdb.http.ResourceConflict:
                pass
            except Exception as e:
                log.error(e)

    def _construct_tweet_data(self, json_data):
        data = {
            "_id": json_data["id_str"],
            "lang": json_data["lang"],
            "retweeted": json_data["retweeted"],
            "coordinates": json_data["coordinates"],
            "retweet_count": json_data["retweet_count"],
            "hashtags": json_data["entities"]["hashtags"],
            "user_mentions": json_data["entities"]["user_mentions"],
            "text": json_data["text"],
            "sentiment": json_data["sentiment"],
            "created_at": json_data["created_at"],
            "user": {
                "followers_count": json_data["user"]["followers_count"],
                "time_zone": json_data["user"]["time_zone"],
                "profile_image_url": json_data["user"]["profile_image_url"],
                "location": json_data["user"]["location"],
                "friends_count": json_data["user"]["friends_count"],
                "statuses_count": json_data["user"]["statuses_count"],
                "name": json_data["user"]["name"],
                "id_str": json_data["user"]["id_str"],
                "lang": json_data["user"]["lang"]
            },
            "favorite_count": json_data["favorite_count"]
        }

        return data
