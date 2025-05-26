import React, { useState, useEffect } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

const ChatApp = () => {
  const [username, setUsername] = useState("");
  const [room, setRoom] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const userId = localStorage.getItem("user_id");
  const joinRoom = () => {
    if (username && room) {
      socket.emit("join", {
        user_id: userId,
        username,
        room,
      });
    }
  };

  const sendMessage = () => {
    if (message) {
      socket.emit("send_message", {
        user_id: userId,
        username,
        msg: message,
        room,
      });
      setMessage("");
    }
  };

  useEffect(() => {
    socket.on("message", (data) => {
      setMessages((prev) => [...prev, data]);
    });

    return () => socket.off("message");
  }, []);

  return (
    <div className="chat-container" style={styles.container}>
      <div style={styles.top}>
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={styles.input}
        />
        <input
          placeholder="Room"
          value={room}
          onChange={(e) => setRoom(e.target.value)}
          style={styles.input}
        />
        <button onClick={joinRoom} style={styles.button}>
          Join
        </button>
      </div>

      <div style={styles.messages}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.messageWrapper,
              flexDirection: msg.user === username ? "row-reverse" : "row",
            }}
          >
            <img
              src={msg.profilePic || "https://i.pravatar.cc/150?u=" + msg.user}
              alt="avatar"
              style={styles.avatar}
            />
            <div
              style={{
                ...styles.messageBubble,
                backgroundColor: msg.user === username ? "#DCF8C6" : "#FFF",
                alignItems: msg.user === username ? "flex-end" : "flex-start",
              }}
            >
              <div style={styles.name}>{msg.user}</div>
              <div>{msg.msg}</div>
            </div>
          </div>
        ))}
      </div>

      <div style={styles.bottom}>
        <input
          placeholder="Message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: 600,
    margin: "40px auto",
    display: "flex",
    flexDirection: "column",
    gap: 10,
    fontFamily: "Arial",
  },
  top: {
    display: "flex",
    gap: 10,
  },
  bottom: {
    display: "flex",
    gap: 10,
  },
  input: {
    flex: 1,
    padding: 10,
    fontSize: 16,
  },
  button: {
    padding: "10px 20px",
    fontSize: 16,
  },
  messages: {
    height: 400,
    overflowY: "scroll",
    border: "1px solid #ccc",
    padding: 10,
    display: "flex",
    flexDirection: "column",
    gap: 10,
    backgroundColor: "#F8F8F8",
  },
  messageWrapper: {
    display: "flex",
    alignItems: "flex-start",
    gap: 10,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: "50%",
  },
  messageBubble: {
    maxWidth: "70%",
    padding: 10,
    borderRadius: 12,
    backgroundColor: "#EEE",
    display: "flex",
    flexDirection: "column",
  },
  name: {
    fontWeight: "bold",
    fontSize: 14,
    marginBottom: 5,
    color: "#555",
  },
};

export default ChatApp;
