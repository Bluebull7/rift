from app.agents.base_agent import BaseAgent
from app.utils.memory_trigger import MemoryTrigger
from datetime import datetime

class TaskAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "TaskAgent")
        self.trigger = MemoryTrigger(memory)
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
        
        elif command == "track_progress":
            return self.track_progress(*args, **kwargs)
        else:
            self.log(f"Unknown command: {command}")

    def proactive_deadline_reminder(self):
        """Remind users of upcoming task deadlines."""
        users = self.memory.get_list(self.memory_key("users"))
        for user in users:
            tasks = self.memory.get_list(self.memory_key(f"assigned_tasks:{user}"))
            for task in tasks:
                if self.trigger.check_deadline(self.memory_key(f"task:{task}")):
                    self.log(f"Reminder for {user}: Task {task} is nearing its deadline!")

    def proactive_overdue_notification(self):
        """Notify about overdue tasks."""
        users = self.memory.get_list(self.memory_key("users"))
        for user in users:
            tasks = self.memory.get_list(self.memory_key(f"assigned_tasks:{user}"))
            for task in tasks:
                task_data = self.memory.get(self.memory_key(f"task:{task}"))
                if task_data and datetime.fromisoformat(task_data["deadline"]) < datetime.now():
                    self.log(f"Overdue Task: {task} assigned to {user} is overdue.")
    
    def track_progress(self, task_id):
        # Check if all dependencies are resolved
        context = self.memory.hgetall(f"shared:task_context:{task_id}")
        if "TechAgent_analysis" in context and "ConceptAgent_narrative" in context:
            progress = {"task_id": task_id, "status": "completed"}
            self.memory.set(self.memory_key(f"progress:{task_id}"), progress)
            self.log(f"Task {task_id} marked as completed: {progress}")
            return progress
        return {"task_id": task_id, "status": "in-progress"}