from app.agents.base_agent import BaseAgent
from app.utils.memory_trigger import MemoryTrigger

class ConceptAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "ConceptAgent")

        # Subscribe to updates
        self.memory.subscribe("global_updates", self.handle_update)

    def generate_narrative(self, task_id):
        analysis = self.memory.hget(f"shared:task_context:{task_id}", "TechAgent_analysis")
        if not analysis:
            return f"No analysis found for task {task_id}"

        narrative = f"The analysis for task {task_id} concluded: {analysis['summary']}."
        self.memory.set(self.memory_key(f"narrative:{task_id}"), narrative)
        self.memory.hset(f"shared:task_context:{task_id}", "ConceptAgent_narrative", narrative)

        # Publish update
        self.memory.publish(f"task_updates:{task_id}", {"agent": "ConceptAgent", "action": "narrative_generated", "data": narrative})
        self.log(f"Narrative for task {task_id} generated: {narrative}")
        return narrative

    def handle_update(self, message):
        self.log(f"Received update: {message}")
        # Process incoming updates if necessary
