import redis
import json
from typing import Any
import threading

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
            value = json.dumps(value)  # Serialize only once
        self.client.set(key, value, ex=expire)
        print(f"[DEBUG] SET key={key}, value={value}")  # Debug log
    
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

    def hset(self, key: str, field: str, value: Any):
        """Set a field in a Redis hash."""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.client.hset(key, field, value)

    def hget(self, key: str, field: str) -> Any:
        """Get a field from a Redis hash."""
        value = self.client.hget(key, field)
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def rpush(self, key: str, value: Any):
        """Append a value to a Redis list."""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.client.rpush(key, value)

    def lrange(self, key: str, start: int, end: int) -> list:
        """Retrieve a range of elements from a Redis list."""
        return [json.loads(item) for item in self.client.lrange(key, start, end)]
    
    def publish(self, channel: str, message: dict):
        """Publish a message to a Redis channel."""
        self.client.publish(channel, json.dumps(message))

    def subscribe(self, channel: str, callback):
        """Subscribe to a Redis channel and process messages using a callback."""
        pubsub = self.client.pubsub()
        pubsub.subscribe(**{channel: callback})

        def listen():
            for message in pubsub.listen():
                if message["type"] == "message":
                    callback(json.loads(message["data"]))

        # Run subscription in a separate thread
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
