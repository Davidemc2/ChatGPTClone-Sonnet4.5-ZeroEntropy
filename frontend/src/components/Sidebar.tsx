/**
 * Sidebar - Navigation and conversation management
 * 
 * Features:
 * - Conversation list
 * - Settings panel
 * - Apple-inspired slide animation
 * - Clean, minimal design
 */

import React, { useState } from 'react';
import styled from 'styled-components';
import { useChat } from '../context/ChatContext';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const SidebarOverlay = styled.div<{ isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  opacity: ${props => props.isOpen ? 1 : 0};
  visibility: ${props => props.isOpen ? 'visible' : 'hidden'};
  transition: ${props => props.theme.transitions.default};
  z-index: 200;
  
  @media (min-width: ${props => props.theme.breakpoints.tablet}) {
    display: none;
  }
`;

const SidebarContainer = styled.aside<{ isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  width: ${props => props.theme.components.sidebar.width};
  height: 100vh;
  background-color: ${props => props.theme.components.sidebar.background};
  border-right: 1px solid ${props => props.theme.colors.borderLight};
  transform: translateX(${props => props.isOpen ? '0' : '-100%'});
  transition: ${props => props.theme.transitions.slow};
  z-index: 300;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  
  @media (min-width: ${props => props.theme.breakpoints.tablet}) {
    position: relative;
    transform: none;
    width: ${props => props.isOpen ? props.theme.components.sidebar.width : '0'};
    border-right: ${props => props.isOpen ? '1px solid ' + props.theme.colors.borderLight : 'none'};
  }
`;

const SidebarHeader = styled.div`
  padding: ${props => props.theme.spacing.lg};
  border-bottom: 1px solid ${props => props.theme.colors.borderLight};
`;

const SidebarTitle = styled.h2`
  font-size: ${props => props.theme.typography.sizes.lg};
  font-weight: ${props => props.theme.typography.weights.semibold};
  color: ${props => props.theme.colors.text};
  margin: 0 0 ${props => props.theme.spacing.sm} 0;
`;

const SidebarSubtitle = styled.p`
  font-size: ${props => props.theme.typography.sizes.sm};
  color: ${props => props.theme.colors.textSecondary};
  margin: 0;
`;

const SidebarContent = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${props => props.theme.spacing.md};
`;

const Section = styled.div`
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const SectionTitle = styled.h3`
  font-size: ${props => props.theme.typography.sizes.sm};
  font-weight: ${props => props.theme.typography.weights.semibold};
  color: ${props => props.theme.colors.textSecondary};
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 ${props => props.theme.spacing.sm} 0;
`;

const ConversationList = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xs};
`;

const ConversationItem = styled.div<{ isActive: boolean }>`
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.md};
  cursor: pointer;
  transition: ${props => props.theme.transitions.default};
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  background-color: ${props => 
    props.isActive 
      ? props.theme.colors.primary + '15'
      : 'transparent'
  };
  
  border: 1px solid ${props => 
    props.isActive 
      ? props.theme.colors.primary + '30'
      : 'transparent'
  };
  
  &:hover {
    background-color: ${props => 
      props.isActive 
        ? props.theme.colors.primary + '20'
        : props.theme.colors.backgroundSecondary
    };
  }
`;

const ConversationTitle = styled.div`
  font-size: ${props => props.theme.typography.sizes.sm};
  font-weight: ${props => props.theme.typography.weights.medium};
  color: ${props => props.theme.colors.text};
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
`;

const ConversationMeta = styled.div`
  font-size: ${props => props.theme.typography.sizes.xs};
  color: ${props => props.theme.colors.textTertiary};
  margin-top: 2px;
`;

const DeleteButton = styled.button`
  width: 24px;
  height: 24px;
  border: none;
  background: none;
  color: ${props => props.theme.colors.textTertiary};
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: ${props => props.theme.transitions.default};
  
  ${ConversationItem}:hover & {
    opacity: 1;
  }
  
  &:hover {
    background-color: ${props => props.theme.colors.error + '20'};
    color: ${props => props.theme.colors.error};
  }
`;

const SettingsSection = styled.div`
  border-top: 1px solid ${props => props.theme.colors.borderLight};
  padding-top: ${props => props.theme.spacing.md};
`;

const SettingItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${props => props.theme.spacing.sm} 0;
`;

const SettingLabel = styled.label`
  font-size: ${props => props.theme.typography.sizes.sm};
  color: ${props => props.theme.colors.text};
  cursor: pointer;
`;

const ToggleSwitch = styled.input`
  appearance: none;
  width: 44px;
  height: 24px;
  background-color: ${props => props.theme.colors.backgroundSecondary};
  border-radius: 12px;
  position: relative;
  cursor: pointer;
  outline: none;
  transition: ${props => props.theme.transitions.default};
  
  &:checked {
    background-color: ${props => props.theme.colors.primary};
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 20px;
    height: 20px;
    background-color: white;
    border-radius: 50%;
    transition: ${props => props.theme.transitions.default};
    transform: ${props => props.checked ? 'translateX(20px)' : 'translateX(0)'};
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: ${props => props.theme.spacing.xl} ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.textSecondary};
`;

const EmptyStateIcon = styled.div`
  font-size: 48px;
  margin-bottom: ${props => props.theme.spacing.md};
  opacity: 0.5;
`;

const EmptyStateText = styled.p`
  font-size: ${props => props.theme.typography.sizes.sm};
  line-height: ${props => props.theme.typography.lineHeights.relaxed};
  margin: 0;
`;

const NewChatButton = styled.button`
  width: 100%;
  padding: ${props => props.theme.spacing.md};
  border: 2px dashed ${props => props.theme.colors.border};
  background-color: transparent;
  color: ${props => props.theme.colors.textSecondary};
  border-radius: ${props => props.theme.borderRadius.md};
  font-size: ${props => props.theme.typography.sizes.sm};
  cursor: pointer;
  transition: ${props => props.theme.transitions.default};
  margin-bottom: ${props => props.theme.spacing.md};
  
  &:hover {
    border-color: ${props => props.theme.colors.primary};
    color: ${props => props.theme.colors.primary};
    background-color: ${props => props.theme.colors.primary}05;
  }
`;

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { state, actions } = useChat();
  const [activeTab, setActiveTab] = useState<'conversations' | 'settings'>('conversations');

  const handleConversationClick = (conversationId: string) => {
    actions.loadConversation(conversationId);
    onClose(); // Close sidebar on mobile after selection
  };

  const handleDeleteConversation = (conversationId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      actions.deleteConversation(conversationId);
    }
  };

  const handleNewChat = () => {
    actions.createNewConversation();
    onClose();
  };

  const handleSettingChange = (setting: string, value: boolean) => {
    actions.updateSettings({ [setting]: value });
  };

  const getConversationTitle = (conversation: any) => {
    if (conversation.messages && conversation.messages.length > 0) {
      const firstUserMessage = conversation.messages.find((msg: any) => msg.role === 'user');
      return firstUserMessage ? firstUserMessage.content.slice(0, 50) : 'New Chat';
    }
    return 'New Chat';
  };

  return (
    <>
      <SidebarOverlay isOpen={isOpen} onClick={onClose} />
      <SidebarContainer isOpen={isOpen}>
        <SidebarHeader>
          <SidebarTitle>Chat History</SidebarTitle>
          <SidebarSubtitle>Manage your conversations</SidebarSubtitle>
        </SidebarHeader>

        <SidebarContent>
          <NewChatButton onClick={handleNewChat}>
            + Start New Conversation
          </NewChatButton>

          <Section>
            <SectionTitle>Recent Conversations</SectionTitle>
            
            {state.conversations.length === 0 ? (
              <EmptyState>
                <EmptyStateIcon>💬</EmptyStateIcon>
                <EmptyStateText>
                  No conversations yet.<br />
                  Start chatting to see your history here.
                </EmptyStateText>
              </EmptyState>
            ) : (
              <ConversationList>
                {state.conversations.map((conversation) => (
                  <ConversationItem
                    key={conversation.id}
                    isActive={state.currentConversationId === conversation.id}
                    onClick={() => handleConversationClick(conversation.id)}
                  >
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <ConversationTitle>
                        {getConversationTitle(conversation)}
                      </ConversationTitle>
                      <ConversationMeta>
                        {new Intl.DateTimeFormat('en-US', {
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        }).format(new Date(conversation.updated_at))}
                      </ConversationMeta>
                    </div>
                    
                    <DeleteButton
                      onClick={(e) => handleDeleteConversation(conversation.id, e)}
                      title="Delete conversation"
                    >
                      🗑
                    </DeleteButton>
                  </ConversationItem>
                ))}
              </ConversationList>
            )}
          </Section>

          <SettingsSection>
            <SectionTitle>Settings</SectionTitle>
            
            <SettingItem>
              <SettingLabel htmlFor="rag-toggle">
                Enhanced RAG Mode
              </SettingLabel>
              <ToggleSwitch
                id="rag-toggle"
                type="checkbox"
                checked={state.settings.useRAG}
                onChange={(e) => handleSettingChange('useRAG', e.target.checked)}
              />
            </SettingItem>
            
            <SettingItem>
              <SettingLabel htmlFor="entropy-toggle">
                Show Entropy Metrics
              </SettingLabel>
              <ToggleSwitch
                id="entropy-toggle"
                type="checkbox"
                checked={state.settings.showEntropyMetrics}
                onChange={(e) => handleSettingChange('showEntropyMetrics', e.target.checked)}
              />
            </SettingItem>
          </SettingsSection>
        </SidebarContent>
      </SidebarContainer>
    </>
  );
};

export default Sidebar;

