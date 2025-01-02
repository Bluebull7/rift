from base_agent import BaseAgent
from memory_trigger import MemoryTrigger

class ConceptAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory, "ConceptAgent")
        self.trigger = MemoryTrigger(memory)

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
    
    def proactive_preference_suggestion(self):
        """Suggest updates to preferences based on repeated interactions."""
        interactions = self.memory.get_list(self.memory_key("history:user123"))
        if len(interactions) > 5 and all(interaction["action"] == "enable_dark_mode" for interaction in interactions):
            self.log("Suggestion: It seems you frequently enable dark mode. Would you like to set it as your default preference?")

    def proactive_anomaly_alert(self):
        """Detect and notify anomalies in preferences."""
        if self.trigger.check_anomaly(self.memory_key("preferences:user123"), {"theme": "dark", "notifications": "enabled"}):
            self.log("Alert: Your preferences have changed unexpectedly. Please verify your settings.")
