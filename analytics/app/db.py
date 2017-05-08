class DB(object):
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