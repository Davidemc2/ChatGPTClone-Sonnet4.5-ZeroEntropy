import React from 'react';
import { Plus, MessageSquare, Trash2, X } from 'lucide-react';
import './Sidebar.css';
import { deleteSession } from '../services/api';

const Sidebar = ({ 
  sessions, 
  currentSessionId, 
  onNewChat, 
  onSelectSession, 
  onDeleteSession,
  isOpen,
  onToggle 
}) => {
  const handleDelete = async (e, sessionId) => {
    e.stopPropagation();
    
    if (window.confirm('Delete this conversation?')) {
      try {
        await deleteSession(sessionId);
        onDeleteSession(sessionId);
      } catch (error) {
        console.error('Error deleting session:', error);
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const getSessionPreview = (session) => {
    if (session.messages && session.messages.length > 0) {
      const lastUserMessage = session.messages
        .filter(m => m.role === 'user')
        .pop();
      
      if (lastUserMessage) {
        return lastUserMessage.content.slice(0, 50) + 
               (lastUserMessage.content.length > 50 ? '...' : '');
      }
    }
    return 'New conversation';
  };

  return (
    <>
      <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <button className="new-chat-button" onClick={onNewChat}>
            <Plus size={18} />
            <span>New Chat</span>
          </button>
          
          <button className="close-sidebar-button" onClick={onToggle}>
            <X size={18} />
          </button>
        </div>

        <div className="sessions-list">
          {sessions.length === 0 ? (
            <div className="empty-sessions">
              <MessageSquare size={32} className="empty-icon" />
              <p>No conversations yet</p>
              <p className="empty-subtitle">Start a new chat to begin</p>
            </div>
          ) : (
            sessions.map(session => (
              <div
                key={session.id}
                className={`session-item ${currentSessionId === session.id ? 'active' : ''}`}
                onClick={() => onSelectSession(session.id)}
              >
                <div className="session-icon">
                  <MessageSquare size={16} />
                </div>
                
                <div className="session-info">
                  <div className="session-preview">
                    {getSessionPreview(session)}
                  </div>
                  <div className="session-date">
                    {formatDate(session.updated_at || session.created_at)}
                  </div>
                </div>

                <button
                  className="delete-session-button"
                  onClick={(e) => handleDelete(e, session.id)}
                  title="Delete conversation"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))
          )}
        </div>

        <div className="sidebar-footer">
          <div className="footer-info">
            <p className="footer-title">Zero Entropy</p>
            <p className="footer-subtitle">First Principles • RAG Enhanced</p>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="sidebar-overlay" onClick={onToggle}></div>
      )}
    </>
  );
};

export default Sidebar;
