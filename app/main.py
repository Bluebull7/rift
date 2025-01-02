from agents.tech_agent import TechAgent
from agents.concept_agent import ConceptAgent
from utils.redis_memory import RedisMemory
from agents.task_agent import TaskAgent
from agents.base_agent import BaseAgent



if __name__ == "__main__":
    memory = RedisMemory()

    # Set sample data
    memory.set("TechAgent:task:001", {"description": "Deploy Redis", "deadline": "2025-01-03T10:00:00"})
    memory.append_to_list("TechAgent:tasks", {"task_id": "001", "details": {"description": "Deploy Redis"}})
    memory.set("ConceptAgent:preferences:user123", {"theme": "light", "notifications": "enabled"})
    memory.append_to_list("ConceptAgent:history:user123", {"action": "enable_dark_mode"})

    # Test proactive behaviors
    tech_agent = TechAgent(memory)
    tech_agent.proactive_reminder()
    tech_agent.proactive_overload_check()

    concept_agent = ConceptAgent(memory)
    concept_agent.proactive_preference_suggestion()
    concept_agent.proactive_anomaly_alert()

    task_agent = TaskAgent(memory)
    task_agent.proactive_deadline_reminder()
    task_agent.proactive_overdue_notification()
