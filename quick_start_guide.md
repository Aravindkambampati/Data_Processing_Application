# 🚀 Quick Start Guide - Advanced Data Processor

## ⚡ Get Started in 5 Minutes

This guide will help you get up and running with the Advanced Data Processor in just a few minutes!

---

## 📋 Prerequisites

Before you start, make sure you have:
- Python 3.7+ installed
- Required packages: `pandas`, `PyQt5`, `matplotlib`, `numpy`
- A data file (CSV, Excel, JSON, or SQLite)

### Install Dependencies
```bash
pip install pandas PyQt5 matplotlib numpy openpyxl
```

---

## 🎯 Step-by-Step Tutorial

### Step 1: Launch the Application
```bash
python code.py
```

You'll see the main interface with:
- **Left Panel**: Control buttons organized by function
- **Right Panel**: Data display area with tabs

### Step 2: Load Your Data
1. **Select File Type**: Choose your file format from the dropdown
2. **Click "🚀 Load File"**: Opens file browser
3. **Select Your File**: Navigate to your data file
4. **Success!**: You'll see a confirmation message

**Example Success:**
```
Success: Loaded 1500 rows and 8 columns!
```

### Step 3: Explore Your Data
1. **View Data Table**: Your data appears in the table view
2. **Check Statistics**: Click "📊 Show Statistics" and switch to the Statistics tab
3. **Understand Your Data**: Review the statistics to understand your dataset

### Step 4: Clean Your Data
1. **Remove Null Values**: Click "🗑️ Drop Null Rows" to remove incomplete data
2. **Remove Duplicates**: Click "🔄 Remove Duplicates" to eliminate duplicates
3. **Reset if Needed**: Use "↺ Reset to Original" to start over

### Step 5: Filter Your Data
1. **Enter Filter Condition**: Type a condition like `Country == 'USA'`
2. **Apply Filter**: Click "🔍 Apply Filter"
3. **View Results**: See how many rows remain

### Step 6: Analyze Your Data
1. **Show Statistics**: Click "📊 Show Statistics" for detailed analysis
2. **Create Visualizations**: Click "📈 Plot Bar Chart" for charts
3. **Check Correlations**: Click "🔗 Correlation Matrix" for relationships

### Step 7: Export Your Results
1. **Click "💾 Export Cleaned Data"**
2. **Choose Format**: Select CSV or Excel
3. **Save File**: Choose location and filename

---

## 📊 Sample Data for Testing

If you don't have data to test with, create a simple CSV file:

**sample_data.csv:**
```csv
Name,Age,Salary,Department,Country
John Smith,32,65000,Sales,USA
Sarah Johnson,28,72000,Marketing,Canada
Mike Davis,35,85000,Engineering,USA
Lisa Wilson,29,68000,HR,UK
David Brown,41,95000,Engineering,Germany
```

---

## 🔧 Common Workflows

### Workflow 1: Basic Data Cleaning
1. Load your data
2. Click "📊 Show Statistics" to understand your data
3. Click "🗑️ Drop Null Rows" to remove incomplete records
4. Click "🔄 Remove Duplicates" to eliminate duplicates
5. Export cleaned data

### Workflow 2: Data Analysis
1. Load your data
2. Click "📊 Show Statistics" to see basic stats
3. Click "📈 Plot Bar Chart" to visualize distributions
4. Click "🔗 Correlation Matrix" to see relationships
5. Use filters to focus on specific subsets

### Workflow 3: Data Filtering
1. Load your data
2. Enter filter condition (e.g., `Age > 30`)
3. Click "🔍 Apply Filter"
4. Repeat with different conditions as needed
5. Export filtered results

---

## 🎨 Interface Tips

### Color-Coded Buttons
- **🟢 Green**: Safe operations (load, export)
- **🟠 Orange**: Data cleaning (destructive operations)
- **🔵 Blue**: Filtering operations
- **🟣 Purple**: Column-specific operations
- **🔘 Gray**: Analysis operations

### Keyboard Shortcuts
- **Tab**: Navigate between elements
- **Enter**: Activate buttons
- **Escape**: Close dialogs

### Performance Tips
- **Large Files**: The app shows only first 1000 rows for performance
- **Memory**: Close other applications for large datasets
- **Reset**: Use "Reset to Original" if operations become slow

---

## 🚨 Troubleshooting

### "File won't load"
- Check file format matches selected type
- Ensure file isn't corrupted
- Try with a simple CSV file first

### "Filter not working"
- Use exact column names
- Quote string values: `Country == 'USA'`
- Check pandas query syntax

### "App is slow"
- Close other applications
- Use smaller datasets for testing
- Restart the application

### "Export failed"
- Check disk space
- Ensure write permissions
- Close file if open in another app

---

## 📚 Next Steps

After mastering the basics:

1. **Advanced Filtering**: Learn pandas query syntax
2. **Data Visualization**: Explore different chart types
3. **Data Types**: Understand numeric vs categorical columns
4. **Best Practices**: Follow data cleaning workflows

---

## 🆘 Need Help?

1. **Check Error Messages**: Read the full error text
2. **Try Sample Data**: Test with the provided sample CSV
3. **Restart Application**: Close and reopen if issues persist
4. **Check File Format**: Ensure your data file is valid

---

*This quick start guide covers the essential operations. For detailed information, refer to the full Interface Guide.* 