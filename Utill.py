import psycopg2
from configparser import ConfigParser


class Database:
    def __init__(self, file_path: str):
        self.__connection = self.__connect_db(file_path)
        if self.__connection:
            self.__create_table()

    def __del__(self):
        self.__connection.close()

    def __connect_db(self, file_path: str):
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
        return connection

    def __create_table(self):
        curs = self.__connection.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS WikiEntries
              (wgRequestId TEXT PRIMARY KEY NOT NULL,
              wgCategories TEXT[] NOT NULL,
              wgPageContentLanguage TEXT,
              wgRelevantPageName TEXT);''')
        curs.close()
        self.__connection.commit()

    def insert_data(self, rlconf_dict: dict):
        curs = self.__connection.cursor()
        curs.execute(
            '''INSERT INTO wikientries(wgRequestId, wgCategories, wgPageContentLanguage, wgRelevantPageName) VALUES(%s,%s,%s,%s) ON CONFLICT (wgRequestId) DO NOTHING''',
            (rlconf_dict["wgRequestId"], rlconf_dict["wgCategories"], rlconf_dict["wgPageContentLanguage"],
             rlconf_dict["wgRelevantPageName"]))
        self.__connection.commit()
        curs.close()
