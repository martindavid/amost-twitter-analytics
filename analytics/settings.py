from os.path import join, dirname
import os
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SENTRY_DSN = os.environ.get('SENTRY_DSN')

# CouchDB configuration
COUCHDB_DB = os.environ.get('COUCHDB_DB')
COUCHDB_SERVER = os.environ.get('COUCHDB_SERVER')