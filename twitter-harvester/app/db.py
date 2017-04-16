import sqlalchemy
import logging
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
        url = url.format(self.user, self.password, self.host, self.port, self.database_name)

        try:
            # The return value of create_engine() is our connection object
            con = sqlalchemy.create_engine(url, client_encoding='utf8')

            # We then bind the connection to MetaData()
            meta = sqlalchemy.MetaData(bind=con, reflect=True)
        except Exception as ex:
            logging.error(ex)
            return False

        self.con = con
        self.meta = meta

        return True


class Keyword(object):
    """Handle database access for Keyword table

    Attributes:
        con: database connection object from sqlalchemy initialization
        meta: database meta object from sqlalchemy initialization
        data: keyword table from database
    """
    def __init__(self, con, meta):
        self.con = con
        self.meta = meta
        self.data = meta.tables['keyword']

    def find_by_group(self, group_name):
        """Fetch a keyword from database

        Args:
            group_name: a search group name to be fetched

        Returns:
            array of dictionary containing:
                - keyword
                - max_id
                - since_id
        """
        search_clause = self.data.select().where(self.data.c.keyword_group == group_name)
        results = []
        for result in self.con.execute(search_clause):
            keyword = {}
            keyword["id"] = result[0]
            keyword["keyword"] = result[1]
            keyword["max_id"] = result[3]
            keyword["since_id"] = result[4]
            results.append(keyword)

        return results

    def update_max_id(self, keyword_id, max_id):
        """Update keyword max_id value in database"""
        try:
            update_stmt = self.data.update().\
                                where(self.data.c.id == keyword_id).\
                                values(max_id=max_id)
            self.con.execute(update_stmt)
        except Exception as ex:
            logging.error(ex)

    def update_since_id(self, keyword_id, since_id):
        """Update keyword since_id value in database"""
        try:
            update_stmt = self.data.update().\
                                    where(self.data.c.id == keyword_id).\
                                    values(since_id=since_id, \
                                    updated_at=str(datetime.datetime.now()))
            self.con.execute(update_stmt)
        except Exception as ex:
            logging.error(ex)


class TwitterToken(object):
    """Handle database access for twitter_token table

    Attributes:
        con: sqlalchemy connection object
        meta: sqlalchemy meta object
        data: twitter_token table from database
    """
    def __init__(self, con, meta):
        self.con = con
        self.meta = meta
        self.data = meta.tables['twitter_token']

    def find_by_group(self, group_name):
        """Fetch twitter token data from database base on group name

        Args:
            group_name: group name associate with the twitter token
        Returns:
            dictionary contains:
            - consumer_key
            - consumer_secret
            - access_token
            - access_token_secret
        """
        search_clause = self.data.select().where(self.data.c.keyword_group == group_name)
        results = {}
        for result in self.con.execute(search_clause):
            results["consumer_key"] = result[1]
            results["consumer_secret"] = result[2]
            results["access_token"] = result[3]
            results["access_token_secret"] = result[4]

        return results
