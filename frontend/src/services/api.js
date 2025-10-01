/**
 * API Service - Zero Entropy ChatGPT Clone
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}

// Chat endpoints
export async function sendMessage(sessionId, message, options = {}) {
  return apiCall('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
      stream: false,
      use_rag: options.useRag !== false,
      temperature: options.temperature,
      max_tokens: options.maxTokens,
    }),
  });
}

export async function getChatHistory(sessionId) {
  return apiCall(`/api/chat/history/${sessionId}`);
}

export async function clearChatHistory(sessionId) {
  return apiCall(`/api/chat/history/${sessionId}`, {
    method: 'DELETE',
  });
}

// Session endpoints
export async function listSessions() {
  return apiCall('/api/sessions');
}

export async function createSession(metadata = null) {
  return apiCall('/api/sessions', {
    method: 'POST',
    body: JSON.stringify({ metadata }),
  });
}

export async function getSession(sessionId) {
  return apiCall(`/api/sessions/${sessionId}`);
}

export async function deleteSession(sessionId) {
  return apiCall(`/api/sessions/${sessionId}`, {
    method: 'DELETE',
  });
}

// Memory/RAG endpoints
export async function addKnowledge(content, metadata = null, category = 'general') {
  return apiCall('/api/memory/add', {
    method: 'POST',
    body: JSON.stringify({
      content,
      metadata,
      category,
    }),
  });
}

export async function searchMemory(query, nResults = 5, filterBy = null) {
  return apiCall('/api/memory/search', {
    method: 'POST',
    body: JSON.stringify({
      query,
      n_results: nResults,
      filter_by: filterBy,
    }),
  });
}

export async function getMemoryStats() {
  return apiCall('/api/memory/stats');
}

export async function clearMemory() {
  return apiCall('/api/memory/clear', {
    method: 'DELETE',
  });
}

// Health check
export async function healthCheck() {
  return apiCall('/health');
}
