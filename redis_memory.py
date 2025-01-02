import redis
import json
from typing import Any

class RedisMemory:
    def __init__(self, host="localhost", port=6379, password=None):
        self.client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )

    def set(self, key: str, value: Any, expire=None):
        """Store data in Redis."""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.client.set(key, value, ex=expire)

    def get(self, key: str) -> Any:
        """Retrieve data from Redis."""
        value = self.client.get(key)
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def delete(self, key: str):
        """Delete data from Redis."""
        self.client.delete(key)

    def append_to_list(self, key: str, value: Any):
        """Append value to a list in Redis."""
        self.client.rpush(key, json.dumps(value))

    def get_list(self, key: str) -> list:
        """Retrieve list data from Redis."""
        return [json.loads(item) for item in self.client.lrange(key, 0, -1)]
