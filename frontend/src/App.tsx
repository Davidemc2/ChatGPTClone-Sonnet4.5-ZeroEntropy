/**
 * Zero Entropy ChatGPT Clone - Main Application
 * 
 * Design Philosophy (Johnny Ive's Apple):
 * - Ruthless simplicity: Only essential elements visible
 * - Intuitive interactions: Natural chat flow
 * - Emotional connection: Delightful, responsive UI
 * - Zero entropy: Clean, ordered interface design
 */

import React, { useState, useEffect } from 'react';
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import { ChatProvider } from './context/ChatContext';
import { theme } from './styles/theme';

const GlobalStyle = createGlobalStyle`
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.text};
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: ${props => props.theme.colors.backgroundSecondary};
  }

  ::-webkit-scrollbar-thumb {
    background: ${props => props.theme.colors.border};
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: ${props => props.theme.colors.textSecondary};
  }

  /* Selection color */
  ::selection {
    background-color: ${props => props.theme.colors.primary}20;
    color: ${props => props.theme.colors.primary};
  }
`;

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: ${props => props.theme.colors.background};
`;

const MainContent = styled.div<{ sidebarOpen: boolean }>`
  display: flex;
  flex-direction: column;
  flex: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-left: ${props => props.sidebarOpen ? '280px' : '0'};
  
  @media (max-width: 768px) {
    margin-left: 0;
  }
`;

const App: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [systemStatus, setSystemStatus] = useState<'loading' | 'ready' | 'error'>('loading');

  useEffect(() => {
    // Check system status on startup
    checkSystemStatus();
    
    // Close sidebar on mobile by default
    if (window.innerWidth <= 768) {
      setSidebarOpen(false);
    }
    
    // Handle window resize
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setSidebarOpen(false);
      }
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const checkSystemStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setSystemStatus('ready');
      } else {
        setSystemStatus('error');
      }
    } catch (error) {
      console.error('System status check failed:', error);
      setSystemStatus('error');
    }
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  if (systemStatus === 'loading') {
    return (
      <ThemeProvider theme={theme}>
        <GlobalStyle />
        <LoadingScreen>
          <LoadingSpinner />
          <LoadingText>Initializing Zero Entropy System...</LoadingText>
        </LoadingScreen>
      </ThemeProvider>
    );
  }

  if (systemStatus === 'error') {
    return (
      <ThemeProvider theme={theme}>
        <GlobalStyle />
        <ErrorScreen>
          <ErrorIcon>⚠️</ErrorIcon>
          <ErrorTitle>System Unavailable</ErrorTitle>
          <ErrorMessage>
            Unable to connect to the Zero Entropy backend.
            <br />Please ensure the server is running on localhost:8000
          </ErrorMessage>
          <RetryButton onClick={checkSystemStatus}>
            Retry Connection
          </RetryButton>
        </ErrorScreen>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <ChatProvider>
        <AppContainer>
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
          <MainContent sidebarOpen={sidebarOpen}>
            <Header onToggleSidebar={toggleSidebar} sidebarOpen={sidebarOpen} />
            <ChatInterface />
          </MainContent>
        </AppContainer>
      </ChatProvider>
    </ThemeProvider>
  );
};

// Loading Screen Components
const LoadingScreen = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: ${props => props.theme.colors.background};
`;

const LoadingSpinner = styled.div`
  width: 48px;
  height: 48px;
  border: 3px solid ${props => props.theme.colors.border};
  border-top: 3px solid ${props => props.theme.colors.primary};
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 24px;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const LoadingText = styled.div`
  font-size: 16px;
  font-weight: 500;
  color: ${props => props.theme.colors.textSecondary};
`;

// Error Screen Components
const ErrorScreen = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 40px;
  text-align: center;
  background-color: ${props => props.theme.colors.background};
`;

const ErrorIcon = styled.div`
  font-size: 64px;
  margin-bottom: 24px;
`;

const ErrorTitle = styled.h1`
  font-size: 24px;
  font-weight: 600;
  color: ${props => props.theme.colors.text};
  margin-bottom: 16px;
`;

const ErrorMessage = styled.p`
  font-size: 16px;
  color: ${props => props.theme.colors.textSecondary};
  line-height: 1.6;
  margin-bottom: 32px;
  max-width: 400px;
`;

const RetryButton = styled.button`
  padding: 12px 24px;
  background-color: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    background-color: ${props => props.theme.colors.primaryHover};
    transform: translateY(-1px);
  }

  &:active {
    transform: translateY(0);
  }
`;

export default App;

