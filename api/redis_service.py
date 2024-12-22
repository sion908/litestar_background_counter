import json
import redis

import logging

logger = logging.getLogger(__name__)


class RedisService:
    alias: str = "counter"
    def __init__(self, host='redis', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def save(self, counter_id: str, data: dict) -> None:

        self.redis_client.set(f"{self.alias}_{counter_id}", json.dumps(data))


    def delete(self, counter_id: str):
        self.redis_client.delete(f"{self.alias}_{counter_id}")

    def load(self, counter_id: str) -> None|dict:
        data = self.redis_client.get(f"{self.alias}_{counter_id}")
        if not data:
            return None

        return json.loads(data)
