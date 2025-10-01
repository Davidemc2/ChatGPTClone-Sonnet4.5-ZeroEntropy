#!/usr/bin/env python3
"""
Zero Entropy ChatGPT Clone - Smart Startup Script

This script handles the complete setup and startup of the Zero Entropy system:
1. Checks system requirements
2. Sets up Python environment
3. Installs dependencies  
4. Starts backend server
5. Optionally starts frontend development server

Usage:
    python start.py [--frontend] [--dev] [--port 8000]
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path


class Colors:
    """Terminal colors for better output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    """Print Zero Entropy banner"""
    banner = f"""
{Colors.BLUE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║            🧠 ZERO ENTROPY CHATGPT CLONE 🚀             ║
║                                                          ║
║     Enhanced RAG System with Minimal Uncertainty        ║
║     Apple-Inspired Design • First Principles AI         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """
    print(banner)


def check_requirements():
    """Check system requirements"""
    print(f"{Colors.HEADER}🔍 Checking System Requirements...{Colors.ENDC}")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"{Colors.FAIL}❌ Python 3.8+ required. Current: {sys.version}{Colors.ENDC}")
        return False
    
    print(f"{Colors.GREEN}✅ Python {sys.version.split()[0]}{Colors.ENDC}")
    
    # Check pip
    try:
        import pip
        print(f"{Colors.GREEN}✅ pip available{Colors.ENDC}")
    except ImportError:
        print(f"{Colors.FAIL}❌ pip not available{Colors.ENDC}")
        return False
    
    # Check Node.js for frontend (optional)
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Node.js {result.stdout.strip()}{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}⚠️  Node.js not found (frontend won't be available){Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.WARNING}⚠️  Node.js not found (frontend won't be available){Colors.ENDC}")
    
    return True


def setup_environment():
    """Setup Python environment and install dependencies"""
    print(f"{Colors.HEADER}🔧 Setting up Python Environment...{Colors.ENDC}")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Change to backend directory
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # Install Python dependencies
        print(f"{Colors.BLUE}📦 Installing Python dependencies...{Colors.ENDC}")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print(f"{Colors.GREEN}✅ Python dependencies installed{Colors.ENDC}")
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Failed to install Python dependencies: {e}{Colors.ENDC}")
        return False
    finally:
        os.chdir(original_dir)
    
    return True


def setup_frontend():
    """Setup frontend dependencies"""
    print(f"{Colors.HEADER}🎨 Setting up Frontend...{Colors.ENDC}")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print(f"{Colors.WARNING}⚠️  Frontend directory not found{Colors.ENDC}")
        return False
    
    # Change to frontend directory
    original_dir = os.getcwd()
    os.chdir(frontend_dir)
    
    try:
        # Install npm dependencies
        print(f"{Colors.BLUE}📦 Installing npm dependencies...{Colors.ENDC}")
        subprocess.run(["npm", "install"], check=True)
        print(f"{Colors.GREEN}✅ Frontend dependencies installed{Colors.ENDC}")
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Failed to install frontend dependencies: {e}{Colors.ENDC}")
        return False
    except FileNotFoundError:
        print(f"{Colors.FAIL}❌ npm not found. Please install Node.js{Colors.ENDC}")
        return False
    finally:
        os.chdir(original_dir)
    
    return True


def check_env_file():
    """Check and create .env file if needed"""
    print(f"{Colors.HEADER}⚙️  Checking Configuration...{Colors.ENDC}")
    
    env_file = Path(__file__).parent / ".env"
    env_example = Path(__file__).parent / ".env.example"
    
    if not env_file.exists():
        if env_example.exists():
            print(f"{Colors.WARNING}⚠️  .env file not found. Creating from template...{Colors.ENDC}")
            
            # Copy .env.example to .env
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print(f"{Colors.GREEN}✅ .env file created{Colors.ENDC}")
            print(f"{Colors.WARNING}⚠️  Please edit .env file and add your OpenAI API key{Colors.ENDC}")
            print(f"{Colors.BLUE}   OPENAI_API_KEY=your_actual_key_here{Colors.ENDC}")
            
            return False  # Need user to add API key
        else:
            print(f"{Colors.FAIL}❌ No .env.example file found{Colors.ENDC}")
            return False
    
    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print(f"{Colors.WARNING}⚠️  Please add your actual OpenAI API key to .env file{Colors.ENDC}")
            return False
    
    print(f"{Colors.GREEN}✅ Configuration file ready{Colors.ENDC}")
    return True


def start_backend(port=8000, dev=False):
    """Start the backend server"""
    print(f"{Colors.HEADER}🚀 Starting Zero Entropy Backend Server...{Colors.ENDC}")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Change to backend directory
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # Start uvicorn server
        cmd = [
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", str(port)
        ]
        
        if dev:
            cmd.extend(["--reload", "--log-level", "debug"])
        
        print(f"{Colors.GREEN}🌟 Backend server starting on http://localhost:{port}{Colors.ENDC}")
        print(f"{Colors.BLUE}📖 API docs available at http://localhost:{port}/docs{Colors.ENDC}")
        print(f"{Colors.BLUE}🔍 Health check: http://localhost:{port}/health{Colors.ENDC}")
        print(f"{Colors.WARNING}Press Ctrl+C to stop the server{Colors.ENDC}")
        print()
        
        # Start server
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}🛑 Server stopped by user{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Failed to start backend server: {e}{Colors.ENDC}")
        return False
    finally:
        os.chdir(original_dir)
    
    return True


def start_frontend():
    """Start the frontend development server"""
    print(f"{Colors.HEADER}🎨 Starting Frontend Development Server...{Colors.ENDC}")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print(f"{Colors.WARNING}⚠️  Frontend directory not found{Colors.ENDC}")
        return False
    
    # Change to frontend directory
    original_dir = os.getcwd()
    os.chdir(frontend_dir)
    
    try:
        print(f"{Colors.GREEN}🌟 Frontend server starting on http://localhost:3000{Colors.ENDC}")
        print(f"{Colors.WARNING}Press Ctrl+C to stop the server{Colors.ENDC}")
        print()
        
        # Start React development server
        subprocess.run(["npm", "start"], check=True)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}🛑 Frontend server stopped by user{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Failed to start frontend server: {e}{Colors.ENDC}")
        return False
    except FileNotFoundError:
        print(f"{Colors.FAIL}❌ npm not found. Please install Node.js{Colors.ENDC}")
        return False
    finally:
        os.chdir(original_dir)
    
    return True


def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(description='Zero Entropy ChatGPT Clone Startup Script')
    parser.add_argument('--frontend', action='store_true', help='Also start frontend development server')
    parser.add_argument('--dev', action='store_true', help='Enable development mode (auto-reload)')
    parser.add_argument('--port', type=int, default=8000, help='Backend server port (default: 8000)')
    parser.add_argument('--skip-setup', action='store_true', help='Skip dependency installation')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print(f"{Colors.FAIL}❌ System requirements not met{Colors.ENDC}")
        sys.exit(1)
    
    # Setup environment
    if not args.skip_setup:
        if not setup_environment():
            print(f"{Colors.FAIL}❌ Failed to setup Python environment{Colors.ENDC}")
            sys.exit(1)
        
        if args.frontend:
            if not setup_frontend():
                print(f"{Colors.FAIL}❌ Failed to setup frontend{Colors.ENDC}")
                sys.exit(1)
    
    # Check configuration
    if not check_env_file():
        print(f"{Colors.FAIL}❌ Configuration incomplete{Colors.ENDC}")
        sys.exit(1)
    
    print(f"{Colors.GREEN}🎉 Setup complete! Starting Zero Entropy system...{Colors.ENDC}")
    print()
    
    # Start servers
    if args.frontend:
        # Start frontend in background
        import threading
        frontend_thread = threading.Thread(target=start_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()
        
        # Give frontend time to start
        time.sleep(2)
    
    # Start backend (this will block)
    start_backend(port=args.port, dev=args.dev)


if __name__ == "__main__":
    main()

