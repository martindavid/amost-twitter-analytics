import os, sys, time, json, couchdb, tweepy 
from couchdb.mapping import Document, TextField, FloatField
#from meaningcloud_client import sendPost

consumer_token = 'ifIEMehY2FZKYygyzdkCtzVHx'
consumer_secret = 'gkvEmZFKIIlIuVDBniV2grfvXw8GBj3pfNzLXVPNHpw2fjCSOQ'

access_token = "1646962993-MMYcOwuSDiAZyDFDTI5tXzSy7yoH6ybJiiMr7OR"
access_token_secret = "HC1qOFT5Qu7scrcfJRXPdDqzBulM4RZ22xlKIiVEwopb6"

#handles authentication 
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
"""
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())
myStream.filter(track=['python'], async=True)
"""
#set up couchdb (local version)
db_name = 'amost_twitter'
server_location = "http://localhost:5984/"
couch = couchdb.Server(server_location)
db = couch[db_name]

class listener(x):
    # A listener handles tweets received from the stream.
    # This is a custom listener that store received tweets to FILE.
    def on_data(self, tweet_data):
        try:
            #converts to json format then saves in couchdb
            tweets_json = json.loads(tweet_data)
            doc_id = tweets_json["id_str"]
            tweet_lang = tweets_json["lang"]
            #gets data from meaningcloud service
            """
            meaningcloud_data = sendPost(tweets_json["text"], tweet_lang)
            if meaningcloud_data is None:
                #if invalid language, topic and sentiment is not added to document
                doc = {"_id": doc_id, "tweet_data": tweets_json}
            else:
                sentiment_topic = meaningcloud_data.read()
                r = json.loads(sentiment_topic.decode())

                #handling of API call limit
                counter = int(r["status"]["remaining_credits"])
                if counter < 100:
                    print ("There are less than 100 API calls left on the current account.
                            Please insert a new key in meaningcloud_client.py")
                elif counter < 10:
                    print ("There are less than 10 API calls left on the current account.
                            Please insert a new key in meaningcloud_client.py")
                    print ("Terminating...")
                    sys.exit(0)

                #id of the document is the tweet id
                #meaningcloud data is added as attribute in the document
                doc = {"_id": doc_id, "tweet_data": tweets_json, "meaningcloud": r}
            """
            #saves the document to database
            db.save(doc)
            print('added: ' + doc_id)
            return True
        except BaseException as e:
            print(e)
            time.sleep(5)
        except couchdb.http.ResourceConflict:
            #handles duplicates
            time.sleep(5)

    def on_error(self,status):
        #returning False in on_data disconnects the stream
        if status_code == 420:
            print(status)
            return False

def main():
    print("Streaming is started.... Ctrl+C to abort.")
    try:
        twitterStream = Stream(auth,listener())
        twitterStream.filter(track=['python'], async=True)
    except Exception as e:
        print (e)
        print("Error or execution finished. Program exiting... ")
        twitterStream.disconnect()

main() 
 

    