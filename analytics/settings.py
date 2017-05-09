from os.path import join, dirname
import os
from dotenv import Dotenv

dotenv_path = join(dirname(__file__), '.env')
Dotenv(dotenv_path)

SENTRY_DSN = os.environ.get('SENTRY_DSN')

# CouchDB configuration
COUCHDB_DB = os.environ.get('COUCHDB_DB')
COUCHDB_SERVER = os.environ.get('COUCHDB_SERVER')