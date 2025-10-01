import React, { useState, useRef, useEffect } from 'react'

const ChatInput = ({ onSend, disabled }) => {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSend(message)
      setMessage('')
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
    }
  }, [message])

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-end space-x-2">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={disabled ? "Connecting..." : "Type your message... (Shift+Enter for new line)"}
            disabled={disabled}
            className="w-full px-4 py-3 pr-12 bg-dark-bg border border-dark-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary resize-none max-h-40 disabled:opacity-50 disabled:cursor-not-allowed"
            rows={1}
          />
          <div className="absolute right-2 bottom-2 text-xs text-gray-500">
            {message.length > 0 && `${message.length} chars`}
          </div>
        </div>
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="px-6 py-3 bg-primary hover:bg-primary-hover text-white rounded-xl font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <span>Send</span>
          <svg 
            className="w-5 h-5" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" 
            />
          </svg>
        </button>
      </div>
    </form>
  )
}

export default ChatInput
