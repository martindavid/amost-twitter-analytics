from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from couchdb.design import ViewDefinition
import couchdb
from datetime import datetime
import pytz 

try:
    couch = couchdb.Server()
    db_sa = couch['sa-time']
    db_tweets = couch['tweets']
except:
    db_sa = couch.create('sa-time')
    analyzer = SentimentIntensityAnalyzer()  
    
for row in db_tweets.view('_design/sa2/_view/sa-location'):  
    vs = analyzer.polarity_scores(row.value['text']) 
    if vs['compound'] >= 0.5:
        result_tw = 1
    elif vs['compound'] <= -0.5:
        result_tw = -1
    else:
        result_tw = 0       
    db_sa[row.id] = dict(time=row.value['time'], text=row.value['text'], neg=vs['neg'], neu=vs['neu'], pos=vs['pos'], comp=vs['compound'], result=result_tw)
    