import React from 'react'
import { useChatStore } from '../store/chatStore'

const Header = ({ onMenuClick, isConnected }) => {
  const { newSession, toggleRAG, settings } = useChatStore()

  return (
    <header className="bg-dark-surface border-b border-dark-border px-4 py-3">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center space-x-4">
          <button
            onClick={onMenuClick}
            className="p-2 hover:bg-dark-hover rounded-lg transition-colors lg:hidden"
          >
            <svg 
              className="w-6 h-6" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M4 6h16M4 12h16M4 18h16" 
              />
            </svg>
          </button>
          
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">ZE</span>
            </div>
            <div>
              <h1 className="text-lg font-semibold">Zero Entropy ChatGPT</h1>
              <p className="text-xs text-gray-400">Enhanced with RAG</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* RAG Toggle */}
          <button
            onClick={toggleRAG}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              settings.useRAG 
                ? 'bg-green-600 text-white' 
                : 'bg-dark-hover text-gray-400'
            }`}
            title="Toggle RAG system"
          >
            RAG {settings.useRAG ? 'ON' : 'OFF'}
          </button>

          {/* New Chat Button */}
          <button
            onClick={newSession}
            className="px-3 py-1.5 bg-primary hover:bg-primary-hover text-white rounded-lg text-sm font-medium transition-colors"
          >
            New Chat
          </button>

          {/* Status Indicator */}
          <div className={`w-2 h-2 rounded-full ${
            isConnected ? 'bg-green-500' : 'bg-red-500'
          }`} title={isConnected ? 'Connected' : 'Disconnected'} />
        </div>
      </div>
    </header>
  )
}

export default Header
