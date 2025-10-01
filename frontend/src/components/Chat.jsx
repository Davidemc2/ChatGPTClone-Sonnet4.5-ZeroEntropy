import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader, AlertCircle } from 'lucide-react';
import './Chat.css';
import Message from './Message';
import { sendMessage, getChatHistory } from '../services/api';

const Chat = ({ sessionId, onNewSession }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Load chat history when session changes
  useEffect(() => {
    if (sessionId) {
      loadHistory();
    } else {
      setMessages([]);
    }
  }, [sessionId]);

  // Auto-scroll to bottom
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadHistory = async () => {
    try {
      const data = await getChatHistory(sessionId);
      setMessages(data.messages || []);
      setError(null);
    } catch (err) {
      console.error('Error loading history:', err);
      setMessages([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setError(null);

    // Add user message immediately
    const tempUserMessage = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMessage]);

    // Add temporary loading message
    const loadingMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
      isLoading: true
    };
    setMessages(prev => [...prev, loadingMessage]);

    setLoading(true);

    try {
      const response = await sendMessage(sessionId, userMessage);
      
      // Remove loading message and add real response
      setMessages(prev => {
        const filtered = prev.filter(m => !m.isLoading);
        return [
          ...filtered,
          {
            role: 'assistant',
            content: response.message,
            timestamp: new Date().toISOString(),
            metadata: response.metadata
          }
        ];
      });

    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');
      
      // Remove loading message
      setMessages(prev => prev.filter(m => !m.isLoading));
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-container">
      {!sessionId ? (
        <div className="chat-empty">
          <div className="empty-content">
            <h2>Zero Entropy Chat</h2>
            <p>Advanced AI chat with RAG-enhanced memory</p>
            <button className="start-chat-button" onClick={onNewSession}>
              Start New Conversation
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="messages-empty">
                <h3>Start a conversation</h3>
                <p>Ask me anything. I have access to enhanced memory and context.</p>
              </div>
            ) : (
              <>
                {messages.map((message, index) => (
                  <Message 
                    key={index} 
                    message={message}
                  />
                ))}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          <div className="input-container">
            {error && (
              <div className="error-banner">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}
            
            <form onSubmit={handleSubmit} className="input-form">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Send a message..."
                className="message-input"
                rows="1"
                disabled={loading}
              />
              
              <button
                type="submit"
                className="send-button"
                disabled={loading || !input.trim()}
              >
                {loading ? (
                  <Loader size={20} className="spinner" />
                ) : (
                  <Send size={20} />
                )}
              </button>
            </form>

            <div className="input-footer">
              <span className="footer-text">
                Enhanced with Zero Entropy RAG • Press Enter to send, Shift+Enter for new line
              </span>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Chat;
