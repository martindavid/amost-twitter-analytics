from __future__ import print_function
import math
import couchdb

from app.sentiment_analysis import SentimentAnalysis
from app.logger import LOGGER as log

import settings

ALL_DOCS_VIEW = '_all_docs'

try:
    log.info("START db updater script")
    log.info("-----------------------")
    server = couchdb.Server(url=settings.COUCHDB_SERVER)
    db = server[settings.COUCHDB_DB]

    info = db.info()
    doc_count = info["doc_count"]
    num_per_request = 10000

    iteration = math.ceil(doc_count / num_per_request)

    for i in range(iteration):
        log.info('Run %d iteration' % i)
        for row in db.view(ALL_DOCS_VIEW, limit=num_per_request, skip=i * num_per_request):
            data = db.get(row.id)
            data["sentiment"] = SentimentAnalysis.get_sentiment(data["text"])
            db.save(data)
        log.info('%d iteration success')
    log.info("FINISH db updater script")
except Exception as e:
    log.error(e)
