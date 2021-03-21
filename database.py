import psycopg2
from configparser import ConfigParser


class Database:
    """class the responsible for the database"""
    def __init__(self, file_path: str):
        self.__connection = self.__connect_db(file_path)
        if self.__connection:
            self.__create_table()

    def __del__(self):
        self.__connection.close() # close the connection

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
            connection = psycopg2.connect(user=config.get('postgresql', 'user'),
                                          password=config.get('postgresql', "password"),
                                          host=config.get('postgresql', "host"),
                                          port=config.get('postgresql', "port"),
                                          database=config.get('postgresql', "database"))
        except Exception as e:
            print('cannot access data base')
            return None
        return connection

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
