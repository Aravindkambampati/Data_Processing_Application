#!/usr/bin/env python3
"""
Advanced Data Processor - Launcher Script
=========================================

This script launches the Advanced Data Processor application with proper
error handling and dependency checking.

Usage:
    python run.py
"""

import sys
import os
import subprocess
import importlib.util

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = {
        'pandas': 'pandas',
        'PyQt5': 'PyQt5',
        'matplotlib': 'matplotlib',
        'numpy': 'numpy',
        'openpyxl': 'openpyxl'
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(package_name)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing dependencies."""
    print("Installing missing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main launcher function."""
    print("🚀 Advanced Data Processor - Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('code.py'):
        print("❌ Error: code.py not found in current directory")
        print("Please run this script from the Project directory")
        return 1
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        response = input("Would you like to install them now? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if not install_dependencies(missing_packages):
                return 1
        else:
            print("❌ Cannot run without required dependencies")
            print("Please install manually: pip install -r requirements.txt")
            return 1
    
    print("✅ All dependencies found!")
    
    # Launch the application
    print("🎯 Launching Advanced Data Processor...")
    print("=" * 50)
    
    try:
        # Import and run the application
        from code import DataProcessorApp
        import sys
        from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = DataProcessorApp()
        window.show()
        
        print("✅ Application launched successfully!")
        print("💡 Tip: Use the sample_data.csv file to test the application")
        
        return app.exec_()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed correctly")
        return 1
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 