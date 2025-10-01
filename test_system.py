#!/usr/bin/env python3
"""
Zero Entropy System Validation Test

Quick validation script to ensure all components are working correctly.
Tests:
1. Import validation
2. Basic functionality
3. Configuration validation
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

def test_imports():
    """Test that all core modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.core.zero_entropy_rag import ZeroEntropyRAG
        print("✅ ZeroEntropyRAG import successful")
    except ImportError as e:
        print(f"❌ ZeroEntropyRAG import failed: {e}")
        return False
    
    try:
        from src.core.vector_store import VectorStore
        print("✅ VectorStore import successful")
    except ImportError as e:
        print(f"❌ VectorStore import failed: {e}")
        return False
    
    try:
        from src.utils.entropy_calculator import EntropyCalculator
        print("✅ EntropyCalculator import successful")
    except ImportError as e:
        print(f"❌ EntropyCalculator import failed: {e}")
        return False
    
    return True

def test_entropy_calculator():
    """Test entropy calculator functionality"""
    print("\n🧮 Testing Entropy Calculator...")
    
    try:
        from src.utils.entropy_calculator import EntropyCalculator
        
        calc = EntropyCalculator()
        
        # Test with sample text
        test_text = "This is a sample text for testing entropy calculation."
        entropy = calc.calculate_text_entropy(test_text)
        
        print(f"✅ Entropy calculation successful: {entropy:.2f}")
        
        if entropy > 0:
            print("✅ Entropy value is positive")
        else:
            print("❌ Entropy value should be positive")
            return False
            
    except Exception as e:
        print(f"❌ Entropy calculator test failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration files"""
    print("\n⚙️ Testing Configuration...")
    
    env_example = Path(__file__).parent / ".env.example"
    if env_example.exists():
        print("✅ .env.example file exists")
    else:
        print("❌ .env.example file missing")
        return False
    
    requirements = Path(__file__).parent / "requirements.txt"
    if requirements.exists():
        print("✅ requirements.txt file exists")
    else:
        print("❌ requirements.txt file missing")
        return False
    
    # Check frontend package.json
    frontend_pkg = Path(__file__).parent / "frontend" / "package.json"
    if frontend_pkg.exists():
        print("✅ Frontend package.json exists")
    else:
        print("❌ Frontend package.json missing")
        return False
    
    return True

def main():
    """Run all validation tests"""
    print("🚀 Zero Entropy System Validation")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test entropy calculator
    if not test_entropy_calculator():
        all_passed = False
    
    # Test configuration
    if not test_configuration():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Run: python start.py --frontend --dev")
        print("3. Open http://localhost:3000 in your browser")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

