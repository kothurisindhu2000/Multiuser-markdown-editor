# Multiuser Markdown Editor App

## 📌 Project Overview

This project is a real-time collaborative markdown editor built using Python and WebSockets.

The goal of this project is to simulate how multiple users can edit the same document at the same time, while keeping everything synchronized across different clients.

It also includes a simple offline-first mechanism, where user inputs are temporarily saved and later synced when the connection is restored.

---

## 🎯 Why this project was built

In real-world applications like Google Docs or Notion, multiple users can work on the same document simultaneously.

This project was created to understand:

- How real-time communication works
- How multiple users stay in sync
- How to handle basic offline scenarios
- How backend systems manage shared state (documents)

---

## ⚙️ How it works

### 1. Server (server.py)

- Runs a WebSocket server on ws://localhost:8765
- Keeps track of all connected users
- Stores the shared document in memory
- When a user sends a message:
  - It updates the main document
  - Broadcasts the updated document to all users

---

### 2. Client (main.py)

Each client:

- Connects to the WebSocket server
- Takes user input from terminal
- Sends messages to the server
- Receives updated document in real-time
- Displays the shared document on screen

---

### 3. Shared Document (document.md)

- Acts as the local copy of the shared document
- Gets updated whenever new content is received from the server

---

### 4. Offline Support (queue.json)

If connection fails:

- Messages are saved locally in queue.json
- Once reconnected, these messages can be sent again

This simulates a basic offline-first sync mechanism

---

## ✨ Features

- 👥 Multi-user real-time collaboration
- 🔄 Live document synchronization
- 📡 WebSocket-based communication
- 💾 Local document persistence (document.md)
- 📥 Offline message queue (queue.json)
- ⚡ Asynchronous programming using asyncio

---

## 🛠️ Tech Stack

- Python
- asyncio
- websockets library

---

## ▶️ How to Run

### Step 1: Install dependencies

bash pip install -r requirements.txt 

### Step 2: Start the server

bash python server.py 

### Step 3: Run multiple clients

Open multiple terminals:

bash python main.py 

Enter different usernames to simulate multiple users.

---

## 🧠 What we learned

- Basics of WebSocket communication
- Handling multiple clients concurrently
- Managing shared state across users
- Implementing a simple offline-first system
- Understanding real-time collaboration concepts

---

## ⚠️ Limitations

- No advanced conflict resolution (CRDT not fully implemented)
- Terminal-based UI (no graphical interface)
- Offline sync is basic and manual
- No authentication system

---

## 🚀 Future Improvements

- Implement proper CRDT-based conflict resolution
- Build a web-based UI (React / HTML)
- Add user authentication
- Improve offline sync with auto-retry
- Add rich markdown editing features

---

## 📎 Conclusion

This project demonstrates the core idea behind collaborative editing systems.

While simplified, it provides a strong foundation for understanding how real-world tools like Google Docs work internally.
