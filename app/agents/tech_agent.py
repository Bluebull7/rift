from app.agents.base_agent import BaseAgent
from app.utils.memory_trigger import MemoryTrigger
class TechAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "TechAgent")

    def save_task(self, task_id, task_details):
        """
        Save a task to Redis with the correct key format.
        Example key: "TechAgent:task:<task_id>"
        """
        key = self.memory_key(f"task:{task_id}")
        self.memory.set(key, task_details)  # Ensure task_details is a dictionary or JSON
        self.log(f"Task {task_id} saved.")
        return f"Task {task_id} saved successfully."

    def get_task(self, task_id):
        """
        Retrieve a task from Redis.
        """
        key = self.memory_key(f"task:{task_id}")
        task = self.memory.get(key)  # Fetch the task from Redis
        if task:
            self.log(f"Task {task_id} retrieved: {task}")
            return task
        else:
            self.log(f"Task {task_id} not found.")
            return f"Task {task_id} not found."
        
    def analyze_data(self, task_id, data):
        # Example analysis: Generate summary stats
        analysis_result = {"task_id": task_id, "summary": f"Analyzed {len(data)} items"}
        self.memory.set(self.memory_key(f"analysis:{task_id}"), analysis_result)
        self.memory.hset(f"shared:task_context:{task_id}", "TechAgent_analysis", analysis_result)
        self.log(f"Analysis for task {task_id} saved: {analysis_result}")
        return analysis_result

    def parse_command(self, command, *args, **kwargs):
        if command == "save_task":
            return self.save_task(*args, **kwargs)
        elif command == "get_task":
            return self.get_task(*args, **kwargs)
        elif command == "analyze_data":
            return self.analyze_data(*args, **kwargs)
        else:
            return f"Unknown command: {command}"
