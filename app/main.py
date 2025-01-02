from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.utils.redis_memory import RedisMemory
from app.utils.memory_trigger import MemoryTrigger
from app.agents.tech_agent import TechAgent
from app.agents.concept_agent import ConceptAgent
from app.agents.task_agent import TaskAgent
from typing import List

app = FastAPI()

# Memory and trigger setup
memory = RedisMemory()
trigger = MemoryTrigger(memory)

# Connection manager for WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Agent registry
agents = {}

def register_agent(agent_name: str, agent_instance):
    """Register an agent for command delegation."""
    agents[agent_name] = agent_instance

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time interaction."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            response = handle_message(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def handle_message(message: str) -> str:
    """
    Route commands to the correct agent.
    Message format: "agent_name:command:arg1,arg2"
    """
    try:
        parts = message.split(":")
        if len(parts) < 2:
            return "Invalid command format. Use 'agent_name:command:args'."
        agent_name, command = parts[0], parts[1]
        args = parts[2:] if len(parts) > 2 else []
        agent = agents.get(agent_name)
        if not agent:
            return f"Agent '{agent_name}' not found."
        return str(agent.parse_command(command, *args))
    except Exception as e:
        return f"Error handling message: {str(e)}"

# Initialize and register agents
tech_agent = TechAgent(memory)
concept_agent = ConceptAgent(memory)
task_agent = TaskAgent(memory)

register_agent("TechAgent", tech_agent)
register_agent("ConceptAgent", concept_agent)
register_agent("TaskAgent", task_agent)

# Start-up event for testing
@app.on_event("startup")
def startup_event():
    # Example: Populate memory with sample data
    memory.set("TechAgent:task:001", {"description": "Setup Redis", "deadline": "2025-01-03T10:00:00"})
    memory.append_to_list("TechAgent:tasks", {"task_id": "001", "details": {"description": "Setup Redis"}})
    memory.set("ConceptAgent:preferences:user123", {"theme": "dark", "notifications": "enabled"})
    memory.append_to_list("ConceptAgent:history:user123", {"action": "enable_dark_mode"})
    print("Sample data loaded into Redis memory.")
