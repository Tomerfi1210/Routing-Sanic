from sanic import Sanic
import sanic.response
import aiohttp
import parsel
import json
import psycopg2
from configparser import ConfigParser

app = Sanic(__name__)

connection = None


@app.route('/<page>', methods=['GET'])
async def test(request, page):
    response = await fetch(f'https://en.wikipedia.org/wiki/{page}')
    if connection:
        insert_data(response)
    return sanic.response.json(response)


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            resp = parsel.Selector(html)
            rlconf = resp.xpath('/html/head/script[1]/text()').extract_first().split(';')[1][7:].replace('!', '')
            rlconfJson = json.loads(rlconf)
            response_object = {'wgRequestId': rlconfJson['wgRequestId'],
                               'wgCategories': rlconfJson['wgCategories'],
                               'wgPageContentLanguage': rlconfJson['wgPageContentLanguage'],
                               'wgRelevantPageName': rlconfJson['wgRelevantPageName']}
            return response_object


def insert_data(rlconf_dict: dict):
    curs = connection.cursor()
    curs.execute(
        '''INSERT INTO wikientries(wgRequestId, wgCategories, wgPageContentLanguage, wgRelevantPageName) VALUES(%s,%s,%s,%s) ON CONFLICT (wgRequestId) DO NOTHING''',
        (rlconf_dict["wgRequestId"], rlconf_dict["wgCategories"], rlconf_dict["wgPageContentLanguage"],
         rlconf_dict["wgRelevantPageName"]))
    connection.commit()
    curs.close()


def create_table():
    curs = connection.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS WikiEntries
          (wgRequestId TEXT PRIMARY KEY NOT NULL,
          wgCategories TEXT[] NOT NULL,
          wgPageContentLanguage TEXT,
          wgRelevantPageName TEXT);''')
    curs.close()
    connection.commit()


def connect_db():
    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read('database.ini')

    try:
        # read values from a section
        connection = psycopg2.connect(user=config.get('postgresql', 'user'),
                                      password=config.get('postgresql', "password"),
                                      host=config.get('postgresql', "host"),
                                      port=config.get('postgresql', "port"),
                                      database=config.get('postgresql', "database"))
        return connection
    except Exception as e:
        print('cannot access db')
        print(e)


if __name__ == '__main__':
    connection = connect_db()
    create_table()
    app.run(host='0.0.0.0', port=8000)
