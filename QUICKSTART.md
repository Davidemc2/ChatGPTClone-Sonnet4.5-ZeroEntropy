# Quick Start Guide

Get up and running with Zero Entropy ChatGPT Clone in 5 minutes.

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- OpenAI API key

## Installation (3 steps)

### 1. Run Setup Script

```bash
./setup.sh
```

This will:
- Check dependencies
- Install Python packages
- Install Node.js packages
- Create data directories
- Generate `.env` file

### 2. Configure API Key

Edit `.env` and add your OpenAI API key:

```bash
nano .env
```

Set this variable:
```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start the Application

```bash
./run.sh
```

That's it! Open http://localhost:3000 in your browser.

## First Steps

### 1. Chat Without RAG

Just start typing and chatting. The system works like ChatGPT.

### 2. Add Knowledge to RAG

```bash
python3 examples/add_knowledge.py
```

This adds Zero Entropy principles to the knowledge base.

### 3. Chat With RAG

Now ask questions about:
- Zero Entropy principles
- First principles thinking
- Unix philosophy
- RAG architecture

The system will retrieve relevant information and provide enhanced responses.

### 4. Test Programmatically

```bash
python3 examples/test_chat.py
```

This demonstrates the Python API.

## Common Tasks

### Add Custom Knowledge

```python
from core import ZeroEntropyVectorStore

vector_store = ZeroEntropyVectorStore()
vector_store.add_documents([
    "Your knowledge here...",
    "More information..."
])
```

### Toggle RAG On/Off

Click the "RAG ON/OFF" button in the header to compare responses with and without retrieval.

### Start New Conversation

Click "New Chat" button to start fresh.

### Change Settings

Click the menu icon (≡) to open the sidebar and adjust:
- Model (GPT-4, GPT-3.5, etc.)
- Temperature (0 = deterministic, 2 = creative)
- RAG settings

## API Usage

### REST API

```bash
# Send a message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Add knowledge
curl -X POST http://localhost:8000/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{"documents": ["Your knowledge"]}'

# Search knowledge
curl -X POST http://localhost:8000/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query": "search term"}'
```

### WebSocket (Streaming)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/session-id');

ws.onopen = () => {
  ws.send(JSON.stringify({
    message: "Hello!",
    use_rag: true
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'chunk') {
    console.log(data.content);
  }
};
```

## Troubleshooting

### "Module not found" error

```bash
pip3 install -r requirements.txt
```

### "WebSocket disconnected"

Check if the backend is running:
```bash
curl http://localhost:8000/health
```

### Frontend not loading

```bash
cd frontend
npm install
npm run dev
```

### API key error

Make sure `.env` contains valid `OPENAI_API_KEY`.

### Port already in use

Change ports in `.env`:
```
PORT=8001  # Backend
```

And in `frontend/vite.config.js`:
```javascript
server: {
  port: 3001  // Frontend
}
```

## Next Steps

1. **Read the Architecture**: See `ARCHITECTURE.md` for deep dive
2. **Customize**: Modify prompts in `core/rag_engine.py`
3. **Add Features**: Follow the modular structure
4. **Deploy**: Use Docker or docker-compose for production

## Resources

- Full README: `README.md`
- Architecture: `ARCHITECTURE.md`
- API Docs: http://localhost:8000/docs
- Examples: `examples/` directory

## Support

For issues:
1. Check error messages carefully
2. Verify all dependencies are installed
3. Ensure API keys are valid
4. Check the logs in terminal

---

**Happy chatting! 🚀**
