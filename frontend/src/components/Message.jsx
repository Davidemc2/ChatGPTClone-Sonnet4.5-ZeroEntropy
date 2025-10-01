import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { User, Bot, Loader } from 'lucide-react';
import './Message.css';

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  const isLoading = message.isLoading;

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className="message-avatar">
        {isUser ? (
          <User size={20} />
        ) : (
          <Bot size={20} />
        )}
      </div>

      <div className="message-content">
        {isLoading ? (
          <div className="message-loading">
            <Loader size={16} className="spinner" />
            <span>Thinking...</span>
          </div>
        ) : (
          <>
            {isUser ? (
              <div className="message-text user-text">
                {message.content}
              </div>
            ) : (
              <div className="message-text assistant-text">
                <ReactMarkdown
                  components={{
                    code({ node, inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '');
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
                      );
                    },
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}

            {message.metadata && message.metadata.rag_used && (
              <div className="message-metadata">
                <span className="metadata-badge">
                  RAG Enhanced • {message.metadata.context_length} context items
                </span>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Message;
