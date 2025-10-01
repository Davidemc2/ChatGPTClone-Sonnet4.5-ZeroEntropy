# Contributing to Zero Entropy ChatGPT Clone

Thank you for your interest in contributing! This project follows the Linux development philosophy: modular, transparent, and community-driven.

## Philosophy

### First Principles
- Question assumptions
- Build from fundamentals
- Optimize ruthlessly
- No unnecessary complexity

### Zero Entropy
- Minimize uncertainty
- Deterministic behavior
- Information density
- Ordered states

### Linux Methodology
- Modular design
- Do one thing well
- Transparent code
- Community collaboration

---

## How to Contribute

### 1. Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/zero-entropy-chat.git
   cd zero-entropy-chat
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Setup

Follow [SETUP.md](SETUP.md) for installation instructions.

#### Code Style

**Python (Backend)**:
- Follow PEP 8
- Use type hints where appropriate
- Document complex functions
- Keep functions focused and modular

```python
def calculate_entropy_score(text: str) -> float:
    """
    Calculate information entropy for text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Normalized entropy score (0-1)
    """
    # Implementation
```

**JavaScript/React (Frontend)**:
- Use functional components
- Prefer hooks over class components
- Keep components small and focused
- Use meaningful variable names

```javascript
// Good
const handleSubmit = async (message) => {
  // Implementation
};

// Avoid
const h = (m) => { /* ... */ };
```

#### Testing

Before submitting:
1. Test your changes locally
2. Ensure no regressions
3. Add tests for new features
4. Run linter (if available)

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test
```

#### Commit Messages

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Testing
- `chore`: Maintenance

Examples:
```
feat(rag): add hybrid search with keyword boosting

Implements hybrid search that combines semantic and keyword
matching for improved retrieval accuracy.

Closes #42
```

```
fix(memory): prevent duplicate context injection

Adds content fingerprinting to eliminate redundant memories
from being included in the same context window.
```

#### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure CI passes** (when available)
4. **Request review** from maintainers
5. **Address feedback** promptly

**PR Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
```

---

### 2. Documentation Contributions

Great documentation is crucial!

#### Areas to Improve
- API usage examples
- Architecture explanations
- Setup guides for different platforms
- Tutorial videos/blog posts
- FAQ additions

#### Documentation Style
- Clear and concise
- Code examples where helpful
- Screenshots for UI features
- Step-by-step instructions

---

### 3. Bug Reports

Found a bug? Help us fix it!

#### Before Reporting
1. Check existing issues
2. Verify it's reproducible
3. Test on latest version

#### Bug Report Template

```markdown
**Describe the bug**
Clear description of what's wrong

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Node version: [e.g., 18.17]
- Browser: [e.g., Chrome 120]

**Additional context**
Any other relevant information
```

---

### 4. Feature Requests

Have an idea? We'd love to hear it!

#### Feature Request Template

```markdown
**Problem Statement**
What problem does this solve?

**Proposed Solution**
How would you implement it?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Mockups, examples, related features
```

---

## Code Architecture Guidelines

### Backend

#### Adding New API Endpoints

1. **Create/update router** in `/backend/api/`
2. **Define Pydantic models** in `/backend/models/schemas.py`
3. **Add business logic** in `/backend/core/`
4. **Update main.py** if needed
5. **Document in README**

Example:
```python
# api/new_feature.py
from fastapi import APIRouter, Request
from models.schemas import NewFeatureRequest

router = APIRouter()

@router.post("/new-endpoint")
async def new_endpoint(request: NewFeatureRequest, app_request: Request):
    # Implementation
    return {"status": "success"}
```

#### Extending RAG Engine

For advanced RAG features:

```python
# core/rag_engine.py
class RAGEngine:
    def advanced_retrieval(self, query: str) -> List[Dict]:
        """
        Implement your advanced retrieval logic
        
        Should maintain Zero Entropy principles:
        - Deterministic
        - Entropy-optimized
        - Redundancy-free
        """
        pass
```

### Frontend

#### Adding New Components

1. **Create component file** in `/frontend/src/components/`
2. **Create CSS file** alongside
3. **Import and use** in parent component
4. **Follow existing patterns**

Example:
```jsx
// components/NewFeature.jsx
import React from 'react';
import './NewFeature.css';

const NewFeature = ({ prop1, prop2 }) => {
  return (
    <div className="new-feature">
      {/* Implementation */}
    </div>
  );
};

export default NewFeature;
```

#### API Integration

Update `/frontend/src/services/api.js`:

```javascript
export async function newApiFunction(param1, param2) {
  return apiCall('/api/new-endpoint', {
    method: 'POST',
    body: JSON.stringify({ param1, param2 }),
  });
}
```

---

## Performance Guidelines

### Backend Performance

1. **Minimize database calls**
   - Batch operations when possible
   - Cache frequently accessed data

2. **Optimize vector searches**
   - Adjust similarity threshold
   - Limit result count
   - Use metadata filtering

3. **Async operations**
   - Use `async/await` for I/O
   - Don't block event loop

### Frontend Performance

1. **Minimize re-renders**
   - Use `React.memo` for expensive components
   - Optimize state updates

2. **Code splitting**
   - Lazy load routes
   - Dynamic imports for large dependencies

3. **Asset optimization**
   - Compress images
   - Minimize bundle size

---

## Security Guidelines

1. **Never commit secrets**
   - Use environment variables
   - Add to `.gitignore`

2. **Validate all inputs**
   - Use Pydantic models
   - Sanitize user content

3. **Handle errors gracefully**
   - Don't expose internal details
   - Log appropriately

4. **Keep dependencies updated**
   - Regular security patches
   - Monitor for vulnerabilities

---

## Testing Guidelines

### Unit Tests

Test individual functions:

```python
# test_rag_engine.py
def test_entropy_calculation():
    engine = RAGEngine()
    score = engine._calculate_entropy_score("test text")
    assert 0 <= score <= 1
```

### Integration Tests

Test component interactions:

```python
# test_api.py
def test_chat_endpoint():
    response = client.post("/api/chat", json={
        "message": "Hello",
        "use_rag": True
    })
    assert response.status_code == 200
```

### Frontend Tests

```javascript
// Chat.test.js
import { render, screen } from '@testing-library/react';
import Chat from './Chat';

test('renders chat input', () => {
  render(<Chat sessionId="test" />);
  expect(screen.getByPlaceholderText(/send a message/i)).toBeInTheDocument();
});
```

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Requests**: Code contributions

### Code Review Process

1. Maintainer reviews PR
2. Feedback provided
3. Author addresses comments
4. Approval and merge

### Recognition

Contributors will be:
- Listed in contributors section
- Credited in release notes
- Acknowledged in documentation

---

## Project Structure

```
zero-entropy-chat/
├── backend/
│   ├── api/           # API endpoints
│   ├── core/          # Business logic
│   ├── models/        # Data models
│   └── main.py        # Entry point
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── App.js       # Root component
│   └── public/
├── docs/              # Additional documentation
├── tests/             # Test files
└── docker/            # Docker configurations
```

---

## Release Process

1. **Version bump** (semantic versioning)
2. **Update CHANGELOG**
3. **Tag release**
4. **Build and test**
5. **Deploy**

---

## Questions?

- Check [README.md](README.md)
- Review [SETUP.md](SETUP.md)
- Read [ARCHITECTURE.md](ARCHITECTURE.md)
- Open a GitHub Discussion

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Zero Entropy ChatGPT Clone!**

Built with **First Principles** • Optimized with **Zero Entropy** • Engineered for **Production**
