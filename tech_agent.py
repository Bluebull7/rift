from redis_memory import RedisMemory 
class TechAgent:
    def __init__(self, memory: RedisMemory):
        self.memory = memory
        self.agent_id = "TechAgent"

    def save_task(self, task_id, task_details):
        self.memory.set(f"{self.agent_id}:task:{task_id}", task_details)

    def get_task(self, task_id):
        return self.memory.get(f"{self.agent_id}:task:{task_id}")

    def list_tasks(self):
        return self.memory.get_list(f"{self.agent_id}:tasks")

    def add_task_to_list(self, task_id, task_details):
        self.memory.append_to_list(f"{self.agent_id}:tasks", {"task_id": task_id, "details": task_details})
