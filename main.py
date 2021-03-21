from sanic import Sanic
import sanic.response
import aiohttp
import parsel
import json
from Utill import Database

app = Sanic(__name__)


@app.route('/<page>', methods=['GET'])
async def test(request, page):
    response = await fetch(f'https://en.wikipedia.org/wiki/{page}')
    database.insert_data(response)
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


def create_database():
    global database


if __name__ == '__main__':
    create_database()
    try:
        database = Database('database.ini')
        app.run(host='0.0.0.0', port=8000)
    except ValueError as e:
        print(e)
