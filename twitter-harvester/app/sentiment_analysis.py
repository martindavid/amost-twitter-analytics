from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.logger import LOGGER as log


class SentimentAnalysis(object):

    @staticmethod
    def get_sentiment(tweet_text):
        try:
            analyzer = SentimentIntensityAnalyzer()
            return analyzer.polarity_scores(tweet_text)
        except Exception as e:
            log.error(e)
