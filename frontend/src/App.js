import React, { useState } from 'react';
import { askQuestion } from './api';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userMsg = { role: 'user', text: question };
    setChatHistory((prev) => [...prev, userMsg]);

    const res = await askQuestion(question);
    const botMsg = { role: 'bot', text: res.answer };
    setChatHistory((prev) => [...prev, botMsg]);

    setQuestion('');
  };

  return (
    <div className="app">
      <h1>⚖️ AI Legal Assistant Chatbot</h1>
      <div className="chat-box">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          placeholder="Ask a legal question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit">Ask</button>
      </form>
    </div>
  );
}

export default App;
