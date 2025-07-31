#!/usr/bin/env python3
"""
Advanced Data Processor - Complete Installation and Launch Script
================================================================

This script handles the complete setup, installation, and launch of the
Advanced Data Processor application.

Features:
- Automatic dependency checking and installation
- Environment setup
- Application launch with error handling
- Sample data creation
- Documentation access

Usage:
    python install_and_run.py
"""

import sys
import os
import subprocess
import importlib.util
import platform
from pathlib import Path

class DataProcessorInstaller:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.requirements_file = self.project_dir / "requirements.txt"
        self.main_app_file = self.project_dir / "code.py"
        
    def print_banner(self):
        """Print application banner."""
        print("=" * 60)
        print("🚀 Advanced Data Processor - Complete Setup")
        print("=" * 60)
        print("📊 One-Click Data Processing Application")
        print("🎯 Features: Loading, Cleaning, Analysis, Visualization")
        print("=" * 60)
        
    def check_python_version(self):
        """Check if Python version is compatible."""
        print("🔍 Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print(f"❌ Python {version.major}.{version.minor} detected")
            print("⚠️  Python 3.7 or higher is required")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
        
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        print("🔍 Checking dependencies...")
        required_packages = {
            'pandas': 'pandas',
            'PyQt5': 'PyQt5',
            'matplotlib': 'matplotlib',
            'numpy': 'numpy',
            'openpyxl': 'openpyxl'
        }
        
        missing_packages = []
        installed_packages = []
        
        for package_name, import_name in required_packages.items():
            if importlib.util.find_spec(import_name) is None:
                missing_packages.append(package_name)
            else:
                installed_packages.append(package_name)
        
        if installed_packages:
            print(f"✅ Installed: {', '.join(installed_packages)}")
        
        if missing_packages:
            print(f"❌ Missing: {', '.join(missing_packages)}")
            return missing_packages
        
        print("✅ All dependencies are installed!")
        return []
        
    def install_dependencies(self, packages):
        """Install missing dependencies."""
        print(f"📦 Installing {len(packages)} missing packages...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--upgrade'
            ] + packages, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
            
    def create_sample_data(self):
        """Create sample data if it doesn't exist."""
        sample_file = self.project_dir / "sample_data.csv"
        if not sample_file.exists():
            print("📊 Creating sample data file...")
            sample_data = """Name,Age,Salary,Department,Country,Experience_Years,Performance_Rating
John Smith,32,65000,Sales,USA,5,4.2
Sarah Johnson,28,72000,Marketing,Canada,3,4.5
Mike Davis,35,85000,Engineering,USA,8,4.8
Lisa Wilson,29,68000,HR,UK,4,3.9
David Brown,41,95000,Engineering,Germany,12,4.7
Emma Thompson,26,58000,Sales,USA,2,3.8
James Anderson,33,78000,Marketing,Canada,6,4.3
Maria Garcia,31,82000,Engineering,Spain,7,4.6
Robert Lee,38,88000,Engineering,USA,10,4.4
Jennifer White,27,62000,HR,Canada,3,4.1"""
            
            with open(sample_file, 'w') as f:
                f.write(sample_data)
            print("✅ Sample data created: sample_data.csv")
        else:
            print("✅ Sample data already exists")
            
    def show_documentation_links(self):
        """Show available documentation."""
        print("\n📚 Documentation Available:")
        docs = [
            ("README.md", "Main project documentation"),
            ("quick_start_guide.md", "5-minute quick start guide"),
            ("interface_guide.md", "Complete interface documentation"),
            ("interface_mockup.html", "Visual interface reference")
        ]
        
        for doc_file, description in docs:
            doc_path = self.project_dir / doc_file
            if doc_path.exists():
                print(f"  📖 {doc_file} - {description}")
            else:
                print(f"  ❌ {doc_file} - Missing")
                
    def launch_application(self):
        """Launch the main application."""
        print("\n🎯 Launching Advanced Data Processor...")
        print("=" * 60)
        
        try:
            # Change to project directory
            os.chdir(self.project_dir)
            
            # Import and run the application
            from code import DataProcessorApp
            from PyQt5.QtWidgets import QApplication
            
            app = QApplication(sys.argv)
            window = DataProcessorApp()
            window.show()
            
            print("✅ Application launched successfully!")
            print("💡 Tips:")
            print("   • Use sample_data.csv to test the application")
            print("   • Check the documentation for detailed instructions")
            print("   • All operations are one-click!")
            
            return app.exec_()
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Please ensure all dependencies are installed correctly")
            return 1
        except Exception as e:
            print(f"❌ Error launching application: {e}")
            return 1
            
    def run(self):
        """Main installation and launch process."""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            return 1
            
        # Check and install dependencies
        missing_packages = self.check_dependencies()
        if missing_packages:
            print(f"\n📦 Installing {len(missing_packages)} missing packages...")
            if not self.install_dependencies(missing_packages):
                print("❌ Installation failed. Please install manually:")
                print(f"   pip install {' '.join(missing_packages)}")
                return 1
                
            # Re-check dependencies
            missing_packages = self.check_dependencies()
            if missing_packages:
                print("❌ Some dependencies are still missing")
                return 1
        
        # Create sample data
        self.create_sample_data()
        
        # Show documentation
        self.show_documentation_links()
        
        # Launch application
        return self.launch_application()

def main():
    """Main entry point."""
    installer = DataProcessorInstaller()
    return installer.run()

if __name__ == '__main__':
    sys.exit(main()) 