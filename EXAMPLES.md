# Zero Entropy ChatGPT Clone - Usage Examples

## 📚 Table of Contents

1. [Basic Chat Usage](#basic-chat-usage)
2. [Adding Custom Knowledge](#adding-custom-knowledge)
3. [API Examples](#api-examples)
4. [Advanced RAG Queries](#advanced-rag-queries)
5. [Session Management](#session-management)
6. [Memory System Examples](#memory-system-examples)

---

## Basic Chat Usage

### Simple Conversation

1. **Start the application**
   ```bash
   ./quickstart.sh
   ```

2. **Open browser**: http://localhost

3. **Start chatting**:
   - Click "New Chat" in sidebar
   - Type your message
   - Press Enter to send

### Example Conversations

**General Q&A**:
```
User: What is the capital of France?
AI: The capital of France is Paris. It's the country's largest city...
```

**Technical Questions**:
```
User: Explain how vector embeddings work
AI: Vector embeddings are numerical representations of text...
[Enhanced with RAG if knowledge was added]
```

**Follow-up Context**:
```
User: What's your favorite color?
AI: As an AI, I don't have personal preferences...

User: Why not?
AI: [Remembers previous message about preferences]
Because I'm an artificial intelligence system...
```

---

## Adding Custom Knowledge

### Via Python Script

```python
import requests

API_URL = "http://localhost:8000"

knowledge = {
    "content": """
    Product Documentation: WidgetX Pro
    
    Features:
    - Ultra-fast processing (1000 TPS)
    - Cloud-native architecture
    - 99.99% uptime SLA
    
    Pricing:
    - Starter: $29/month
    - Pro: $99/month
    - Enterprise: Custom pricing
    """,
    "category": "product_docs",
    "metadata": {
        "product": "widgetx",
        "version": "2.0",
        "topic": "features_pricing"
    }
}

response = requests.post(
    f"{API_URL}/api/memory/add",
    json=knowledge
)

print(response.json())
# Output: {"status": "success", "document_id": "abc123...", ...}
```

### Via cURL

```bash
curl -X POST http://localhost:8000/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Company policy: All employees get 20 vacation days per year.",
    "category": "hr_policies",
    "metadata": {
      "department": "hr",
      "topic": "vacation"
    }
  }'
```

### Batch Upload

```python
import requests

documents = [
    {
        "content": "Technical documentation for Feature A...",
        "category": "technical",
        "metadata": {"feature": "A"}
    },
    {
        "content": "User guide for Feature B...",
        "category": "user_guides",
        "metadata": {"feature": "B"}
    },
    # ... more documents
]

response = requests.post(
    "http://localhost:8000/api/memory/batch-add",
    json=documents
)

print(f"Added {response.json()['count']} documents")
```

### From Text Files

```python
import requests
import os

def add_document_from_file(file_path, category):
    with open(file_path, 'r') as f:
        content = f.read()
    
    response = requests.post(
        "http://localhost:8000/api/memory/add",
        json={
            "content": content,
            "category": category,
            "metadata": {
                "source_file": os.path.basename(file_path),
                "added_date": "2025-10-01"
            }
        }
    )
    return response.json()

# Add multiple files
docs_dir = "./documents"
for filename in os.listdir(docs_dir):
    if filename.endswith(".txt"):
        result = add_document_from_file(
            os.path.join(docs_dir, filename),
            category="documentation"
        )
        print(f"Added {filename}: {result['document_id']}")
```

---

## API Examples

### Chat API

#### Simple Message

```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "What is RAG?",
        "use_rag": True
    }
)

data = response.json()
print(f"Session ID: {data['session_id']}")
print(f"Response: {data['message']}")
print(f"Metadata: {data['metadata']}")
```

#### Continue Conversation

```python
session_id = "your-session-id-here"

response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "session_id": session_id,
        "message": "Can you elaborate on that?",
        "use_rag": True
    }
)

print(response.json()['message'])
```

#### Custom Parameters

```python
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "Write a creative story",
        "use_rag": False,  # Don't use RAG for creative tasks
        "temperature": 0.9,  # More creative
        "max_tokens": 500
    }
)
```

### Memory/Search API

#### Search Knowledge

```python
response = requests.post(
    "http://localhost:8000/api/memory/search",
    json={
        "query": "vacation policy",
        "n_results": 5
    }
)

results = response.json()['results']
for result in results:
    print(f"Score: {result['final_score']:.2f}")
    print(f"Content: {result['content'][:100]}...")
    print(f"Metadata: {result['metadata']}")
    print("---")
```

#### Filter by Metadata

```python
response = requests.post(
    "http://localhost:8000/api/memory/search",
    json={
        "query": "technical documentation",
        "n_results": 10,
        "filter_by": {
            "category": "technical",
            "version": "2.0"
        }
    }
)
```

#### Get Statistics

```python
response = requests.get("http://localhost:8000/api/memory/stats")
stats = response.json()

print(f"Total documents: {stats['long_term_memories']}")
print(f"Active sessions: {stats['active_sessions']}")
print(f"Long-term memory: {stats['long_term_memory_enabled']}")
```

### Session Management

#### List All Sessions

```python
response = requests.get("http://localhost:8000/api/sessions")
sessions = response.json()['sessions']

for session in sessions:
    print(f"ID: {session['id']}")
    print(f"Created: {session['created_at']}")
    print(f"Messages: {len(session['messages'])}")
```

#### Get Session Details

```python
session_id = "your-session-id"
response = requests.get(f"http://localhost:8000/api/sessions/{session_id}")
session = response.json()

print(f"Session has {len(session['messages'])} messages")
for msg in session['messages'][-5:]:  # Last 5 messages
    print(f"{msg['role']}: {msg['content'][:50]}...")
```

#### Delete Session

```python
session_id = "your-session-id"
response = requests.delete(f"http://localhost:8000/api/sessions/{session_id}")
print(response.json()['message'])
```

---

## Advanced RAG Queries

### Domain-Specific Q&A

After adding domain knowledge:

```python
# Add knowledge
requests.post("http://localhost:8000/api/memory/add", json={
    "content": """
    Our company uses the Agile methodology with 2-week sprints.
    Daily standups at 9 AM. Sprint planning on Mondays.
    Retrospectives on Fridays. We use Jira for tracking.
    """,
    "category": "processes",
    "metadata": {"topic": "agile", "department": "engineering"}
})

# Query with RAG
response = requests.post("http://localhost:8000/api/chat", json={
    "message": "What's our sprint schedule?",
    "use_rag": True
})

# AI will retrieve the relevant context and respond accurately
```

### Multi-turn Technical Support

```python
session_id = None

# First question
response = requests.post("http://localhost:8000/api/chat", json={
    "message": "How do I reset my password?",
    "use_rag": True
})
session_id = response.json()['session_id']

# Follow-up (maintains context)
response = requests.post("http://localhost:8000/api/chat", json={
    "session_id": session_id,
    "message": "What if I don't receive the reset email?",
    "use_rag": True
})

# Another follow-up
response = requests.post("http://localhost:8000/api/chat", json={
    "session_id": session_id,
    "message": "Where is the reset link valid for how long?",
    "use_rag": True
})
```

### Code Documentation Chat

```python
# Add code documentation
requests.post("http://localhost:8000/api/memory/add", json={
    "content": """
    API Endpoint: /api/users
    
    GET /api/users - List all users
    POST /api/users - Create new user
    GET /api/users/{id} - Get user by ID
    PUT /api/users/{id} - Update user
    DELETE /api/users/{id} - Delete user
    
    Authentication: Bearer token required
    Rate limit: 100 requests per minute
    """,
    "category": "api_docs",
    "metadata": {"endpoint": "users", "version": "v1"}
})

# Ask about the API
response = requests.post("http://localhost:8000/api/chat", json={
    "message": "How do I create a new user via the API?",
    "use_rag": True
})
```

---

## Memory System Examples

### Session Memory (Short-term)

Session memory automatically tracks recent conversation:

```python
# Start conversation
response1 = requests.post("http://localhost:8000/api/chat", json={
    "message": "My name is Alice and I work in engineering"
})
session_id = response1.json()['session_id']

# Ask about previous information
response2 = requests.post("http://localhost:8000/api/chat", json={
    "session_id": session_id,
    "message": "What's my name and department?"
})

# AI will remember: "Your name is Alice and you work in engineering"
```

### Long-term Memory (Persistent)

Long-term memory stores important information across sessions:

```python
# Session 1: Tell AI something important
requests.post("http://localhost:8000/api/chat", json={
    "session_id": "session-1",
    "message": "Remember that our Q4 launch date is December 15th"
})

# ... time passes ...

# Session 2: Different session, but can recall
response = requests.post("http://localhost:8000/api/chat", json={
    "session_id": "session-2",  # Different session!
    "message": "When is our Q4 launch?",
    "use_rag": True  # RAG retrieves from long-term memory
})

# AI finds the information from the previous session
```

### Memory Consolidation

When a conversation gets long, memory is automatically consolidated:

```python
# Have a long conversation (20+ messages)
session_id = "long-session"

for i in range(25):
    requests.post("http://localhost:8000/api/chat", json={
        "session_id": session_id,
        "message": f"Question {i}: Tell me about topic {i}"
    })

# Get session details
response = requests.get(f"http://localhost:8000/api/sessions/{session_id}")
session = response.json()

# Notice:
# - Recent messages are fully preserved
# - Older messages are summarized
# - Summary available in session['summary']
print(f"Summary: {session.get('summary', 'None')}")
print(f"Recent messages: {len(session['messages'])}")
```

---

## Integration Examples

### Slack Bot Integration

```python
from slack_bolt import App
import requests

app = App(token="xoxb-your-token")

CHAT_API = "http://localhost:8000/api/chat"

@app.message(".*")
def handle_message(message, say):
    user_id = message['user']
    text = message['text']
    
    # Use user_id as session_id for continuity
    response = requests.post(CHAT_API, json={
        "session_id": f"slack-{user_id}",
        "message": text,
        "use_rag": True
    })
    
    ai_response = response.json()['message']
    say(ai_response)

app.start(3000)
```

### Discord Bot Integration

```python
import discord
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

CHAT_API = "http://localhost:8000/api/chat"

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    response = requests.post(CHAT_API, json={
        "session_id": f"discord-{message.author.id}",
        "message": message.content,
        "use_rag": True
    })
    
    await message.channel.send(response.json()['message'])

client.run('your-discord-token')
```

### CLI Tool

```python
#!/usr/bin/env python3
import requests
import sys

API_URL = "http://localhost:8000/api/chat"
SESSION_FILE = ".chat_session"

def load_session():
    try:
        with open(SESSION_FILE, 'r') as f:
            return f.read().strip()
    except:
        return None

def save_session(session_id):
    with open(SESSION_FILE, 'w') as f:
        f.write(session_id)

def chat(message):
    session_id = load_session()
    
    response = requests.post(API_URL, json={
        "session_id": session_id,
        "message": message,
        "use_rag": True
    })
    
    data = response.json()
    save_session(data['session_id'])
    
    return data['message']

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: chat.py 'your message'")
        sys.exit(1)
    
    message = ' '.join(sys.argv[1:])
    response = chat(message)
    print(response)
```

Usage:
```bash
./chat.py "Hello, how are you?"
./chat.py "What did I just say?"  # Maintains context
```

---

## Performance Tips

### Optimize for Speed

```python
# Disable RAG for simple queries (faster)
response = requests.post("http://localhost:8000/api/chat", json={
    "message": "Hello!",
    "use_rag": False,
    "max_tokens": 100
})

# Use lower temperature for faster, more deterministic responses
response = requests.post("http://localhost:8000/api/chat", json={
    "message": "Quick question",
    "temperature": 0.3
})
```

### Optimize for Quality

```python
# Enable RAG and allow more context
response = requests.post("http://localhost:8000/api/chat", json={
    "message": "Explain our complex technical architecture",
    "use_rag": True,
    "temperature": 0.7,
    "max_tokens": 2000
})
```

### Batch Knowledge Upload

```python
# More efficient than individual uploads
documents = [{"content": f"Doc {i}", "category": "batch"} for i in range(100)]

response = requests.post(
    "http://localhost:8000/api/memory/batch-add",
    json=documents
)
```

---

## Troubleshooting Examples

### Check System Health

```python
response = requests.get("http://localhost:8000/health")
health = response.json()

if health['status'] == 'healthy':
    print("✅ System is operational")
    print(f"RAG Engine: {health['rag_engine']}")
    print(f"Memory System: {health['memory_system']}")
    print(f"LLM Client: {health['llm_client']}")
else:
    print("❌ System issue detected")
```

### Clear Memory (Fresh Start)

```python
# Clear all sessions and knowledge
response = requests.delete("http://localhost:8000/api/memory/clear")
print(response.json()['message'])

# Verify
stats = requests.get("http://localhost:8000/api/memory/stats").json()
print(f"Documents: {stats['long_term_memories']}")  # Should be 0
```

---

## Best Practices

### 1. Use Descriptive Metadata

```python
# Good
requests.post("http://localhost:8000/api/memory/add", json={
    "content": "...",
    "category": "product_docs",
    "metadata": {
        "product": "widgetx",
        "version": "2.0",
        "section": "api",
        "importance": "high",
        "last_updated": "2025-10-01"
    }
})
```

### 2. Organize by Category

```python
categories = [
    "technical_docs",
    "user_guides",
    "api_reference",
    "troubleshooting",
    "policies"
]
```

### 3. Keep Knowledge Updated

```python
# Update by adding new version (deterministic ID will differ)
old_doc_id = "abc123..."

# Add updated version
new_response = requests.post("http://localhost:8000/api/memory/add", json={
    "content": "Updated content...",
    "metadata": {"replaces": old_doc_id, "version": "2.0"}
})
```

---

**More examples and use cases coming soon!**

For questions or suggestions, open a GitHub issue or discussion.

Built with **First Principles** • Optimized with **Zero Entropy** • Engineered for **Production**
