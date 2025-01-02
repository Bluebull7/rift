from base_agent import BaseAgent

class ConceptAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "ConceptAgent")

    def save_preference(self, user_id, preference):
        self.memory.set(self.memory_key(f"preferences:{user_id}"), preference)
        self.log(f"Preference for user {user_id} saved.")

    def get_preference(self, user_id):
        return self.memory.get(self.memory_key(f"preferences:{user_id}"))

    def log_interaction(self, user_id, interaction):
        self.memory.append_to_list(self.memory_key(f"history:{user_id}"), interaction)
        self.log(f"Logged interaction for user {user_id}.")

    def get_interaction_history(self, user_id):
        return self.memory.get_list(self.memory_key(f"history:{user_id}"))

    def parse_command(self, command, *args, **kwargs):
        if command == "save_preference":
            self.save_preference(*args, **kwargs)
        elif command == "get_preference":
            return self.get_preference(*args, **kwargs)
        elif command == "log_interaction":
            self.log_interaction(*args, **kwargs)
        elif command == "get_interaction_history":
            return self.get_interaction_history(*args, **kwargs)
        else:
            self.log(f"Unknown command: {command}")
