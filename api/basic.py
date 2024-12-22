from litestar import Litestar, get

from tasks import (
    system_upkeep
)
from redis_service import RedisService
from litestar import Litestar, Response, get
from logging import getLogger
from litestar.background_tasks import BackgroundTask
from random import randint


logger = getLogger(__name__)

@get("/counter/start")
async def start_counter() -> dict:
    """現在のカウンター値を取得"""

    id = randint(0,100)
    counter = 0
    r = RedisService()
    r.save(id, {"counter": counter})
    return Response(
        {"id": id},
        background=BackgroundTask(system_upkeep, id, counter),
    )

@get("/counter/{id:int}")
async def get_counter(id: int) -> dict:
    """現在のカウンター値を取得"""
    r = RedisService()
    data = r.load(id)
    return {"counter": data.get('counter', 0)}


@get("/counter/{id:int}/v/{counter:int}")
async def set_counter(id:int,counter: int) -> dict:
    """カウンター値を設定"""
    r = RedisService()
    r.save(id, {"counter": counter})

    logger.info(f"Counter set to: {counter}")
    return {"counter": counter}

@get("/counter/{id:int}/end")
async def end_counter(id: int) -> dict:
    """現在のカウンター値を取得"""
    r = RedisService()
    r.save(id, {"counter": -1})
    return {"message": "ended"}


app = Litestar(
    route_handlers=[
        start_counter,
        get_counter,
        set_counter,
        end_counter
    ],
)
