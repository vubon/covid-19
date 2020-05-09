import logging
import asyncio
import aiohttp
import aiohttp_jinja2
from aiohttp import web

log = logging.getLogger(__name__)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def summary():
    """
    {"cases":229881,"deaths":9377,"recovered":86254}
    {"country":"China","cases":80928,"todayCases":34,"deaths":3245,"todayDeaths":8,"recovered":70420,"active":7263,"critical":2274,"casesPerOneMillion":56}
    :return:
    """
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, 'https://coronavirus-19-api.herokuapp.com/all')
        return response


async def bangladesh():
    async with aiohttp.ClientSession() as session:
        return await fetch(session, 'https://coronavirus-19-api.herokuapp.com/countries/bangladesh')


async def top_deaths_country():
    async with aiohttp.ClientSession() as session:
        return await fetch(session, 'https://coronavirus-19-api.herokuapp.com/countries')


async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})

    await ws_current.prepare(request)

    while True:
        bd = await bangladesh()
        bd['state'] = 'Bangladesh'
        world = await summary()
        world['state'] = 'global'
        # all_countries = await top_deaths_country()
        # async for country in all_countries:
        #
        # print(all_countries)

        await ws_current.send_json(world)
        await ws_current.send_json(bd)
        await asyncio.sleep(10)
