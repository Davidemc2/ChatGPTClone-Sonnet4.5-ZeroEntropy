#!/bin/bash

# Verification script for Zero Entropy ChatGPT Clone
# Checks that everything is properly installed and configured

echo "🔍 Zero Entropy ChatGPT Clone - System Verification"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        ((ERRORS++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
    else
        echo -e "${YELLOW}⚠${NC} $1/ (missing)"
        ((WARNINGS++))
    fi
}

echo "1. Checking Core Files"
echo "----------------------"
check_file "config.py"
check_file "requirements.txt"
check_file ".env.example"
check_file "setup.sh"
check_file "run.sh"
echo ""

echo "2. Checking Backend Files"
echo "-------------------------"
check_file "api/__init__.py"
check_file "api/main.py"
check_file "core/__init__.py"
check_file "core/vector_store.py"
check_file "core/memory_manager.py"
check_file "core/rag_engine.py"
echo ""

echo "3. Checking Frontend Files"
echo "---------------------------"
check_file "frontend/package.json"
check_file "frontend/vite.config.js"
check_file "frontend/index.html"
check_file "frontend/src/main.jsx"
check_file "frontend/src/App.jsx"
check_file "frontend/src/index.css"
check_file "frontend/src/components/ChatMessage.jsx"
check_file "frontend/src/components/ChatInput.jsx"
check_file "frontend/src/components/Header.jsx"
check_file "frontend/src/components/Sidebar.jsx"
check_file "frontend/src/store/chatStore.js"
echo ""

echo "4. Checking Documentation"
echo "-------------------------"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "ARCHITECTURE.md"
check_file "PROJECT_SUMMARY.md"
echo ""

echo "5. Checking Deployment Files"
echo "-----------------------------"
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file ".gitignore"
echo ""

echo "6. Checking Example Scripts"
echo "----------------------------"
check_file "examples/add_knowledge.py"
check_file "examples/test_chat.py"
echo ""

echo "7. Checking Dependencies"
echo "------------------------"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    ((ERRORS++))
fi

if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip3"
else
    echo -e "${RED}✗${NC} pip3 not found"
    ((ERRORS++))
fi

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version 2>&1)
    echo -e "${GREEN}✓${NC} Node.js $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found"
    ((ERRORS++))
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version 2>&1)
    echo -e "${GREEN}✓${NC} npm $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm not found"
    ((ERRORS++))
fi
echo ""

echo "8. Checking Configuration"
echo "-------------------------"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
    
    if grep -q "your_openai_api_key_here" .env; then
        echo -e "${YELLOW}⚠${NC} .env still contains placeholder API key"
        ((WARNINGS++))
    else
        echo -e "${GREEN}✓${NC} API key appears to be configured"
    fi
else
    echo -e "${YELLOW}⚠${NC} .env file not found (run setup.sh)"
    ((WARNINGS++))
fi
echo ""

echo "9. Checking Data Directories"
echo "-----------------------------"
check_dir "data"
check_dir "data/chroma"
check_dir "data/sessions"
echo ""

echo "10. Python Package Check"
echo "-------------------------"
if command -v pip3 &> /dev/null; then
    # Check for key packages
    PACKAGES=("fastapi" "uvicorn" "langchain" "chromadb" "openai")
    for pkg in "${PACKAGES[@]}"; do
        if pip3 show "$pkg" &> /dev/null; then
            echo -e "${GREEN}✓${NC} $pkg"
        else
            echo -e "${YELLOW}⚠${NC} $pkg (not installed)"
            ((WARNINGS++))
        fi
    done
else
    echo -e "${YELLOW}⚠${NC} Cannot check Python packages (pip3 not found)"
fi
echo ""

echo "=================================================="
echo "Summary"
echo "=================================================="
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! System is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure .env has your API keys"
    echo "  2. Run: ./run.sh"
    echo "  3. Open: http://localhost:3000"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  System mostly ready with some warnings.${NC}"
    echo ""
    echo "You may need to:"
    echo "  1. Run ./setup.sh to install dependencies"
    echo "  2. Add your API keys to .env"
    exit 0
else
    echo -e "${RED}❌ System has errors that need to be fixed.${NC}"
    echo ""
    echo "Please:"
    echo "  1. Check missing files above"
    echo "  2. Install missing dependencies"
    echo "  3. Run ./setup.sh"
    exit 1
fi
