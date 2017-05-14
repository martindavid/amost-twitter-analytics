from __future__ import print_function
from datetime import date, timedelta
import sqlalchemy
from app.logger import LOGGER as log
import datetime


class DB(object):
    """ Main class to handle connection to database

    Attributes:
        user: username used to access the database
        password: password used to access the database
        database_name: database name to be used
        host: database server host; default to localhost
        port: database server port; default to 5432
        con: sqlalchemy connection object
        meta: sqlalchemy meta object
    Notes:
        con and meta object will only be set after call connect() method
    """

    def __init__(self, user, password, database_name, host='localhost', port=5432):
        self.user = user
        self.password = password
        self.database_name = database_name
        self.host = host
        self.port = port
        self.con = None
        self.meta = None

    def connect(self):
        '''Connect to database then set con and meta attributes'''

        # We connect with the help of the PostgreSQL URL
        # postgresql://federer:grandestslam@localhost:5432/tennis
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host,
                         self.port, self.database_name)

        try:
            # The return value of create_engine() is our connection object
            con = sqlalchemy.create_engine(url, client_encoding='utf8')

            # We then bind the connection to MetaData()
            meta = sqlalchemy.MetaData(bind=con, reflect=True)
        except Exception as ex:
            log.error(ex)
            return False

        self.con = con
        self.meta = meta

        return True


class AnalyticsLog(object):
    """Handle database access for analytics_log table
    """

    def __init__(self, con, meta):
        self.con = con
        self.meta = meta
        print(meta)
        self.data = meta.tables['analytics_log']

    def fetch_unprocessed_data(self):
        yesterday = date.today() - timedelta(1)
        yesterday = yesterday.strftime('%Y/%-m/%-d')

        search_yesterday = self.data.select().where(self.data.c.data_timestamp ==
                                                    yesterday and self.data.c.status == False)

        search_result = [
            result for result in self.con.execute(search_yesterday)]

        if len(search_result) <= 0:
            insert_yesterday = self.data.insert().values(
                data_timestamp=yesterday, status=False)
            self.con.execute(insert_yesterday)

        search_clause = self.data.select().where(self.data.c.status == False)
        date_list = []
        for result in self.con.execute(search_clause):
            date_list.append(result[0])

        return date_list

    def update_timestamp_data(self, timestamp):
        try:
            update_statement = self.data.update().where(
                self.data.c.data_timestamp == timestamp).values(status=True)
            self.con.execute(update_statement)
        except Exception as e:
            log.error(e)
