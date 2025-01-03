from app.agents.base_agent import BaseAgent
from app.utils.memory_trigger import MemoryTrigger
class TechAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "TechAgent")

        # Subscribe to updates
        self.memory.subscribe("global_updates", self.handle_update)
    
    def parse_command(self, command, *args, **kwargs):
        if command == "analyze_data":
            return self.analyze_data(*args, **kwargs)
        else:
            return f"Unknown command: {command}"
    def analyze_data(self, task_id, data):
        analysis_result = {"task_id": task_id, "summary": f"Analyzed {len(data)} items"}
        self.memory.set(self.memory_key(f"analysis:{task_id}"), analysis_result)
        self.memory.hset(f"shared:task_context:{task_id}", "TechAgent_analysis", analysis_result)

        # Publish update
        self.memory.publish(f"task_updates:{task_id}", {"agent": "TechAgent", "action": "analyzed", "data": analysis_result})
        self.log(f"Analysis for task {task_id} saved: {analysis_result}")
        return analysis_result

    def handle_update(self, message):
        self.log(f"Received update: {message}")
        # Process incoming updates if necessary
