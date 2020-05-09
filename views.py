import logging
import asyncio
import aiohttp
import aiohttp_jinja2
from aiohttp import web

from db import create_record, fetch_last_data, update_record
from mail import send_mail
from settings import API_HOST

log = logging.getLogger(__name__)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def summary():
    """
    {"cases":229881,"deaths":9377,"recovered":86254}
    {"country":"China","cases":80928,"todayCases":34,"deaths":3245,"todayDeaths":8,"recovered":70420,"active":7263,
    "critical":2274,"casesPerOneMillion":56}
    :return:
    """
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, API_HOST + '/all')
        return response


async def bangladesh():
    async with aiohttp.ClientSession() as session:
        return await fetch(session, API_HOST + '/countries/bangladesh')


async def top_deaths_country():
    async with aiohttp.ClientSession() as session:
        return await fetch(session, API_HOST + '/countries')


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
        create = {"today_deaths": bd.get("todayDeaths", 0), "today_affected": bd.get("todayCases", 0)}
        # create = {"today_deaths": 9, "today_affected": 1000}
        fetch_data = await fetch_last_data()

        if fetch_data:
            fetch_dict = fetch_data.to_dict()
            if fetch_dict["death"] != create["today_deaths"] and fetch_dict["affected"] != create['today_affected']:
                await update_record(fetch_data, create)
                send_mail(data=bd)
        else:
            await create_record(**create)

        # all_countries = await top_deaths_country()
        # async for country in all_countries:
        #
        # print(all_countries)

        await ws_current.send_json(world)
        await ws_current.send_json(bd)
        await asyncio.sleep(10)
