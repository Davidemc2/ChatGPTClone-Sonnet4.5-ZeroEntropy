import React from 'react';
import { Menu, Brain } from 'lucide-react';
import './Header.css';

const Header = ({ onToggleSidebar, sidebarOpen }) => {
  return (
    <header className="header">
      <div className="header-left">
        <button 
          className="icon-button"
          onClick={onToggleSidebar}
          title={sidebarOpen ? "Close sidebar" : "Open sidebar"}
        >
          <Menu size={20} />
        </button>
        
        <div className="header-logo">
          <Brain size={24} className="logo-icon" />
          <h1 className="header-title">Zero Entropy Chat</h1>
        </div>
      </div>
      
      <div className="header-right">
        <div className="status-badge">
          <span className="status-dot"></span>
          <span className="status-text">RAG Enhanced</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
