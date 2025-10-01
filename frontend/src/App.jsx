import React, { useState, useEffect, useRef } from 'react'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import { useChatStore } from './store/chatStore'

function App() {
  const [ws, setWs] = useState(null)
  const [isConnected, setIsConnected] = useState(false)
  const messagesEndRef = useRef(null)
  const { messages, sessionId, addMessage, updateLastMessage, setSessionId, settings } = useChatStore()

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.hostname}:8000/ws/chat/${sessionId}`
      
      const socket = new WebSocket(wsUrl)

      socket.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
      }

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        if (data.type === 'chunk') {
          updateLastMessage(data.content)
        } else if (data.type === 'complete') {
          // Message is complete
          scrollToBottom()
        }
      }

      socket.onerror = (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      }

      socket.onclose = () => {
        console.log('WebSocket disconnected')
        setIsConnected(false)
        // Attempt to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000)
      }

      setWs(socket)
    }

    if (sessionId) {
      connectWebSocket()
    }

    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [sessionId])

  const handleSendMessage = (message) => {
    if (!message.trim() || !ws || !isConnected) return

    // Add user message
    addMessage({
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    })

    // Add placeholder for assistant message
    addMessage({
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
      isStreaming: true
    })

    // Send message via WebSocket
    ws.send(JSON.stringify({
      message: message,
      use_rag: settings.useRAG
    }))
  }

  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen bg-dark-bg text-gray-100">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <Header 
          onMenuClick={() => setSidebarOpen(!sidebarOpen)} 
          isConnected={isConnected}
        />

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.length === 0 ? (
              <div className="text-center mt-20">
                <div className="inline-block p-6 bg-dark-surface rounded-2xl border border-dark-border">
                  <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    Zero Entropy ChatGPT
                  </h1>
                  <p className="text-gray-400 mb-6">
                    Enhanced with RAG system for minimal information loss
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
                    <div className="p-4 bg-dark-bg rounded-lg">
                      <div className="text-xl mb-2">🎯</div>
                      <h3 className="font-semibold mb-1">First Principles</h3>
                      <p className="text-sm text-gray-400">
                        Break down complex problems to fundamental truths
                      </p>
                    </div>
                    <div className="p-4 bg-dark-bg rounded-lg">
                      <div className="text-xl mb-2">🧠</div>
                      <h3 className="font-semibold mb-1">Enhanced Memory</h3>
                      <p className="text-sm text-gray-400">
                        RAG-powered context retrieval system
                      </p>
                    </div>
                    <div className="p-4 bg-dark-bg rounded-lg">
                      <div className="text-xl mb-2">⚡</div>
                      <h3 className="font-semibold mb-1">Zero Entropy</h3>
                      <p className="text-sm text-gray-400">
                        Minimal information loss, maximum accuracy
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input area */}
        <div className="border-t border-dark-border bg-dark-surface">
          <div className="max-w-3xl mx-auto p-4">
            <ChatInput 
              onSend={handleSendMessage} 
              disabled={!isConnected}
            />
            <div className="text-xs text-center text-gray-500 mt-2">
              {isConnected ? (
                <span className="text-green-500">● Connected</span>
              ) : (
                <span className="text-red-500">● Disconnected</span>
              )}
              {' | '}
              RAG: {settings.useRAG ? 'ON' : 'OFF'}
              {' | '}
              Model: {settings.model}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
