import os
import couchdb
import re
import HTMLParser
from collections import Counter
from nltk.corpus import stopwords
import string
from lib.genderComputer.genderComputer import GenderComputer
from collections import Counter
from logger import LOGGER as log
import settings
from string_processor import StringPreprocessor


class TweetAnalytics(object):

    def __init__(self, date, data, tweets_db, hashtags_db, words_db, users_db):
        self.data = data
        self.date = date
        self.tweets_db = tweets_db
        self.hashtags_db = hashtags_db
        self.words_db = words_db
        self.users_db = users_db
        self.gc = GenderComputer(os.path.abspath('./data/nameLists'))

    def process_data(self):
        view_data = self.data
        self.process_hashtag(view_data)
        self.count_word_term(view_data)
        self.process_user_data(view_data)

    def process_hashtag(self, view_data):
        log.info("[%s] START - processing hashtag" % self.date)
        hashtag_count = Counter()
        hashtags = self.hashtags_db

        for row in view_data:
            hashtag_count.update(row["hashtags"])

        for tag in hashtag_count.most_common():
            # tag[0] -> hashtag, tag[1] -> frequency
            doc = hashtags.get(tag[0])
            if doc is None:
                data = {}
                data["_id"] = tag[0].replace(r'\u', '')  # use word as an id
                data["hashtag"] = tag[0].replace(r'\u', '')
                data["count"] = tag[1]
            else:
                data = doc
                data["count"] = data["count"] + tag[1]

            hashtags.save(data)
        log.info("[%s] END - processing hashtag" % self.date)

    def count_word_term(self, view_data):
        log.info("[%s] START - processing term frequency" % self.date)
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['rt', 'via']
        count_all = Counter()
        html_parser = HTMLParser.HTMLParser()
        emoji_pattern = re.compile(
            u"(\ud83d[\ude00-\ude4f])|"  # emoticons
            u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
            u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
            u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
            u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
            "+", flags=re.UNICODE)
        for row in view_data:
            clean_text = re.sub(r"http\S+", "", row['text'])
            clean_text = html_parser.unescape(clean_text)
            clean_text = emoji_pattern.sub(r'', clean_text)
            terms_stop = [term for term in StringPreprocessor.preprocess(
                clean_text) if term not in stop]
            count_all.update(terms_stop)

        for num in count_all.most_common():
            doc = self.words_db.get(num[0])  # num[0] -> word, num[1] -> frequency
            try:
                if doc is None:
                    data = {}
                    # make sure we don't save unsafe character
                    word_text = num[0].decode("utf8").encode('ascii', 'ignore')
                    data["_id"] = word_text  # use word as an id
                    data["word"] = word_text
                    data["count"] = num[1]
                else:
                    data = doc
                    data["count"] = data["count"] + num[1]
                self.words_db.save(data)
            except:
                continue
        log.info("[%s] END - processing term frequency" % self.date)

    def process_user_data(self, view_data):
        log.info("[%s] START - processing user data" % self.date)
        users = []
        for row in view_data:
            user = row["user"]
            try:
                gender = self.gc.resolveGender(user["name"], None)
                user["gender"] = gender
            except:
                continue
            users.append(user)

        for row in users:
            id = row["id"]
            doc = self.users_db.get(str(id))
            if doc is None:
                row["_id"] = str(row["id"])
                self.users_db.save(row)
        log.info("[%s] END - processing user data" % self.date)
