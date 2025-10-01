/**
 * Chat Context - Global state management for chat functionality
 * 
 * Manages:
 * - Chat messages and conversations
 * - System status and entropy metrics
 * - API communication with Zero Entropy backend
 * - User preferences and settings
 */

import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Types
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  entropy_metrics?: {
    shannon_entropy: number;
    certainty_score: number;
    semantic_coherence: number;
    overall_quality: number;
  };
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  created_at: Date;
  updated_at: Date;
  entropy_status: string;
}

export interface SystemStatus {
  status: string;
  rag_engine_status: string;
  vector_store_status: string;
  total_documents: number;
  entropy_metrics: {
    entropy_threshold: number;
    confidence_threshold: number;
    system_entropy: number;
  };
}

interface ChatState {
  conversations: Conversation[];
  currentConversationId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  systemStatus: SystemStatus | null;
  settings: {
    useRAG: boolean;
    showEntropyMetrics: boolean;
    theme: 'light' | 'dark';
  };
}

type ChatAction =
  | { type: 'SET_CONVERSATIONS'; payload: Conversation[] }
  | { type: 'SET_CURRENT_CONVERSATION'; payload: string }
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'SET_MESSAGES'; payload: ChatMessage[] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_SYSTEM_STATUS'; payload: SystemStatus }
  | { type: 'UPDATE_SETTINGS'; payload: Partial<ChatState['settings']> }
  | { type: 'CREATE_CONVERSATION'; payload: Conversation }
  | { type: 'DELETE_CONVERSATION'; payload: string }
  | { type: 'CLEAR_MESSAGES' };

const initialState: ChatState = {
  conversations: [],
  currentConversationId: null,
  messages: [],
  isLoading: false,
  error: null,
  systemStatus: null,
  settings: {
    useRAG: true,
    showEntropyMetrics: true,
    theme: 'light',
  },
};

// Reducer
const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'SET_CONVERSATIONS':
      return {
        ...state,
        conversations: action.payload,
      };

    case 'SET_CURRENT_CONVERSATION':
      return {
        ...state,
        currentConversationId: action.payload,
      };

    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.payload],
      };

    case 'SET_MESSAGES':
      return {
        ...state,
        messages: action.payload,
      };

    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };

    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };

    case 'SET_SYSTEM_STATUS':
      return {
        ...state,
        systemStatus: action.payload,
      };

    case 'UPDATE_SETTINGS':
      return {
        ...state,
        settings: {
          ...state.settings,
          ...action.payload,
        },
      };

    case 'CREATE_CONVERSATION':
      return {
        ...state,
        conversations: [action.payload, ...state.conversations],
        currentConversationId: action.payload.id,
        messages: action.payload.messages,
      };

    case 'DELETE_CONVERSATION':
      const updatedConversations = state.conversations.filter(
        conv => conv.id !== action.payload
      );
      const shouldResetCurrent = state.currentConversationId === action.payload;
      
      return {
        ...state,
        conversations: updatedConversations,
        currentConversationId: shouldResetCurrent ? null : state.currentConversationId,
        messages: shouldResetCurrent ? [] : state.messages,
      };

    case 'CLEAR_MESSAGES':
      return {
        ...state,
        messages: [],
      };

    default:
      return state;
  }
};

// Context
const ChatContext = createContext<{
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
  actions: {
    sendMessage: (message: string) => Promise<void>;
    createNewConversation: () => void;
    loadConversation: (conversationId: string) => Promise<void>;
    deleteConversation: (conversationId: string) => Promise<void>;
    loadSystemStatus: () => Promise<void>;
    updateSettings: (settings: Partial<ChatState['settings']>) => void;
  };
} | null>(null);

// Provider
export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // API base URL
  const API_BASE = 'http://localhost:8000/api/v1';

  // Actions
  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    dispatch({ type: 'ADD_MESSAGE', payload: userMessage });

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          conversation_id: state.currentConversationId,
          use_rag: state.settings.useRAG,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: `assistant_${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(data.timestamp),
        entropy_metrics: data.entropy_metrics,
      };
      dispatch({ type: 'ADD_MESSAGE', payload: assistantMessage });

      // Update current conversation ID if it's new
      if (!state.currentConversationId) {
        dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: data.conversation_id });
      }

    } catch (error) {
      console.error('Error sending message:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to send message' });
      
      // Add error message
      const errorMessage: ChatMessage = {
        id: `error_${Date.now()}`,
        role: 'system',
        content: 'Sorry, I encountered an error processing your message. Please try again.',
        timestamp: new Date(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: errorMessage });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const createNewConversation = () => {
    const newConversation: Conversation = {
      id: `conv_${Date.now()}`,
      title: 'New Chat',
      messages: [],
      created_at: new Date(),
      updated_at: new Date(),
      entropy_status: 'optimal',
    };

    dispatch({ type: 'CREATE_CONVERSATION', payload: newConversation });
  };

  const loadConversation = async (conversationId: string) => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const response = await fetch(`${API_BASE}/conversation/${conversationId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: conversationId });
      dispatch({ type: 'SET_MESSAGES', payload: data.messages });
      
    } catch (error) {
      console.error('Error loading conversation:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to load conversation' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const deleteConversation = async (conversationId: string) => {
    try {
      const response = await fetch(`${API_BASE}/conversation/${conversationId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        dispatch({ type: 'DELETE_CONVERSATION', payload: conversationId });
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to delete conversation' });
    }
  };

  const loadSystemStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/system/status`);
      
      if (response.ok) {
        const data = await response.json();
        dispatch({ type: 'SET_SYSTEM_STATUS', payload: data });
      }
    } catch (error) {
      console.error('Error loading system status:', error);
    }
  };

  const updateSettings = (settings: Partial<ChatState['settings']>) => {
    dispatch({ type: 'UPDATE_SETTINGS', payload: settings });
  };

  const actions = {
    sendMessage,
    createNewConversation,
    loadConversation,
    deleteConversation,
    loadSystemStatus,
    updateSettings,
  };

  return (
    <ChatContext.Provider value={{ state, dispatch, actions }}>
      {children}
    </ChatContext.Provider>
  );
};

// Hook
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export default ChatContext;