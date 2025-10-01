#!/bin/bash

# Zero Entropy ChatGPT Clone - Quick Start Script
# Built with First Principles | Optimized with Zero Entropy

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Zero Entropy ChatGPT Clone - Quick Start          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Check for required tools
echo "🔍 Checking prerequisites..."

if command -v docker-compose &> /dev/null || command -v docker &> /dev/null; then
    echo "✅ Docker found"
    USE_DOCKER=true
else
    echo "⚠️  Docker not found. Will use manual setup."
    USE_DOCKER=false
fi

if [ "$USE_DOCKER" = true ]; then
    echo ""
    echo "🐳 Starting with Docker Compose..."
    echo ""
    
    # Build and start containers
    docker-compose up -d --build
    
    echo ""
    echo "✅ Services started!"
    echo ""
    echo "📊 Checking service health..."
    sleep 5
    
    # Check backend health
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ Backend is healthy"
    else
        echo "⚠️  Backend may still be starting..."
    fi
    
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                 🎉 Ready to Go!                        ║"
    echo "╠════════════════════════════════════════════════════════╣"
    echo "║  Frontend:  http://localhost                          ║"
    echo "║  Backend:   http://localhost:8000                     ║"
    echo "║  API Docs:  http://localhost:8000/docs               ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "To stop services:"
    echo "  docker-compose down"
    echo ""
else
    echo ""
    echo "🔧 Manual setup required. Please follow these steps:"
    echo ""
    echo "1. Backend Setup:"
    echo "   cd backend"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
    echo "   pip install -r requirements.txt"
    echo "   python main.py"
    echo ""
    echo "2. Frontend Setup (in a new terminal):"
    echo "   cd frontend"
    echo "   npm install"
    echo "   npm start"
    echo ""
    echo "See SETUP.md for detailed instructions."
fi
