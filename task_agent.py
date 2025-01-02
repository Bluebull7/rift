from base_agent import BaseAgent

class TaskAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "TaskAgent")

    def assign_task(self, user_id, task_id):
        self.memory.append_to_list(self.memory_key(f"assigned_tasks:{user_id}"), task_id)
        self.log(f"Task {task_id} assigned to user {user_id}.")

    def get_assigned_tasks(self, user_id):
        return self.memory.get_list(self.memory_key(f"assigned_tasks:{user_id}"))

    def parse_command(self, command, *args, **kwargs):
        if command == "assign_task":
            self.assign_task(*args, **kwargs)
        elif command == "get_assigned_tasks":
            return self.get_assigned_tasks(*args, **kwargs)
        else:
            self.log(f"Unknown command: {command}")
