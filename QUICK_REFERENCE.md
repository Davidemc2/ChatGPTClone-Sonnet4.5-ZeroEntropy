# Zero Entropy ChatGPT Clone - Quick Reference

## 🚀 Quick Start Commands

### Docker (Recommended)
```bash
# Setup
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Start
docker-compose up -d

# Access
# Frontend: http://localhost
# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env   # Add API key
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## 📡 API Quick Reference

### Chat
```bash
# Send message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Continue conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID", "message": "Follow-up"}'
```

### Memory/RAG
```bash
# Add knowledge
curl -X POST http://localhost:8000/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{"content": "Important info", "category": "general"}'

# Search memory
curl -X POST http://localhost:8000/api/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "search term", "n_results": 5}'

# Get stats
curl http://localhost:8000/api/memory/stats
```

### Sessions
```bash
# List sessions
curl http://localhost:8000/api/sessions

# Get session
curl http://localhost:8000/api/sessions/SESSION_ID

# Delete session
curl -X DELETE http://localhost:8000/api/sessions/SESSION_ID
```

---

## 🐍 Python Quick Reference

### Basic Chat
```python
import requests

response = requests.post("http://localhost:8000/api/chat", json={
    "message": "What is RAG?",
    "use_rag": True
})

print(response.json()['message'])
```

### Add Knowledge
```python
requests.post("http://localhost:8000/api/memory/add", json={
    "content": "Your knowledge here",
    "category": "documentation",
    "metadata": {"topic": "custom", "importance": "high"}
})
```

### Search Memory
```python
response = requests.post("http://localhost:8000/api/memory/search", json={
    "query": "search term",
    "n_results": 5
})

for result in response.json()['results']:
    print(f"Score: {result['final_score']:.2f}")
    print(f"Content: {result['content'][:100]}...")
```

---

## ⚙️ Environment Variables

### Required
```bash
OPENAI_API_KEY=sk-...        # Your OpenAI API key
```

### Optional (with defaults)
```bash
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_RETRIEVAL_RESULTS=5
SIMILARITY_THRESHOLD=0.7
ENABLE_LONG_TERM_MEMORY=true
MAX_CONTEXT_MESSAGES=10
```

---

## 📁 Important Files

### Must Configure
- `.env` - API keys and configuration

### Documentation
- `README.md` - Main overview
- `SETUP.md` - Detailed installation
- `ARCHITECTURE.md` - Technical details
- `EXAMPLES.md` - Usage examples

### Scripts
- `quickstart.sh` - Automated setup
- `demo_knowledge.py` - Load demo data

### Configuration
- `docker-compose.yml` - Docker setup
- `requirements.txt` - Python packages
- `package.json` - Node packages

---

## 🎯 Common Tasks

### Reset Everything
```bash
# Stop services
docker-compose down

# Remove data
rm -rf data/

# Restart
docker-compose up -d
```

### Clear Memory Only
```bash
curl -X DELETE http://localhost:8000/api/memory/clear
```

### Load Demo Knowledge
```bash
python demo_knowledge.py
```

### View Logs
```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Manual
# Check terminal where services are running
```

### Update Code
```bash
# Stop services
docker-compose down

# Pull/update code
git pull  # or make changes

# Rebuild and restart
docker-compose up -d --build
```

---

## 🔧 Troubleshooting

### Backend won't start
- Check `.env` has `OPENAI_API_KEY`
- Verify Python 3.9+ installed
- Check port 8000 is free: `lsof -i :8000`

### Frontend won't start
- Check Node.js 18+ installed
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check port 3000 is free

### API connection failed
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in `main.py`
- Verify `REACT_APP_API_URL` in frontend `.env.local`

### Out of memory
- Reduce `MAX_CONTEXT_MESSAGES`
- Lower `MAX_RETRIEVAL_RESULTS`
- Use smaller embedding model
- Clear old ChromaDB data

### OpenAI errors
- Verify API key is correct
- Check account has credits
- Confirm model name is valid
- Check rate limits

---

## 📊 Performance Tips

### Faster Responses
```bash
MODEL_NAME=gpt-3.5-turbo      # Faster model
MAX_TOKENS=500                # Shorter responses
MAX_CONTEXT_MESSAGES=5        # Less context
```

### Better Quality
```bash
MODEL_NAME=gpt-4-turbo-preview  # Better model
TEMPERATURE=0.7                 # Balanced creativity
MAX_RETRIEVAL_RESULTS=7         # More context
```

### Production Settings
```bash
# Use environment-specific configs
# Enable logging
LOG_LEVEL=INFO

# Set appropriate limits
MAX_TOKENS=1500
MAX_CONTEXT_MESSAGES=10

# Optimize retrieval
SIMILARITY_THRESHOLD=0.8
MAX_RETRIEVAL_RESULTS=5
```

---

## 🌐 Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/chat` | POST | Send message |
| `/api/chat/stream` | POST | Stream response |
| `/api/chat/history/{id}` | GET | Get history |
| `/api/memory/add` | POST | Add knowledge |
| `/api/memory/search` | POST | Search memory |
| `/api/memory/stats` | GET | Get statistics |
| `/api/memory/clear` | DELETE | Clear memory |
| `/api/sessions` | GET | List sessions |
| `/api/sessions` | POST | Create session |
| `/api/sessions/{id}` | GET | Get session |
| `/api/sessions/{id}` | DELETE | Delete session |

Full API docs: http://localhost:8000/docs

---

## 📱 URLs

| Service | URL |
|---------|-----|
| Frontend (Docker) | http://localhost |
| Frontend (Manual) | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

## 🔐 Security Checklist

- [ ] Never commit `.env` file
- [ ] Use strong API keys
- [ ] Configure CORS properly
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Backup your data

---

## 📚 Learning Path

1. **Start**: Read `README.md`
2. **Setup**: Follow `SETUP.md`
3. **Use**: Try `EXAMPLES.md`
4. **Understand**: Read `ARCHITECTURE.md`
5. **Contribute**: See `CONTRIBUTING.md`

---

## 💡 Key Concepts

### Zero Entropy
- Deterministic retrieval
- Minimal uncertainty
- Information density
- Ordered knowledge

### RAG System
- Semantic search
- Context injection
- Enhanced responses
- Source attribution

### Memory
- Short-term (session)
- Long-term (persistent)
- Consolidation
- Entropy optimization

---

## 🎓 Sample Questions

After loading demo knowledge:

- "What is Zero Entropy?"
- "Explain first principles thinking"
- "How does RAG work?"
- "What are vector embeddings?"
- "Describe the Linux philosophy"

---

## 🆘 Getting Help

1. Check documentation files
2. Review `EXAMPLES.md` for code samples
3. Search GitHub issues
4. Open new issue with details
5. Join discussions

---

## 📦 Project Stats

- **Backend**: ~2,500 lines of Python
- **Frontend**: ~1,500 lines of JavaScript/React
- **Docs**: ~10,000 words
- **Files**: ~75 total
- **Time to Deploy**: < 5 minutes

---

Built with **First Principles** • Optimized with **Zero Entropy** • Engineered for **Production**

For full documentation, see README.md
