/**
 * Header - App header with Apple-inspired design
 * 
 * Features:
 * - Translucent background with backdrop blur
 * - Clean typography
 * - Sidebar toggle
 * - System status indicator
 */

import React from 'react';
import styled from 'styled-components';
import { useChat } from '../context/ChatContext';

interface HeaderProps {
  onToggleSidebar: () => void;
  sidebarOpen: boolean;
}

const HeaderContainer = styled.header`
  height: ${props => props.theme.components.header.height};
  background: ${props => props.theme.components.header.background};
  backdrop-filter: ${props => props.theme.components.header.backdropFilter};
  border-bottom: 1px solid ${props => props.theme.colors.borderLight};
  display: flex;
  align-items: center;
  justify-content: between;
  padding: 0 ${props => props.theme.spacing.lg};
  position: sticky;
  top: 0;
  z-index: 100;
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    padding: 0 ${props => props.theme.spacing.md};
  }
`;

const LeftSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.md};
`;

const SidebarToggle = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: none;
  border-radius: ${props => props.theme.borderRadius.md};
  cursor: pointer;
  color: ${props => props.theme.colors.textSecondary};
  transition: ${props => props.theme.transitions.default};
  
  &:hover {
    background-color: ${props => props.theme.colors.backgroundSecondary};
    color: ${props => props.theme.colors.text};
  }
  
  &:active {
    transform: scale(0.95);
  }
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  font-size: ${props => props.theme.typography.sizes.lg};
  font-weight: ${props => props.theme.typography.weights.semibold};
  color: ${props => props.theme.colors.text};
`;

const LogoIcon = styled.div`
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, ${props => props.theme.colors.primary}, ${props => props.theme.colors.primaryHover});
  border-radius: ${props => props.theme.borderRadius.md};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
`;

const Title = styled.h1`
  font-size: ${props => props.theme.typography.sizes.lg};
  font-weight: ${props => props.theme.typography.weights.medium};
  color: ${props => props.theme.colors.text};
  margin: 0;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: none;
  }
`;

const CenterSection = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
`;

const ConversationTitle = styled.div`
  font-size: ${props => props.theme.typography.sizes.base};
  font-weight: ${props => props.theme.typography.weights.medium};
  color: ${props => props.theme.colors.textSecondary};
  text-align: center;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: none;
  }
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
`;

const SystemStatus = styled.div<{ status: string }>`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: ${props => props.theme.borderRadius.full};
  font-size: ${props => props.theme.typography.sizes.sm};
  font-weight: ${props => props.theme.typography.weights.medium};
  
  background-color: ${props => {
    switch (props.status) {
      case 'healthy': return props.theme.colors.success + '20';
      case 'warning': return props.theme.colors.warning + '20';
      case 'error': return props.theme.colors.error + '20';
      default: return props.theme.colors.backgroundSecondary;
    }
  }};
  
  color: ${props => {
    switch (props.status) {
      case 'healthy': return props.theme.colors.success;
      case 'warning': return props.theme.colors.warning;
      case 'error': return props.theme.colors.error;
      default: return props.theme.colors.textSecondary;
    }
  }};
`;

const StatusDot = styled.div<{ status: string }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: ${props => {
    switch (props.status) {
      case 'healthy': return props.theme.colors.success;
      case 'warning': return props.theme.colors.warning;
      case 'error': return props.theme.colors.error;
      default: return props.theme.colors.textTertiary;
    }
  }};
  
  animation: ${props => props.status === 'healthy' ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
`;

const NewChatButton = styled.button`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border: 1px solid ${props => props.theme.colors.border};
  background-color: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  border-radius: ${props => props.theme.borderRadius.md};
  font-size: ${props => props.theme.typography.sizes.sm};
  font-weight: ${props => props.theme.typography.weights.medium};
  cursor: pointer;
  transition: ${props => props.theme.transitions.default};
  
  &:hover {
    background-color: ${props => props.theme.colors.backgroundSecondary};
    border-color: ${props => props.theme.colors.borderDark};
  }
  
  &:active {
    transform: scale(0.95);
  }
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    span {
      display: none;
    }
  }
`;

const Header: React.FC<HeaderProps> = ({ onToggleSidebar, sidebarOpen }) => {
  const { state, actions } = useChat();

  const handleNewChat = () => {
    actions.createNewConversation();
  };

  const getSystemStatus = () => {
    if (!state.systemStatus) return 'unknown';
    return state.systemStatus.status;
  };

  const getConversationTitle = () => {
    if (!state.currentConversationId || state.messages.length === 0) {
      return 'Zero Entropy Chat';
    }
    
    const firstMessage = state.messages.find(msg => msg.role === 'user');
    if (firstMessage) {
      return firstMessage.content.slice(0, 30) + (firstMessage.content.length > 30 ? '...' : '');
    }
    
    return 'Active Conversation';
  };

  return (
    <HeaderContainer>
      <LeftSection>
        <SidebarToggle 
          onClick={onToggleSidebar}
          title={sidebarOpen ? "Close sidebar" : "Open sidebar"}
        >
          {sidebarOpen ? '✕' : '☰'}
        </SidebarToggle>
        
        <Logo>
          <LogoIcon>∅</LogoIcon>
          <Title>Zero Entropy</Title>
        </Logo>
      </LeftSection>

      <CenterSection>
        <ConversationTitle>
          {getConversationTitle()}
        </ConversationTitle>
      </CenterSection>

      <RightSection>
        <SystemStatus status={getSystemStatus()}>
          <StatusDot status={getSystemStatus()} />
          <span>{getSystemStatus()}</span>
        </SystemStatus>
        
        <NewChatButton onClick={handleNewChat}>
          <span>➕</span>
          <span>New Chat</span>
        </NewChatButton>
      </RightSection>
    </HeaderContainer>
  );
};

export default Header;