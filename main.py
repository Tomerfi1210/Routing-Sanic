from sanic import Sanic
from sanic import exceptions
from sanic.exceptions import abort
import sanic.response
import aiohttp
import parsel
import json
from database import Database

app = Sanic(__name__)

database = None


@app.route('/<page>', methods=['GET'])
async def test(request, page):
    if not page or page == "":
        abort(404)
    try:
        response = await fetch(f'https://en.wikipedia.org/wiki/{page}')
        database.insert_data(response)
        return sanic.response.json({"response": "entry added to db"})
    except:
        raise sanic.exceptions.SanicException("error in server")


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


if __name__ == '__main__':
    try:
        database = Database('database.ini')
        if database:
            app.run(host='0.0.0.0', port=8000)
    except ValueError as e:
        print(e)
