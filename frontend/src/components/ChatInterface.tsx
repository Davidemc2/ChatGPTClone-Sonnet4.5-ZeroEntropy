/**
 * Chat Interface - The main chat component
 * 
 * Design Philosophy:
 * - Clean, minimal message layout
 * - Smooth animations and transitions
 * - Intuitive message input
 * - Entropy visualization for Zero Entropy system
 * - Apple-inspired visual hierarchy
 */

import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { useChat } from '../context/ChatContext';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import EntropyIndicator from './EntropyIndicator';
import WelcomeScreen from './WelcomeScreen';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px); /* Subtract header height */
  background-color: ${props => props.theme.colors.background};
  position: relative;
  overflow: hidden;
`;

const MessagesContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
`;

const ChatContent = styled.div`
  max-width: ${props => props.theme.components.chat.maxWidth};
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0 ${props => props.theme.spacing.lg};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    padding: 0 ${props => props.theme.spacing.md};
  }
`;

const InputContainer = styled.div`
  background-color: ${props => props.theme.colors.background};
  border-top: 1px solid ${props => props.theme.colors.borderLight};
  padding: ${props => props.theme.spacing.md} 0;
  backdrop-filter: blur(20px);
  background-color: rgba(255, 255, 255, 0.9);
`;

const StatusBar = styled.div<{ show: boolean }>`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 32px;
  background: linear-gradient(135deg, ${props => props.theme.colors.primaryLight}, ${props => props.theme.colors.background});
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: ${props => props.theme.typography.sizes.sm};
  color: ${props => props.theme.colors.textSecondary};
  transform: translateY(${props => props.show ? '0' : '-100%'});
  transition: ${props => props.theme.transitions.default};
  z-index: 10;
  border-bottom: 1px solid ${props => props.theme.colors.borderLight};
`;

const LoadingIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.textSecondary};
  font-size: ${props => props.theme.typography.sizes.sm};
  
  &::before {
    content: '';
    width: 16px;
    height: 16px;
    border: 2px solid ${props => props.theme.colors.border};
    border-top: 2px solid ${props => props.theme.colors.primary};
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: ${props => props.theme.spacing.sm};
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const ErrorMessage = styled.div`
  background-color: ${props => props.theme.colors.error}10;
  border: 1px solid ${props => props.theme.colors.error}30;
  border-radius: ${props => props.theme.borderRadius.md};
  padding: ${props => props.theme.spacing.md};
  margin: ${props => props.theme.spacing.md} 0;
  color: ${props => props.theme.colors.error};
  font-size: ${props => props.theme.typography.sizes.sm};
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  
  &::before {
    content: '⚠️';
  }
`;

const ChatInterface: React.FC = () => {
  const { state, actions } = useChat();
  const [showStatusBar, setShowStatusBar] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Load system status on mount
    actions.loadSystemStatus();
  }, [actions]);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    scrollToBottom();
  }, [state.messages]);

  useEffect(() => {
    // Show status bar briefly when system status changes
    if (state.systemStatus) {
      setShowStatusBar(true);
      const timer = setTimeout(() => setShowStatusBar(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [state.systemStatus]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'end'
    });
  };

  const handleSendMessage = async (message: string) => {
    await actions.sendMessage(message);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    // Add keyboard shortcuts
    if (e.metaKey || e.ctrlKey) {
      switch (e.key) {
        case 'k':
          e.preventDefault();
          // Focus message input
          const input = document.querySelector('textarea') as HTMLTextAreaElement;
          input?.focus();
          break;
        case 'n':
          e.preventDefault();
          actions.createNewConversation();
          break;
      }
    }
  };

  // Calculate average entropy for current conversation
  const getAverageEntropy = () => {
    const messagesWithEntropy = state.messages.filter(
      msg => msg.entropy_metrics && msg.role === 'assistant'
    );
    
    if (messagesWithEntropy.length === 0) return null;
    
    const totalEntropy = messagesWithEntropy.reduce(
      (sum, msg) => sum + (msg.entropy_metrics?.shannon_entropy || 0), 0
    );
    
    return totalEntropy / messagesWithEntropy.length;
  };

  const averageEntropy = getAverageEntropy();

  return (
    <ChatContainer onKeyDown={handleKeyPress}>
      <StatusBar show={showStatusBar}>
        {state.systemStatus && (
          <>
            System Status: {state.systemStatus.status} • 
            RAG: {state.systemStatus.rag_engine_status} • 
            Documents: {state.systemStatus.total_documents}
          </>
        )}
      </StatusBar>

      <MessagesContainer>
        <ChatContent>
          {state.messages.length === 0 ? (
            <WelcomeScreen onStartChat={actions.createNewConversation} />
          ) : (
            <>
              <MessageList 
                messages={state.messages}
                showEntropyMetrics={state.settings.showEntropyMetrics}
              />
              <div ref={messagesEndRef} />
            </>
          )}
          
          {state.isLoading && (
            <LoadingIndicator>
              Zero Entropy is thinking...
            </LoadingIndicator>
          )}
          
          {state.error && (
            <ErrorMessage>
              {state.error}
            </ErrorMessage>
          )}
        </ChatContent>
      </MessagesContainer>

      <InputContainer>
        <ChatContent>
          <MessageInput
            onSendMessage={handleSendMessage}
            disabled={state.isLoading}
            placeholder={
              state.messages.length === 0
                ? "Start a conversation with Zero Entropy..."
                : "Type your message..."
            }
          />
          
          {averageEntropy !== null && state.settings.showEntropyMetrics && (
            <EntropyIndicator 
              entropy={averageEntropy}
              style={{ marginTop: '8px' }}
            />
          )}
        </ChatContent>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatInterface;