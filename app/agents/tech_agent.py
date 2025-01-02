from app.agents.base_agent import BaseAgent
from app.utils.memory_trigger import MemoryTrigger

class TechAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "TechAgent")
        self.trigger = MemoryTrigger(memory)
    

    def save_task(self, task_id, task_details):
        self.memory.set(self.memory_key(f"task:{task_id}"), task_details)
        self.log(f"Task {task_id} saved.")
        return f"Task {task_id} saved successfully."

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
    
    def proactive_reminder(self):
        """Check for tasks with approaching deadlines and send reminders."""
        tasks = self.memory.get_list(self.memory_key("tasks"))
        for task in tasks:
            if self.trigger.check_deadline(self.memory_key(f"task:{task['task_id']}")):
                self.log(f"Reminder: Task {task['task_id']} ('{task['details']['description']}') is nearing its deadline!")

    def proactive_overload_check(self):
        """Notify if task load exceeds manageable thresholds."""
        tasks = self.memory.get_list(self.memory_key("tasks"))
        if len(tasks) > 10:
            self.log(f"Warning: You have {len(tasks)} tasks. Consider prioritizing or delegating.")