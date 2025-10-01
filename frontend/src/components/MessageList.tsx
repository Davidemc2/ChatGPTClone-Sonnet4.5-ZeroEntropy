/**
 * Message List - Displays chat messages with Apple-inspired design
 * 
 * Features:
 * - Clean message bubbles
 * - Entropy visualization
 * - Smooth animations
 * - Responsive design
 */

import React from 'react';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { ChatMessage } from '../context/ChatContext';
import EntropyIndicator from './EntropyIndicator';

interface MessageListProps {
  messages: ChatMessage[];
  showEntropyMetrics?: boolean;
}

const MessageListContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${props => props.theme.spacing.lg} 0;
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const MessageContainer = styled.div<{ role: string }>`
  display: flex;
  align-items: flex-start;
  gap: ${props => props.theme.spacing.sm};
  justify-content: ${props => props.role === 'user' ? 'flex-end' : 'flex-start'};
  animation: messageSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  @keyframes messageSlideIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const Avatar = styled.div<{ role: string }>`
  width: ${props => props.theme.components.chat.avatarSize};
  height: ${props => props.theme.components.chat.avatarSize};
  border-radius: ${props => props.theme.borderRadius.full};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: ${props => props.theme.typography.weights.medium};
  flex-shrink: 0;
  
  background-color: ${props => 
    props.role === 'user' 
      ? props.theme.colors.primary
      : props.role === 'assistant'
      ? props.theme.colors.backgroundTertiary
      : props.theme.colors.warning
  };
  
  color: ${props => 
    props.role === 'user' 
      ? props.theme.colors.textInverse
      : props.theme.colors.text
  };
`;

const MessageBubble = styled.div<{ role: string }>`
  max-width: 70%;
  min-width: 100px;
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.lg};
  border-radius: ${props => props.theme.borderRadius.lg};
  position: relative;
  
  background-color: ${props => 
    props.role === 'user' 
      ? props.theme.colors.primary
      : props.role === 'assistant'
      ? props.theme.colors.assistantMessage
      : props.theme.colors.systemMessage
  };
  
  color: ${props => 
    props.role === 'user' 
      ? props.theme.colors.textInverse
      : props.theme.colors.text
  };
  
  border: ${props => 
    props.role === 'assistant' 
      ? `1px solid ${props.theme.colors.border}`
      : 'none'
  };
  
  box-shadow: ${props => 
    props.role === 'user'
      ? props.theme.shadows.sm
      : 'none'
  };
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    max-width: 85%;
  }
`;

const MessageContent = styled.div`
  font-size: ${props => props.theme.typography.sizes.base};
  line-height: ${props => props.theme.typography.lineHeights.relaxed};
  
  /* Markdown styling */
  h1, h2, h3, h4, h5, h6 {
    margin: ${props => props.theme.spacing.sm} 0;
    font-weight: ${props => props.theme.typography.weights.semibold};
  }
  
  p {
    margin: ${props => props.theme.spacing.sm} 0;
    
    &:first-child {
      margin-top: 0;
    }
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  ul, ol {
    margin: ${props => props.theme.spacing.sm} 0;
    padding-left: ${props => props.theme.spacing.lg};
  }
  
  li {
    margin: ${props => props.theme.spacing.xs} 0;
  }
  
  blockquote {
    margin: ${props => props.theme.spacing.md} 0;
    padding-left: ${props => props.theme.spacing.md};
    border-left: 3px solid ${props => props.theme.colors.border};
    color: ${props => props.theme.colors.textSecondary};
    font-style: italic;
  }
  
  code {
    background-color: ${props => props.theme.colors.backgroundSecondary};
    padding: 2px 4px;
    border-radius: 4px;
    font-family: ${props => props.theme.typography.monospace};
    font-size: 14px;
  }
`;

const MessageMeta = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xs};
  margin-top: ${props => props.theme.spacing.sm};
`;

const MessageTime = styled.div`
  font-size: ${props => props.theme.typography.sizes.xs};
  color: ${props => props.theme.colors.textTertiary};
  opacity: 0.7;
`;

const EntropyWrapper = styled.div`
  margin-top: ${props => props.theme.spacing.xs};
`;

const CodeBlock = styled(SyntaxHighlighter)`
  margin: ${props => props.theme.spacing.sm} 0 !important;
  border-radius: ${props => props.theme.borderRadius.md} !important;
  font-size: 14px !important;
  
  & > code {
    background: none !important;
    padding: 0 !important;
  }
`;

const MessageList: React.FC<MessageListProps> = ({ messages, showEntropyMetrics = false }) => {
  const getAvatarContent = (role: string) => {
    switch (role) {
      case 'user':
        return '👤';
      case 'assistant':
        return '🤖';
      case 'system':
        return '⚙️';
      default:
        return '?';
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }).format(timestamp);
  };

  const renderCodeBlock = ({ node, inline, className, children, ...props }: any) => {
    const match = /language-(\w+)/.exec(className || '');
    return !inline && match ? (
      <CodeBlock
        style={tomorrow}
        language={match[1]}
        PreTag="div"
        {...props}
      >
        {String(children).replace(/\n$/, '')}
      </CodeBlock>
    ) : (
      <code className={className} {...props}>
        {children}
      </code>
    );
  };

  if (messages.length === 0) {
    return null;
  }

  return (
    <MessageListContainer>
      {messages.map((message) => (
        <MessageContainer key={message.id} role={message.role}>
          {message.role !== 'user' && (
            <Avatar role={message.role}>
              {getAvatarContent(message.role)}
            </Avatar>
          )}
          
          <div style={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
            <MessageBubble role={message.role}>
              <MessageContent>
                <ReactMarkdown
                  components={{
                    code: renderCodeBlock
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </MessageContent>
              
              <MessageMeta>
                <MessageTime>
                  {formatTimestamp(message.timestamp)}
                </MessageTime>
                
                {showEntropyMetrics && 
                 message.entropy_metrics && 
                 message.role === 'assistant' && (
                  <EntropyWrapper>
                    <EntropyIndicator 
                      entropy={message.entropy_metrics.shannon_entropy}
                      quality={message.entropy_metrics.overall_quality}
                      compact={true}
                    />
                  </EntropyWrapper>
                )}
              </MessageMeta>
            </MessageBubble>
          </div>
          
          {message.role === 'user' && (
            <Avatar role={message.role}>
              {getAvatarContent(message.role)}
            </Avatar>
          )}
        </MessageContainer>
      ))}
    </MessageListContainer>
  );
};

export default MessageList;