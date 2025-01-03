import React, { useState, useEffect } from "react";
import { Box, Typography, TextField, Button, Grid, Paper, List, ListItem, ListItemText } from "@mui/material";
import useWebSocket from "react-use-websocket";

function App() {
  const [tasks, setTasks] = useState([]);
  const [logs, setLogs] = useState([]);
  const [input, setInput] = useState("");
  const [socketUrl] = useState("ws://localhost:8000/ws"); // WebSocket URL
  const { sendMessage, lastMessage } = useWebSocket(socketUrl, {
    onOpen: () => console.log("Connected to WebSocket"),
    onMessage: (message) => handleWebSocketMessage(message),
    onError: (error) => console.error("WebSocket error:", error),
  });

  // Handle incoming WebSocket messages
  const handleWebSocketMessage = (message) => {
    const data = JSON.parse(message.data || "{}");

    if (data.task_id) {
      // Update task progress
      setTasks((prev) => [...prev.filter((t) => t.task_id !== data.task_id), data]);
    } else if (data.log) {
      // Update logs
      setLogs((prev) => [data.log, ...prev]);
    }
  };

  // Handle form submission
  const handleSendCommand = () => {
    if (input) {
      sendMessage(input);
      setInput("");
    }
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        Agent Dashboard
      </Typography>
      <Grid container spacing={2}>
        {/* Task Progress */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Task Progress</Typography>
            <List>
              {tasks.map((task, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`Task ${task.task_id}`}
                    secondary={`Status: ${task.status || "In Progress"}`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Agent Logs */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Agent Logs</Typography>
            <List>
              {logs.map((log, index) => (
                <ListItem key={index}>
                  <ListItemText primary={log} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Command Input */}
      <Box sx={{ marginTop: 2 }}>
        <Paper elevation={3} sx={{ padding: 2 }}>
          <Typography variant="h6">Send Command</Typography>
          <TextField
            fullWidth
            variant="outlined"
            label="Command"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            sx={{ marginBottom: 2 }}
          />
          <Button variant="contained" color="primary" onClick={handleSendCommand}>
            Send
          </Button>
        </Paper>
      </Box>
    </Box>
  );
}

export default App;
