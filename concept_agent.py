from redis_memory import RedisMemory

class ConceptAgent:
    def __init__(self, memory: RedisMemory):
        self.memory = memory
        self.agent_id = "ConceptAgent"

    def save_preference(self, user_id, preference):
        self.memory.set(f"{self.agent_id}:preferences:{user_id}", preference)

    def get_preference(self, user_id):
        return self.memory.get(f"{self.agent_id}:preferences:{user_id}")

    def log_interaction(self, user_id, interaction):
        self.memory.append_to_list(f"{self.agent_id}:history:{user_id}", interaction)

    def get_interaction_history(self, user_id):
        return self.memory.get_list(f"{self.agent_id}:history:{user_id}")
