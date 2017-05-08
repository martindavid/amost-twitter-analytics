import os
import couchdb
import re
import HTMLParser
from collections import Counter
from nltk.corpus import stopwords
import string
from lib.genderComputer.genderComputer import GenderComputer

server = couchdb.Server(url='http://127.0.0.1:15984/')
db = server['tweets']
gc = GenderComputer(os.path.abspath('./data/nameLists'))

# Get view data per day
from collections import Counter
view_data = []
for row in db.view('_design/analytics/_view/tweets-victoria', startkey="2017/3/13", endkey="2017/3/13"):
    view_data.append(row.value)
