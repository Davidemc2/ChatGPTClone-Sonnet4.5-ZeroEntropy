import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// Generate a unique session ID
const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

export const useChatStore = create(
  persist(
    (set, get) => ({
      // State
      messages: [],
      sessionId: generateSessionId(),
      sessions: [],
      settings: {
        useRAG: true,
        model: 'gpt-4',
        temperature: 0.7
      },

      // Actions
      addMessage: (message) => {
        set((state) => ({
          messages: [...state.messages, message]
        }))
      },

      updateLastMessage: (content) => {
        set((state) => {
          const messages = [...state.messages]
          if (messages.length > 0) {
            const lastMessage = messages[messages.length - 1]
            lastMessage.content += content
            lastMessage.isStreaming = true
          }
          return { messages }
        })
      },

      clearMessages: () => {
        set({ messages: [] })
      },

      setSessionId: (sessionId) => {
        set({ sessionId })
      },

      newSession: () => {
        const newSessionId = generateSessionId()
        set({ 
          sessionId: newSessionId,
          messages: []
        })
      },

      updateSettings: (newSettings) => {
        set((state) => ({
          settings: { ...state.settings, ...newSettings }
        }))
      },

      toggleRAG: () => {
        set((state) => ({
          settings: { ...state.settings, useRAG: !state.settings.useRAG }
        }))
      }
    }),
    {
      name: 'zero-entropy-chat-storage',
      partialize: (state) => ({
        sessionId: state.sessionId,
        settings: state.settings
      })
    }
  )
)
