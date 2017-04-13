import tweepy 
import json
from time import sleep
from TwitterAPI import TwitterAPI
from tweepy.streaming import StreamListener
import logging
from app.db import DB, Keyword, TwitterToken
from app.tweet_store import TweetStore
import settings  

# Create a class inheriting from StreamListener
class TwitterStream(StreamListener): 
    def on_data(self, data):
        print("Hello!!!")
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
            # print(warning['message'])
            return false

    def on_status(self, status):
        self.tw_store.save_tweet(status)
        print(status)

    def on_error(self, status):
        if status == 420:
            #print(status)
            self.on_timeout()
 
    def on_timeout(self):
        # print("Timeout, sleeping for 10 sec...\n")
        time.sleep(10)
        return 

class TwitterStreamExe(object): 
    def __init__(self, group_name):
        database = DB(settings.PG_DB_USER, settings.PG_DB_PASSWORD, settings.PG_DB_NAME)
        database.connect()

        keyword = Keyword(database.con, database.meta)
        token = TwitterToken(database.con, database.meta)

        # Set tweepy api object and authentication
        token = token.find_by_group(group_name)
        self.auth = tweepy.OAuthHandler(token["consumer_key"], token["consumer_secret"])
        self.auth.set_access_token(token["access_token"], token["access_token_secret"])

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.keyword = keyword
        self.keyword_list = keyword.find_by_group(group_name)
        self.tw_store = TweetStore('tweets', settings.COUCHDB_SERVER)

    def execute(self):
        # Execute the twitter crawler, loop into the keyword_list
        for keyword in self.keyword_list:
            logging.info('Crawl data for %s' % keyword["keyword"])
            self.crawl(keyword)   

    def crawl(self, keyword):   
        loop = True
        while (loop):
            listen = TwitterStream(self.api) 
            track = keyword 
            stream = tweepy.Stream(self.auth, listen) 

            # print ("Twitter streaming started... ")

            try:
                stream.filter(track=[keyword])
                loop = False
            except:
                # print ("Error!...Retry after 10 sec")
                loop = True
                stream.disconnect()
                sleep(10)
                continue 





   
       



   



        
        
        
        
        
        
        
        
        
        
        
        
        