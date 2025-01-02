from tech_agent import TechAgent
from concept_agent import ConceptAgent
from redis_memory import RedisMemory
from task_agent import TaskAgent
from base_agent import BaseAgent

if __name__ == "__main__":
    memory = RedisMemory()

    tech_agent = TechAgent(memory)
    tech_agent.parse_command("save_task", "001", {"description": "Set up Redis", "status": "completed"})
    print("TechAgent Task:", tech_agent.parse_command("get_task", "001"))

    concept_agent = ConceptAgent(memory)
    concept_agent.parse_command("save_preference", "user123", {"theme": "dark", "notifications": "enabled"})
    print("ConceptAgent Preference:", concept_agent.parse_command("get_preference", "user123"))

    task_agent = TaskAgent(memory)
    task_agent.parse_command("assign_task", "user123", "001")
    print("TaskAgent Assigned Tasks:", task_agent.parse_command("get_assigned_tasks", "user123"))
