import re
import json

class QueryProcessor:
    
    def __init__(self, agents):
        self.agents = agents

    def process_query(self, query: str) -> str:
        """
        Process a natural language query and route it to the correct agent.
        """
        # Define patterns for commands
        patterns = [
            (r"analyze data for task (\d+) with data: (.+)", "TechAgent", "analyze_data"),
            (r"generate a narrative for task (\d+)", "ConceptAgent", "generate_narrative"),
            (r"check progress for task (\d+)", "TaskAgent", "track_progress")
        ]

        # Match query to a pattern
        for pattern, agent_name, command in patterns:
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                agent = self.agents.get(agent_name)
                if not agent:
                    return f"Agent '{agent_name}' not found."
                
                args = [json.loads(arg) if arg.startswith("[") or arg.startswith("{") else arg for arg in match.groups()]
                return agent.parse_command(command, *args)

        return "Sorry, I didn't understand your query. Please try again."
