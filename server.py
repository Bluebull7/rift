from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List
from redis_memory import RedisMemory  # Use the RedisMemory class from previous examples

app = FastAPI()

# Manage connected clients
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            response = handle_message(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Redis memory (for state management)
memory = RedisMemory()

# Define agent registry
agents = {}

def register_agent(agent_name, agent_instance):
    agents[agent_name] = agent_instance

# Message routing system
def handle_message(message: str) -> str:
    """
    Route commands to the correct agent based on the incoming message format.
    Example format: "agent_name:command:arg1,arg2"
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
