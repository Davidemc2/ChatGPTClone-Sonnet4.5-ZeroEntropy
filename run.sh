#!/bin/bash

# Zero Entropy ChatGPT Clone - Startup Script
# Following Unix philosophy: Simple, focused, modular

set -e

echo "🚀 Starting Zero Entropy ChatGPT Clone..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}❗ Please edit .env with your API keys before continuing!${NC}"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 16+${NC}"
    exit 1
fi

# Install Python dependencies
echo -e "${GREEN}📦 Installing Python dependencies...${NC}"
pip3 install -r requirements.txt

# Create necessary directories
mkdir -p data/chroma data/sessions

# Start backend
echo -e "${GREEN}🔧 Starting FastAPI backend...${NC}"
cd api
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Give backend time to start
sleep 3

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${GREEN}📦 Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Start frontend
echo -e "${GREEN}🎨 Starting React frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✅ System started successfully!${NC}"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo -e '\n${YELLOW}🛑 Stopping services...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait
