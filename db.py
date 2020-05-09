from asyncio_extras import threadpool

from pony.orm import *

__all__ = [
    'create_record', 'update_record', 'fetch_last_data'
]

db = Database()


class Bangladesh(db.Entity):
    id = PrimaryKey(int, auto=True)
    death = Required(int)
    affected = Required(int)


db.bind('sqlite', './covid19.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


async def create_record(**kwargs):
    """
    :param kwargs:
    :return:
    """
    async with threadpool():
        with db_session:
            Bangladesh(
                death=kwargs['today_deaths'],
                affected=kwargs['today_affected'],
            )


async def update_record(obj, data):
    """
    :param obj:
    :param data:
    :return:
    """
    async with threadpool():
        with db_session:
            bd = Bangladesh[obj.id]
            bd.death = data['today_deaths']
            bd.affected = data['today_affected']


async def fetch_last_data():
    """
    Fetch the last object
    Fetch the last object
    :return:
    """
    async with threadpool():
        with db_session:
            return Bangladesh.select().first()
