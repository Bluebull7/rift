**# Rift

## Overview
Rift is a Redis-backed multi-agent collaboration system built with FastAPI and WebSocket. Rift features agents that share context and collaborate on tasks by leveraging Redis as shared memory. Each agent specializes in a specific function and interacts with others to complete workflows efficiently.

### Key Features
- **TechAgent**: Performs data analysis and stores results in Redis.
- **ConceptAgent**: Reads analysis results from Redis and generates narratives.
- **TaskAgent**: Tracks task progress and determines task completion.
- **WebSocket Interface**: Enables real-time communication with agents.
- **Redis Integration**: Acts as a shared memory layer for inter-agent collaboration.

---

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py           # Initializes the app module
│   ├── main.py               # FastAPI entry point and WebSocket logic
│   ├── agents/
│   │   ├── __init__.py       # Initializes the agents module
│   │   ├── base_agent.py     # Base class for all agents
│   │   ├── tech_agent.py     # TechAgent implementation
│   │   ├── concept_agent.py  # ConceptAgent implementation
│   │   ├── task_agent.py     # TaskAgent implementation
│   └── utils/
│       ├── __init__.py       # Initializes the utils module
│       ├── redis_memory.py   # RedisMemory class for shared memory
│       ├── query_processor.py # QueryProcessor for natural language queries
├── static/
│   └── index.html            # Frontend WebSocket client (optional)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation (this file)
```

---

## Setup Instructions

### Prerequisites
1. **Python 3.10+**
2. **Redis Server**
3. **`pip`** (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Bluebull7/rift
   cd rift
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Redis server:
   ```bash
   redis-server
   ```

5. Run the FastAPI server:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

6. Test the WebSocket connection using `websocat`:
   ```bash
   websocat ws://127.0.0.1:8000/ws
   ```

---

## Usage

### WebSocket Commands
Interact with the agents through the WebSocket interface:

#### Example Commands:
1. **Analyze Data (TechAgent)**:
   ```
   Analyze data for task 101 with data: ["data1", "data2", "data3"]
   ```

2. **Generate Narrative (ConceptAgent)**:
   ```
   Generate a narrative for task 101
   ```

3. **Track Progress (TaskAgent)**:
   ```
   Check progress for task 101
   ```

### Expected Responses:
- **TechAgent**:
  ```json
  {"task_id": "101", "summary": "Analyzed 3 items"}
  ```

- **ConceptAgent**:
  ```
  The analysis for task 101 concluded: Analyzed 3 items.
  ```

- **TaskAgent**:
  ```json
  {"task_id": "101", "status": "completed"}
  ```

---

## Redis Data Structures

### Agent-Specific Namespaces
- `TechAgent:analysis:<task_id>`: Stores analysis results.
- `ConceptAgent:narrative:<task_id>`: Stores generated narratives.
- `TaskAgent:progress:<task_id>`: Tracks task progress.

### Shared Context
- `shared:task_context:<task_id>`: Stores metadata for task-level collaboration.
  - Example fields:
    - `TechAgent_analysis`
    - `ConceptAgent_narrative`
- `shared:notifications`: Redis list for inter-agent notifications.

---

## Future Enhancements

1. **Notification System**:
   - Implement Redis Pub/Sub for real-time agent notifications.

2. **Advanced Analytics**:
   - Add agents for data visualization and reporting.

3. **Role-Based Access Control**:
   - Differentiate between admin and user roles for WebSocket interactions.

4. **Frontend Dashboard**:
   - Build a user-friendly frontend for interacting with agents.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments
- **FastAPI**: For the web framework.
- **Redis**: For shared memory.
- **websocat**: For WebSocket debugging.

---
**
