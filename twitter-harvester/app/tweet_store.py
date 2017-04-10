import couchdb

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
        json_data = twitter._json
        tweet_id = str(twitter.id)
        doc = self.dbase.get(tweet_id)
        if doc is None:
            json_data["_id"] = tweet_id
            self.dbase.save(json_data)
