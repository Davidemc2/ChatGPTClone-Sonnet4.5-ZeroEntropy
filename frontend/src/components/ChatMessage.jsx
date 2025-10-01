import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start space-x-3 max-w-2xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary' : 'bg-gradient-to-br from-purple-500 to-blue-500'
        }`}>
          <span className="text-white text-sm font-semibold">
            {isUser ? 'U' : 'AI'}
          </span>
        </div>

        {/* Message content */}
        <div className={`rounded-2xl px-4 py-3 ${
          isUser 
            ? 'bg-primary text-white' 
            : 'bg-dark-surface border border-dark-border'
        }`}>
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="markdown-content">
              <ReactMarkdown
                components={{
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '')
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        {...props}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    )
                  }
                }}
              >
                {message.content || (message.isStreaming ? '...' : '')}
              </ReactMarkdown>
              {message.isStreaming && message.content && (
                <span className="inline-block w-2 h-4 ml-1 bg-primary animate-pulse"></span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
