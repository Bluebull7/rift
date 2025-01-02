from tech_agent import TechAgent
from concept_agent import ConceptAgent
from redis_memory import RedisMemory

if __name__ == "__main__":
    memory = RedisMemory()

    # TechAgent example
    tech_agent = TechAgent(memory)
    tech_agent.save_task("001", {"description": "Set up Redis", "status": "completed"})
    tech_agent.add_task_to_list("001", {"description": "Set up Redis", "status": "completed"})
    print("TechAgent Task:", tech_agent.get_task("001"))
    print("TechAgent Task List:", tech_agent.list_tasks())

    # ConceptAgent example
    concept_agent = ConceptAgent(memory)
    concept_agent.save_preference("user123", {"theme": "dark", "notifications": "enabled"})
    concept_agent.log_interaction("user123", {"timestamp": "2025-01-02", "action": "login"})
    print("ConceptAgent Preference:", concept_agent.get_preference("user123"))
    print("ConceptAgent Interaction History:", concept_agent.get_interaction_history("user123"))
