import React from 'react'
import { useChatStore } from '../store/chatStore'

const Sidebar = ({ isOpen, onClose }) => {
  const { settings, updateSettings } = useChatStore()

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-64 bg-dark-surface border-r border-dark-border
        transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        flex flex-col
      `}>
        {/* Sidebar Header */}
        <div className="p-4 border-b border-dark-border flex items-center justify-between">
          <h2 className="text-lg font-semibold">Settings</h2>
          <button
            onClick={onClose}
            className="lg:hidden p-1 hover:bg-dark-hover rounded"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Settings Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {/* Model Settings */}
          <div>
            <h3 className="text-sm font-semibold mb-3 text-gray-400">Model</h3>
            <select
              value={settings.model}
              onChange={(e) => updateSettings({ model: e.target.value })}
              className="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-4-turbo">GPT-4 Turbo</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            </select>
          </div>

          {/* Temperature */}
          <div>
            <h3 className="text-sm font-semibold mb-3 text-gray-400">
              Temperature: {settings.temperature}
            </h3>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={settings.temperature}
              onChange={(e) => updateSettings({ temperature: parseFloat(e.target.value) })}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Precise</span>
              <span>Creative</span>
            </div>
          </div>

          {/* RAG Settings */}
          <div>
            <h3 className="text-sm font-semibold mb-3 text-gray-400">RAG System</h3>
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.useRAG}
                onChange={(e) => updateSettings({ useRAG: e.target.checked })}
                className="w-4 h-4 text-primary bg-dark-bg border-dark-border rounded focus:ring-primary"
              />
              <span className="text-sm">Enable RAG retrieval</span>
            </label>
            <p className="text-xs text-gray-500 mt-2">
              Retrieval-Augmented Generation enhances responses with relevant context from the knowledge base.
            </p>
          </div>

          {/* Information */}
          <div className="pt-6 border-t border-dark-border">
            <h3 className="text-sm font-semibold mb-3 text-gray-400">About</h3>
            <div className="space-y-2 text-sm text-gray-400">
              <p>
                <strong className="text-white">Zero Entropy</strong> principles ensure minimal information loss and maximum accuracy.
              </p>
              <ul className="list-disc list-inside space-y-1 text-xs">
                <li>First principles thinking</li>
                <li>Deterministic retrieval</li>
                <li>Context optimization</li>
                <li>Persistent memory</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-dark-border text-xs text-gray-500 text-center">
          Zero Entropy ChatGPT v1.0.0
          <br />
          Built with React + FastAPI
        </div>
      </div>
    </>
  )
}

export default Sidebar
