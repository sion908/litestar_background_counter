import asyncio
from logging import getLogger

from redis_service import RedisService

logger = getLogger(__name__)


async def system_upkeep(id: int, counter: int) -> None:

    logger.info(f"called system_upkeep: id<{id}>")
    r = RedisService()

    while True:
        data = r.load(id)

        counter = data.get('counter', 0)
        if counter < 0:
            break
        counter += 1
        r.save(id, {"counter": counter})
        logger.info(f"count id <{id}>, counter <{counter}>")
        await asyncio.sleep(2)

    r.delete(id)
    logger.info("end the counter")
