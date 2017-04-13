import tweepy 
import json
from time import sleep
from TwitterAPI import TwitterAPI
from tweepy.streaming import StreamListener
from db import DB, Keyword, TwitterToken
from tweet_store import TweetStore
#import settings

consumer_key = 'nyR8ejR7Z7LftoDYRoyusn2jg'
consumer_secret = 'lLlxxKAOd3DyIGTLVgq1Mwy8hOnsGPCTroBhAIbgqB31Dbp0WT'
access_token_key = '851934201506971648-TTEeRvC5pcTBu5GGl9LV1yqANvRMVu1'
access_token_secret = 'tyZVYaNiPm2bMjjo4bkEuGwABUHoBITlrnWnDEENqKZSl'
    
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Create a class inheriting from StreamListener
class TwitterStream(StreamListener):
    def __init__(self, api = None):
        self.api = api
        self.tw_store = TweetStore('tweets', 'http://127.0.0.1:5984/')

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
            print(warning['message'])
            return false

    def on_status(self, status):
        #print(status)
        self.tw_store.save_tweet(status) 

    def on_error(self, status):
        if status == 420:
            print(status)
            self.on_timeout()
 
    def on_timeout(self):
        print("Timeout, sleeping for 10 sec...\n")
        time.sleep(10)
        return 

def stream_crawl(keyword):   
    loop = True
    while (loop):
        track = keyword
        listen = TwitterStream(api)  
        stream = tweepy.Stream(auth, listen) 

        print ("Twitter streaming started... ")

        try:
            stream.filter(track=[keyword])
            loop = False
        except Exception as e:
            print(e)
            print ("Error!...Retry after 10 sec")
            loop = True
            stream.disconnect()
            sleep(10)
            continue

if __name__ == '__main__': 
    stream_crawl( "food" )