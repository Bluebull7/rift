import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemText,
  LinearProgress,
  Snackbar,
} from "@mui/material";
import { Bar } from "react-chartjs-2";
import useWebSocket from "react-use-websocket";

function App() {
  const [tasks, setTasks] = useState([]);
  const [logs, setLogs] = useState([]);
  const [input, setInput] = useState("");
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [socketUrl] = useState("ws://localhost:8000/ws");
  const { sendMessage, lastMessage } = useWebSocket(socketUrl, {
    onOpen: () => console.log("Connected to WebSocket"),
    onMessage: (message) => handleWebSocketMessage(message),
    onError: (error) => console.error("WebSocket error:", error),
  });

  useEffect(() => {
    if (lastMessage) {
      const data = JSON.parse(lastMessage.data || "{}");

      if (data.task_id) {
        setTasks((prev) => [
          ...prev.filter((t) => t.task_id !== data.task_id),
          data,
        ]);
      } else if (data.log) {
        setLogs((prev) => [data.log, ...prev]);
      }
    }
  }, [lastMessage]);

  const handleWebSocketMessage = (message) => {
    console.log("Received message:", message);
  };

  const handleSendCommand = () => {
    if (input) {
      sendMessage(input);
      setInput("");
      setSnackbarMessage("Command sent successfully!");
      setSnackbarOpen(true);
    }
  };

  const handleLogin = async () => {
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (response.ok) {
      setIsLoggedIn(true);
    } else {
      alert("Invalid credentials");
    }
  };

  if (!isLoggedIn) {
    return (
      <Box sx={{ padding: 2 }}>
        <Typography variant="h4">Login</Typography>
        <TextField
          label="Username"
          fullWidth
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          sx={{ marginBottom: 2 }}
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{ marginBottom: 2 }}
        />
        <Button variant="contained" onClick={handleLogin}>
          Login
        </Button>
      </Box>
    );
  }

  const taskData = {
    labels: ["Completed", "In Progress"],
    datasets: [
      {
        label: "Tasks",
        data: [
          tasks.filter((t) => t.status === "completed").length,
          tasks.filter((t) => t.status !== "completed").length,
        ],
        backgroundColor: ["green", "orange"],
      },
    ],
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        Agent Dashboard
      </Typography>
      <Grid container spacing={2}>
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
                  {task.status === "completed" ? (
                    <Typography color="green">Completed</Typography>
                  ) : (
                    <LinearProgress sx={{ width: "100%" }} />
                  )}
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
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
      <Paper elevation={3} sx={{ padding: 2, marginTop: 2 }}>
        <Typography variant="h6">Task Metrics</Typography>
        <Bar data={taskData} />
      </Paper>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        message={snackbarMessage}
      />
    </Box>
  );
}

export default App;
