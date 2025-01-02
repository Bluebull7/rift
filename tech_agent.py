from base_agent import BaseAgent

class TechAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "TechAgent")

    def save_task(self, task_id, task_details):
        self.memory.set(self.memory_key(f"task:{task_id}"), task_details)
        self.log(f"Task {task_id} saved.")

    def get_task(self, task_id):
        return self.memory.get(self.memory_key(f"task:{task_id}"))

    def list_tasks(self):
        return self.memory.get_list(self.memory_key("tasks"))

    def add_task_to_list(self, task_id, task_details):
        self.memory.append_to_list(self.memory_key("tasks"), {"task_id": task_id, "details": task_details})

    def parse_command(self, command, *args, **kwargs):
        if command == "save_task":
            self.save_task(*args, **kwargs)
        elif command == "get_task":
            return self.get_task(*args, **kwargs)
        elif command == "list_tasks":
            return self.list_tasks()
        elif command == "add_task_to_list":
            self.add_task_to_list(*args, **kwargs)
        else:
            self.log(f"Unknown command: {command}")
