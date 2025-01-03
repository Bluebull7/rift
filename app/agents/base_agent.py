import logging
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, memory, agent_id):
        """
        Base class for all agents.
        :param memory: Instance of RedisMemory.
        :param agent_id: Unique identifier for the agent.
        """
        self.memory = memory
        self.agent_id = agent_id
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Set up a logger for the agent."""
        logger = logging.getLogger(self.agent_id)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def log(self, message):
        """Log a message."""
        self.logger.info(message)

    def memory_key(self, key):
        """Generate a namespaced memory key."""
        return f"{self.agent_id}:{key}"

    @abstractmethod
    def parse_command(self, command, *args, **kwargs):
        """Parse and execute a command."""
        pass
