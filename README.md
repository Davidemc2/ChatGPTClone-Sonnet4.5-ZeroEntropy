# Zero Entropy ChatGPT Clone

A fully functional ChatGPT clone enhanced with a **Retrieval-Augmented Generation (RAG)** system, built on Zero Entropy principles for minimal information loss and maximum accuracy.

## 🎯 Philosophy

This project follows three key methodologies:

### 1. **Zero Entropy Principles**
- **Minimal Information Loss**: Precise, accurate responses without degradation
- **Deterministic Retrieval**: Consistent results for similar queries
- **Optimal State**: Perfect coherence between context and response
- **Efficient Storage**: Dense vector representations for knowledge compression

### 2. **First Principles Thinking (Elon Musk)**
- Break down complex problems to fundamental truths
- Build solutions from the ground up
- Challenge assumptions and reason from basics
- Focus on what's physically/logically possible

### 3. **Unix/Linux Philosophy**
- Modularity: Each component does one thing well
- Simplicity: Clean, maintainable code
- Composability: Components work together seamlessly
- Transparency: Clear, understandable architecture

## 🚀 Features

- **Real-time Streaming Chat**: WebSocket-based streaming responses
- **RAG System**: Vector database-powered context retrieval
- **Persistent Memory**: Conversation history with semantic search
- **Modern UI**: Beautiful, responsive React interface
- **Session Management**: Multiple conversation sessions
- **Knowledge Base**: Add custom documents to enhance responses
- **Configurable**: Adjustable model, temperature, and RAG settings

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Frontend (React)               │
│  - Modern UI with Tailwind CSS                  │
│  - WebSocket streaming                          │
│  - State management with Zustand                │
└────────────────┬────────────────────────────────┘
                 │ WebSocket + REST API
┌────────────────┴────────────────────────────────┐
│              Backend (FastAPI)                  │
│  - RESTful API endpoints                        │
│  - WebSocket support                            │
│  - Async request handling                       │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────┐
│              RAG Engine (LangChain)             │
│  - Query processing                             │
│  - Context retrieval                            │
│  - Response generation                          │
└────────┬───────────────────────┬────────────────┘
         │                       │
┌────────┴────────┐    ┌────────┴─────────┐
│  Vector Store   │    │  Memory Manager  │
│  (ChromaDB)     │    │  (JSON + Vector) │
│  - Embeddings   │    │  - Sessions      │
│  - Similarity   │    │  - History       │
│  - RAG Context  │    │  - Persistence   │
└─────────────────┘    └──────────────────┘
```

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **OpenAI API Key** (or Anthropic API Key)

## 🛠️ Installation

### Quick Start

```bash
# 1. Clone or navigate to the project directory
cd /workspace

# 2. Run the setup script
chmod +x setup.sh
./setup.sh

# 3. Configure your API keys
nano .env  # Edit and add your OPENAI_API_KEY

# 4. Start the application
chmod +x run.sh
./run.sh
```

### Manual Installation

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Create necessary directories
mkdir -p data/chroma data/sessions

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

## 🎮 Usage

### Starting the Application

```bash
./run.sh
```

This will start:
- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### Using the Chat Interface

1. Open http://localhost:3000 in your browser
2. Start typing your message
3. Press Enter or click Send
4. Watch responses stream in real-time

### Adding Knowledge to RAG System

```bash
# Using Python
python3 << EOF
from core import ZeroEntropyVectorStore

vector_store = ZeroEntropyVectorStore()
vector_store.add_documents([
    "Your custom knowledge here...",
    "More information to enhance responses..."
])
EOF
```

Or use the API:

```bash
curl -X POST http://localhost:8000/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{
    "documents": ["Your knowledge here..."],
    "metadata": [{"source": "custom"}]
  }'
```

## 📁 Project Structure

```
/workspace
├── api/                    # FastAPI backend
│   ├── main.py            # Main API application
│   └── __init__.py
├── core/                   # Core business logic
│   ├── vector_store.py    # ChromaDB vector store
│   ├── memory_manager.py  # Conversation memory
│   ├── rag_engine.py      # RAG implementation
│   └── __init__.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── store/         # State management
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── package.json
│   └── vite.config.js
├── data/                   # Data storage
│   ├── chroma/            # Vector database
│   └── sessions/          # Session files
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── setup.sh              # Setup script
├── run.sh                # Run script
└── README.md             # This file
```

## 🔧 Configuration

Edit `.env` to configure:

```bash
# API Keys
OPENAI_API_KEY=your_key_here

# Model Settings
DEFAULT_MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=4096

# RAG Configuration
TOP_K_RESULTS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Server
HOST=0.0.0.0
PORT=8000
```

## 🔌 API Endpoints

### Chat
- `POST /chat` - Send a message (non-streaming)
- `WebSocket /ws/chat/{session_id}` - Real-time streaming chat

### Knowledge Base
- `POST /knowledge/add` - Add documents
- `POST /knowledge/search` - Search knowledge base

### Sessions
- `GET /sessions` - List all sessions
- `GET /sessions/{session_id}` - Get session details
- `DELETE /sessions/{session_id}` - Delete session
- `POST /sessions/{session_id}/search` - Search session history

### System
- `GET /` - System information
- `GET /health` - Health check

## 🧪 Testing

### Test the Backend

```bash
# Health check
curl http://localhost:8000/health

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is first principles thinking?"}'
```

### Test the Frontend

Simply open http://localhost:3000 and start chatting!

## 🎨 Features in Detail

### RAG System
- **Semantic Search**: Uses embeddings for intelligent document retrieval
- **Chunking**: Splits large documents into manageable pieces
- **Metadata Filtering**: Filter retrievals by type, session, or custom metadata
- **Relevance Scoring**: Returns documents with similarity scores

### Memory Management
- **Sliding Window**: Maintains recent conversation context
- **Persistent Storage**: Saves conversations to disk
- **Semantic Memory**: Search through past conversations
- **Session Isolation**: Each session maintains separate memory

### UI/UX
- **Dark Theme**: Easy on the eyes
- **Markdown Support**: Rich text formatting
- **Code Highlighting**: Syntax highlighting for code blocks
- **Responsive Design**: Works on desktop and mobile
- **Real-time Streaming**: See responses as they're generated

## 🔐 Security Notes

- Never commit `.env` with real API keys
- Use environment variables for sensitive data
- Configure CORS appropriately for production
- Implement rate limiting for production deployments
- Add authentication for multi-user scenarios

## 🚀 Deployment

### Docker (Recommended)

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Build and run
docker build -t zero-entropy-chat .
docker run -p 8000:8000 --env-file .env zero-entropy-chat
```

### Production Considerations

- Use a process manager (PM2, systemd)
- Set up reverse proxy (nginx)
- Enable HTTPS
- Configure proper logging
- Set up monitoring
- Implement backups for vector database

## 🤝 Contributing

This project follows first principles thinking and Unix philosophy:
- Keep it simple
- Make it modular
- Test thoroughly
- Document clearly

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- **Zero Entropy Principles**: Information theory and thermodynamics
- **Elon Musk**: First principles thinking methodology
- **Linux Philosophy**: Modular, composable design
- **OpenAI**: GPT models and API
- **LangChain**: RAG framework
- **ChromaDB**: Vector database

## 📞 Support

For issues, questions, or contributions:
1. Check the documentation above
2. Review the code comments
3. Test with simple examples first
4. Apply first principles thinking to debug

---

**Built with passion, powered by first principles. 🚀**
