/**
 * Message Input - Elegant chat input with Apple-inspired design
 * 
 * Features:
 * - Auto-resizing textarea
 * - Smooth animations
 * - Keyboard shortcuts
 * - Send button with haptic feedback feel
 */

import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

const InputContainer = styled.div`
  display: flex;
  align-items: flex-end;
  gap: ${props => props.theme.spacing.sm};
  background-color: ${props => props.theme.colors.background};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius.xl};
  padding: ${props => props.theme.spacing.sm};
  transition: ${props => props.theme.transitions.default};
  
  &:focus-within {
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => props.theme.colors.primary}20;
  }
`;

const TextArea = styled.textarea`
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  background: none;
  font-family: ${props => props.theme.typography.primary};
  font-size: ${props => props.theme.typography.sizes.base};
  line-height: ${props => props.theme.typography.lineHeights.normal};
  color: ${props => props.theme.colors.text};
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.sm};
  min-height: 24px;
  max-height: 120px;
  overflow-y: auto;
  
  &::placeholder {
    color: ${props => props.theme.colors.textTertiary};
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  /* Custom scrollbar */
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
  
  &::-webkit-scrollbar-thumb {
    background: ${props => props.theme.colors.border};
    border-radius: 3px;
  }
`;

const SendButton = styled.button<{ hasContent: boolean }>`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: ${props => props.theme.borderRadius.full};
  background-color: ${props => 
    props.hasContent 
      ? props.theme.colors.primary 
      : props.theme.colors.backgroundSecondary
  };
  color: ${props => 
    props.hasContent 
      ? props.theme.colors.textInverse 
      : props.theme.colors.textTertiary
  };
  cursor: ${props => props.hasContent ? 'pointer' : 'not-allowed'};
  transition: ${props => props.theme.transitions.default};
  font-size: 18px;
  flex-shrink: 0;
  
  &:hover {
    transform: ${props => props.hasContent ? 'translateY(-1px)' : 'none'};
    background-color: ${props => 
      props.hasContent 
        ? props.theme.colors.primaryHover 
        : props.theme.colors.backgroundSecondary
    };
    box-shadow: ${props => 
      props.hasContent 
        ? props.theme.shadows.md 
        : 'none'
    };
  }
  
  &:active {
    transform: ${props => props.hasContent ? 'translateY(0)' : 'none'};
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const CharacterCount = styled.div<{ show: boolean; nearLimit: boolean }>`
  position: absolute;
  bottom: -24px;
  right: 8px;
  font-size: ${props => props.theme.typography.sizes.xs};
  color: ${props => 
    props.nearLimit 
      ? props.theme.colors.warning
      : props.theme.colors.textTertiary
  };
  opacity: ${props => props.show ? 1 : 0};
  transition: ${props => props.theme.transitions.default};
`;

const InputWrapper = styled.div`
  position: relative;
  width: 100%;
`;

const ShortcutHint = styled.div<{ show: boolean }>`
  position: absolute;
  bottom: -20px;
  left: 12px;
  font-size: ${props => props.theme.typography.sizes.xs};
  color: ${props => props.theme.colors.textTertiary};
  opacity: ${props => props.show ? 1 : 0};
  transition: ${props => props.theme.transitions.default};
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
`;

const KeyCap = styled.span`
  background-color: ${props => props.theme.colors.backgroundSecondary};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 4px;
  padding: 2px 6px;
  font-family: ${props => props.theme.typography.monospace};
  font-size: ${props => props.theme.typography.sizes.xs};
`;

const MessageInput: React.FC<MessageInputProps> = ({ 
  onSendMessage, 
  disabled = false, 
  placeholder = "Type your message..." 
}) => {
  const [message, setMessage] = useState('');
  const [showShortcuts, setShowShortcuts] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const maxLength = 5000;

  useEffect(() => {
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSendMessage(trimmedMessage);
      setMessage('');
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        // Allow new line with Shift+Enter
        return;
      } else {
        e.preventDefault();
        handleSubmit();
      }
    }
    
    if (e.key === 'Escape') {
      setMessage('');
      textareaRef.current?.blur();
    }
  };

  const handleFocus = () => {
    setShowShortcuts(true);
  };

  const handleBlur = () => {
    // Delay hiding shortcuts to prevent flicker
    setTimeout(() => setShowShortcuts(false), 100);
  };

  const hasContent = message.trim().length > 0;
  const nearLimit = message.length > maxLength * 0.8;
  const showCharCount = message.length > maxLength * 0.7;

  return (
    <InputWrapper>
      <InputContainer>
        <TextArea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value.slice(0, maxLength))}
          onKeyDown={handleKeyDown}
          onFocus={handleFocus}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
        />
        
        <SendButton
          hasContent={hasContent}
          onClick={handleSubmit}
          disabled={disabled || !hasContent}
          title={hasContent ? "Send message (Enter)" : "Enter a message to send"}
        >
          {disabled ? '⏳' : '↗️'}
        </SendButton>
      </InputContainer>
      
      <CharacterCount 
        show={showCharCount} 
        nearLimit={nearLimit}
      >
        {message.length}/{maxLength}
      </CharacterCount>
      
      <ShortcutHint show={showShortcuts && !disabled}>
        <KeyCap>Enter</KeyCap> to send •
        <KeyCap>⇧</KeyCap><KeyCap>Enter</KeyCap> for new line •
        <KeyCap>Esc</KeyCap> to clear
      </ShortcutHint>
    </InputWrapper>
  );
};

export default MessageInput;

