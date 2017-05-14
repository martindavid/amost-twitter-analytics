from os.path import join, dirname
import os
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SENTRY_DSN = os.environ.get('SENTRY_DSN')

# PostgreSql Configuration
PG_DB_NAME = os.environ.get('PG_DB_NAME')
PG_DB_USER = os.environ.get('PG_DB_USER')
PG_DB_PASSWORD = os.environ.get('PG_DB_PASSWORD')

# CouchDB configuration
COUCHDB_DB = os.environ.get('COUCHDB_DB')
COUCHDB_SERVER = os.environ.get('COUCHDB_SERVER')