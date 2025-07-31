# 📊 Advanced Data Processor - One-Click Operations

A powerful desktop application for data processing, cleaning, analysis, and visualization with intuitive one-click operations.

## 🚀 Features

### 📁 **File Operations**
- Load CSV, Excel, JSON, and SQLite files
- Automatic file type detection
- Success notifications with data statistics

### 🧹 **Data Cleaning**
- **One-click null row removal**
- **Duplicate elimination**
- **Data reset to original state**
- **Smart null value filling** (mean for numeric, mode for categorical)

### 🔍 **Data Filtering**
- **Advanced pandas query syntax**
- **Real-time filter feedback**
- **Complex condition support**

### 📊 **Column Operations**
- **Column renaming** with validation
- **Null value filling** by data type
- **Column selection** dropdown

### 📈 **Data Analysis**
- **Comprehensive statistics** display
- **Bar chart visualizations**
- **Correlation matrix heatmaps**
- **Tabbed interface** for data and statistics

### 💾 **Export Functionality**
- **Multiple formats** (CSV, Excel)
- **Success confirmations**
- **File path display**

## 🎨 **Interface Design**

- **Color-coded buttons** for different operations
- **Emoji indicators** for visual clarity
- **Organized sections** with clear grouping
- **Responsive layout** that adapts to screen size
- **Performance optimized** for large datasets

## 📋 **Quick Start**

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python code.py
```

### Basic Workflow
1. **Load Data**: Select file type and click "🚀 Load File"
2. **Explore**: Click "📊 Show Statistics" to understand your data
3. **Clean**: Use "🗑️ Drop Null Rows" and "🔄 Remove Duplicates"
4. **Filter**: Enter conditions like `Country == 'USA'`
5. **Analyze**: Create visualizations with "📈 Plot Bar Chart"
6. **Export**: Save cleaned data with "💾 Export Cleaned Data"

## 📚 **Documentation**

- **[Quick Start Guide](quick_start_guide.md)** - Get started in 5 minutes
- **[Interface Guide](interface_guide.md)** - Complete feature documentation
- **[Interface Mockup](interface_mockup.html)** - Visual reference

## 🛠️ **Installation**

### Option 1: Using requirements.txt
```bash
pip install -r requirements.txt
```

### Option 2: Manual installation
```bash
pip install pandas PyQt5 matplotlib numpy openpyxl xlrd
```

## 📊 **Supported File Formats**

| Format | Extension | Features |
|--------|-----------|----------|
| CSV | `.csv` | Comma-separated values |
| Excel | `.xlsx`, `.xls` | Multiple sheets support |
| JSON | `.json` | Nested data structures |
| SQLite | `.db`, `.sqlite`, `.sqlite3` | Database tables |

## 🔧 **Usage Examples**

### Basic Data Cleaning
```python
# Load data
# Click "🚀 Load File" and select your CSV

# Clean data
# Click "🗑️ Drop Null Rows"
# Click "🔄 Remove Duplicates"

# Export results
# Click "💾 Export Cleaned Data"
```

### Advanced Filtering
```python
# Filter conditions examples:
Country == 'USA'                    # Exact match
Age > 30                           # Numeric comparison
Salary >= 50000 and Department == 'Sales'  # Complex filter
Name.str.contains('John')          # String contains
```

### Data Analysis
```python
# View statistics
# Click "📊 Show Statistics"

# Create visualizations
# Click "📈 Plot Bar Chart"

# Check correlations
# Click "🔗 Correlation Matrix"
```

## 🎯 **Key Features**

### **One-Click Operations**
- **Data Loading**: Support for multiple file formats
- **Data Cleaning**: Remove nulls, duplicates, fill missing values
- **Data Filtering**: Advanced query syntax with real-time feedback
- **Data Analysis**: Statistics, visualizations, correlations
- **Data Export**: Multiple format support with success confirmations

### **User-Friendly Interface**
- **Color-coded buttons** for different operation types
- **Emoji indicators** for visual clarity
- **Organized sections** with clear grouping
- **Tabbed interface** for data and statistics views
- **Status bar** showing current data state

### **Performance Optimizations**
- **Limited display**: Shows only first 1000 rows for performance
- **Smart updates**: Only updates necessary components
- **Memory efficient**: Handles large datasets efficiently
- **Error handling**: Graceful failure with clear messages

## 🚨 **Troubleshooting**

### Common Issues

**"File won't load"**
- Check file format matches selected type
- Ensure file isn't corrupted
- Try with a simple CSV file first

**"Filter not working"**
- Use exact column names
- Quote string values: `Country == 'USA'`
- Check pandas query syntax

**"App is slow"**
- Close other applications
- Use smaller datasets for testing
- Restart the application

**"Export failed"**
- Check disk space
- Ensure write permissions
- Close file if open in another app

### Performance Tips
1. **Close unused applications** to free up memory
2. **Use smaller datasets** for testing
3. **Restart application** if performance degrades
4. **Check file format** before loading

## 📈 **Advanced Features**

### **Smart Data Handling**
- **Automatic data type detection**
- **Intelligent null value filling**
- **Memory-efficient large file handling**
- **Original data preservation** for reset functionality

### **Visualization Capabilities**
- **Bar charts** for categorical data
- **Correlation matrices** for numeric data
- **Responsive chart sizing**
- **Export-ready visualizations**

### **Data Validation**
- **Input validation** for all operations
- **Error handling** with user-friendly messages
- **Data integrity checks**
- **Format validation** for supported file types

## 🔄 **Workflow Examples**

### **Workflow 1: Basic Data Cleaning**
1. Load your data file
2. Click "📊 Show Statistics" to understand your data
3. Click "🗑️ Drop Null Rows" to remove incomplete records
4. Click "🔄 Remove Duplicates" to eliminate duplicates
5. Export cleaned data

### **Workflow 2: Data Analysis**
1. Load your data file
2. Click "📊 Show Statistics" to see basic stats
3. Click "📈 Plot Bar Chart" to visualize distributions
4. Click "🔗 Correlation Matrix" to see relationships
5. Use filters to focus on specific subsets

### **Workflow 3: Data Filtering**
1. Load your data file
2. Enter filter condition (e.g., `Age > 30`)
3. Click "🔍 Apply Filter"
4. Repeat with different conditions as needed
5. Export filtered results

## 📞 **Support**

If you encounter issues:
1. **Check error messages** - Read the full error text
2. **Verify data format** - Ensure your data file is valid
3. **Try sample data** - Test with a simple CSV file first
4. **Restart application** - Close and reopen if issues persist

## 🤝 **Contributing**

This application is designed for easy data processing. If you have suggestions for improvements:

1. **Feature requests** - Open an issue with detailed description
2. **Bug reports** - Include error messages and steps to reproduce
3. **Documentation** - Help improve guides and examples

## 📄 **License**

This project is open source and available under the MIT License.

---

**🎯 Ready to process your data with one-click operations!**

*For detailed usage instructions, see the [Quick Start Guide](quick_start_guide.md) and [Interface Guide](interface_guide.md).* 