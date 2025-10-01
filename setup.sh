#!/bin/bash

# Setup script for Zero Entropy ChatGPT Clone
# First principles: Check dependencies, configure environment, prepare system

set -e

echo "🔧 Setting up Zero Entropy ChatGPT Clone..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check Python version
echo -e "${GREEN}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python $PYTHON_VERSION found"
else
    echo -e "${RED}✗ Python3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}✗ pip3 not found. Please install pip.${NC}"
    exit 1
fi
echo "✓ pip3 found"

# Check Node.js
echo -e "${GREEN}Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js $NODE_VERSION found"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗ npm not found. Please install npm.${NC}"
    exit 1
fi
echo "✓ npm found"

# Create .env file if it doesn't exist
echo -e "${GREEN}Setting up environment...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Created .env file from .env.example${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your API keys!${NC}"
else
    echo "✓ .env file exists"
fi

# Create data directories
echo -e "${GREEN}Creating data directories...${NC}"
mkdir -p data/chroma data/sessions
echo "✓ Data directories created"

# Install Python dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip3 install -r requirements.txt
echo "✓ Python dependencies installed"

# Install frontend dependencies
echo -e "${GREEN}Installing frontend dependencies...${NC}"
cd frontend
npm install
cd ..
echo "✓ Frontend dependencies installed"

# Make scripts executable
chmod +x run.sh setup.sh

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run ./run.sh to start the application"
echo ""
