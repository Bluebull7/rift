from datetime import datetime, timedelta

class MemoryTrigger:
    def __init__(self, memory):
        self.memory = memory

    def check_deadline(self, key, threshold_hours=24):
        """Check if a task deadline is approaching."""
        task = self.memory.get(key)
        if not task or "deadline" not in task:
            return False
        deadline = datetime.fromisoformat(task["deadline"])
        return deadline <= datetime.now() + timedelta(hours=threshold_hours)

    def check_anomaly(self, key, expected_pattern):
        """Detect if a key's value deviates from an expected pattern."""
        value = self.memory.get(key)
        return value != expected_pattern
