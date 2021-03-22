import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Database:
    """class the responsible for the database"""
    def __init__(self, file_path: str):
        self.__connect_db(file_path)
        if self.__connection:
            self.__create_table()

    def __del__(self):
        self.__connection.close() # close the connection
    def __db_exists(self, db_name):
        cur = self.__connection.cursor()
        cur.execute("SELECT datname FROM pg_database")
        db_list = cur.fetchall()
        self.__connection.commit()
        if(db_name,) in db_list:
            return True
        return False

    def __connect_db(self, file_path: str):
        """
        connect the database to the server
        Get all the parameters to connect from the .ini file
        """
        # instantiate
        config = ConfigParser()

        # parse existing file
        config.read(file_path)

        try:
            # read values from a section
            # conect to defualt db
            self.__connection = psycopg2.connect(user=config.get('postgresql', 'user'),
                                          password=config.get('postgresql', "password"),
                                          host=config.get('postgresql', "host"),
                                          port=config.get('postgresql', "port"))
            self.__connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            if not self.__db_exists(config.get('postgresql', 'database')):
                self.__create_db(config.get('postgresql', 'database'))
            self.__connection.close()
            self.__connection = psycopg2.connect(user=config.get('postgresql', 'user'),
                                         password=config.get('postgresql', "password"),
                                         host=config.get('postgresql', "host"),
                                         port=config.get('postgresql', "port"),
                                         database=config.get('postgresql', 'database'))

        except Exception as e:
            print(e)
            return None

    def __create_db(self, db_name):
        curs = self.__connection.cursor()
        # command =  + db_name+";"
        curs.execute(sql.SQL("CREATE DATABASE {}".format(db_name)))


    def __create_table(self):
        """function that create table in database"""
        curs = self.__connection.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS WikiEntries
              (wgRequestId TEXT PRIMARY KEY NOT NULL,
              wgCategories TEXT[] NOT NULL,
              wgPageContentLanguage TEXT,
              wgRelevantPageName TEXT);''')
        curs.close()
        self.__connection.commit()

    def insert_data(self, rlconf_dict: dict):
        """
        Insert the json in to our database
        :param rlconf_dict: the wanted object dict type
        :return: None
        """
        curs = self.__connection.cursor()
        curs.execute(
            '''INSERT INTO wikientries(wgRequestId, wgCategories, wgPageContentLanguage, wgRelevantPageName) VALUES(%s,%s,%s,%s) ON CONFLICT (wgRequestId) DO NOTHING''',
            (rlconf_dict["wgRequestId"], rlconf_dict["wgCategories"], rlconf_dict["wgPageContentLanguage"],
             rlconf_dict["wgRelevantPageName"]))
        self.__connection.commit()
        curs.close()
