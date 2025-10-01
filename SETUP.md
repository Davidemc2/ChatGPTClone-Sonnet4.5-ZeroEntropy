# Zero Entropy ChatGPT Clone - Setup Guide

## Quick Start (Docker - Recommended)

The fastest way to get started is using Docker:

### 1. Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### 2. Setup

```bash
# Clone or navigate to the project
cd zero-entropy-chat

# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

### 3. Run

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## Manual Setup (Development)

### Backend Setup

#### 1. Prerequisites
- Python 3.9 or higher
- pip

#### 2. Installation

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configuration

```bash
# Copy environment file
cp ../.env.example .env

# Edit .env with your settings
# REQUIRED: Set your OPENAI_API_KEY
nano .env
```

#### 4. Run Backend

```bash
python main.py
```

Backend will be available at http://localhost:8000

---

### Frontend Setup

#### 1. Prerequisites
- Node.js 18 or higher
- npm

#### 2. Installation

```bash
cd frontend

# Install dependencies
npm install
```

#### 3. Configuration

Create `.env.local` file:

```bash
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
```

#### 4. Run Frontend

```bash
# Development mode
npm start

# Production build
npm run build
npm install -g serve
serve -s build
```

Frontend will be available at http://localhost:3000 (dev) or http://localhost:3000 (production)

---

## Environment Variables

### Backend (.env)

```bash
# LLM Configuration (REQUIRED)
OPENAI_API_KEY=sk-...your-key-here

# Model Settings
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000

# RAG Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_STORE_PATH=./data/chroma
MAX_RETRIEVAL_RESULTS=5
SIMILARITY_THRESHOLD=0.7

# Memory Configuration
ENABLE_LONG_TERM_MEMORY=true
MEMORY_CONSOLIDATION_THRESHOLD=10
ENTROPY_OPTIMIZATION=true
MAX_CONTEXT_MESSAGES=10

# Server Configuration
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000

# Storage
DATA_DIR=./data
SESSIONS_DB=./data/sessions.json

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```bash
REACT_APP_API_URL=http://localhost:8000
```

---

## Testing the Installation

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "rag_engine": "ready",
  "memory_system": "ready",
  "llm_client": "ready"
}
```

### 2. Test API

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How does the RAG system work?",
    "use_rag": true
  }'
```

### 3. Access Frontend

Open http://localhost:3000 (or http://localhost for Docker) in your browser and start chatting!

---

## Adding Knowledge to RAG System

You can enhance the AI with custom knowledge:

### Via API

```bash
curl -X POST http://localhost:8000/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your custom knowledge or context here",
    "category": "documentation",
    "metadata": {
      "source": "manual",
      "topic": "custom"
    }
  }'
```

### Via Python Script

```python
import requests

url = "http://localhost:8000/api/memory/add"
data = {
    "content": "Important information about your domain",
    "category": "domain_knowledge",
    "metadata": {"importance": "high"}
}

response = requests.post(url, json=data)
print(response.json())
```

---

## Troubleshooting

### Backend Issues

**Problem**: "No module named 'X'"
```bash
pip install -r requirements.txt --force-reinstall
```

**Problem**: ChromaDB errors
```bash
# Clear ChromaDB data
rm -rf data/chroma
# Restart backend
```

**Problem**: OpenAI API errors
- Verify your API key is correct
- Check your OpenAI account has credits
- Ensure the model name is correct

### Frontend Issues

**Problem**: "Failed to fetch" errors
- Check backend is running
- Verify REACT_APP_API_URL is correct
- Check CORS settings in backend

**Problem**: Build errors
```bash
rm -rf node_modules package-lock.json
npm install
npm start
```

### Docker Issues

**Problem**: Container fails to start
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Problem**: Port already in use
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "3000:80"    # Frontend
```

---

## Performance Tuning

### For Better Response Speed

1. **Use faster models**:
   ```bash
   MODEL_NAME=gpt-3.5-turbo
   ```

2. **Reduce context window**:
   ```bash
   MAX_CONTEXT_MESSAGES=5
   MAX_TOKENS=1000
   ```

3. **Adjust RAG retrieval**:
   ```bash
   MAX_RETRIEVAL_RESULTS=3
   SIMILARITY_THRESHOLD=0.8
   ```

### For Better Quality

1. **Use advanced models**:
   ```bash
   MODEL_NAME=gpt-4-turbo-preview
   TEMPERATURE=0.7
   ```

2. **Increase context**:
   ```bash
   MAX_CONTEXT_MESSAGES=15
   MAX_RETRIEVAL_RESULTS=7
   ```

---

## Next Steps

1. **Customize the system prompt** in `backend/api/chat.py`
2. **Add domain-specific knowledge** via the memory API
3. **Adjust UI theme** in `frontend/src/*.css` files
4. **Configure advanced RAG** in `backend/core/rag_engine.py`

---

## Support

For issues and questions:
- Check the main README.md
- Review API documentation at http://localhost:8000/docs
- Examine logs for error messages

---

Built with **First Principles** • Optimized with **Zero Entropy** • Engineered for **Production**
