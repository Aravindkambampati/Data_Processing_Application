import sys
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox,
    QHBoxLayout, QGroupBox, QTextEdit, QSplitter, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DataProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Data Processor - One-Click Operations")
        self.resize(1200, 800)

        self.df = None
        self.original_df = None  # Keep original data for reset

        # Create main layout
        main_layout = QHBoxLayout()
        
        # Create left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # File loading section
        file_group = QGroupBox("📁 File Operations")
        file_layout = QVBoxLayout()
        
        self.label = QLabel("Upload a CSV, Excel, JSON, or SQLite DB file")
        self.label.setFont(QFont("Arial", 10, QFont.Bold))
        file_layout.addWidget(self.label)

        self.filetype_dropdown = QComboBox()
        self.filetype_dropdown.addItems(["CSV", "Excel", "JSON", "SQLite"])
        file_layout.addWidget(self.filetype_dropdown)

        self.load_button = QPushButton("🚀 Load File")
        self.load_button.clicked.connect(self.load_file)
        self.load_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px; }")
        file_layout.addWidget(self.load_button)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)

        # Data cleaning section
        clean_group = QGroupBox("🧹 Data Cleaning")
        clean_layout = QVBoxLayout()
        
        self.dropna_button = QPushButton("🗑️ Drop Null Rows")
        self.dropna_button.clicked.connect(self.drop_na)
        self.dropna_button.setEnabled(False)
        self.dropna_button.setStyleSheet("QPushButton { background-color: #FF9800; color: white; padding: 8px; }")
        clean_layout.addWidget(self.dropna_button)

        self.duplicates_button = QPushButton("🔄 Remove Duplicates")
        self.duplicates_button.clicked.connect(self.remove_duplicates)
        self.duplicates_button.setEnabled(False)
        self.duplicates_button.setStyleSheet("QPushButton { background-color: #FF9800; color: white; padding: 8px; }")
        clean_layout.addWidget(self.duplicates_button)

        self.reset_button = QPushButton("↺ Reset to Original")
        self.reset_button.clicked.connect(self.reset_data)
        self.reset_button.setEnabled(False)
        self.reset_button.setStyleSheet("QPushButton { background-color: #9E9E9E; color: white; padding: 8px; }")
        clean_layout.addWidget(self.reset_button)
        
        clean_group.setLayout(clean_layout)
        left_layout.addWidget(clean_group)

        # Filtering section
        filter_group = QGroupBox("🔍 Data Filtering")
        filter_layout = QVBoxLayout()
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter filter condition (e.g., Country == 'USA')")
        filter_layout.addWidget(self.filter_input)

        self.filter_button = QPushButton("🔍 Apply Filter")
        self.filter_button.clicked.connect(self.apply_filter)
        self.filter_button.setEnabled(False)
        self.filter_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 8px; }")
        filter_layout.addWidget(self.filter_button)
        
        filter_group.setLayout(filter_layout)
        left_layout.addWidget(filter_group)

        # Column operations section
        column_group = QGroupBox("📊 Column Operations")
        column_layout = QVBoxLayout()
        
        self.column_dropdown = QComboBox()
        self.column_dropdown.setEnabled(False)
        column_layout.addWidget(self.column_dropdown)

        self.fillna_button = QPushButton("📝 Fill Null Values")
        self.fillna_button.clicked.connect(self.fill_null_values)
        self.fillna_button.setEnabled(False)
        self.fillna_button.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; padding: 8px; }")
        column_layout.addWidget(self.fillna_button)

        self.rename_button = QPushButton("✏️ Rename Column")
        self.rename_button.clicked.connect(self.rename_column)
        self.rename_button.setEnabled(False)
        self.rename_button.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; padding: 8px; }")
        column_layout.addWidget(self.rename_button)
        
        column_group.setLayout(column_layout)
        left_layout.addWidget(column_group)

        # Analysis section
        analysis_group = QGroupBox("📈 Data Analysis")
        analysis_layout = QVBoxLayout()
        
        self.stats_button = QPushButton("📊 Show Statistics")
        self.stats_button.clicked.connect(self.show_statistics)
        self.stats_button.setEnabled(False)
        self.stats_button.setStyleSheet("QPushButton { background-color: #607D8B; color: white; padding: 8px; }")
        analysis_layout.addWidget(self.stats_button)

        self.plot_button = QPushButton("📈 Plot Bar Chart")
        self.plot_button.clicked.connect(self.plot_column)
        self.plot_button.setEnabled(False)
        self.plot_button.setStyleSheet("QPushButton { background-color: #607D8B; color: white; padding: 8px; }")
        analysis_layout.addWidget(self.plot_button)

        self.correlation_button = QPushButton("🔗 Correlation Matrix")
        self.correlation_button.clicked.connect(self.show_correlation)
        self.correlation_button.setEnabled(False)
        self.correlation_button.setStyleSheet("QPushButton { background-color: #607D8B; color: white; padding: 8px; }")
        analysis_layout.addWidget(self.correlation_button)
        
        analysis_group.setLayout(analysis_layout)
        left_layout.addWidget(analysis_group)

        # Export section
        export_group = QGroupBox("💾 Export Data")
        export_layout = QVBoxLayout()
        
        self.export_button = QPushButton("💾 Export Cleaned Data")
        self.export_button.clicked.connect(self.export_data)
        self.export_button.setEnabled(False)
        self.export_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px; }")
        export_layout.addWidget(self.export_button)
        
        export_group.setLayout(export_layout)
        left_layout.addWidget(export_group)

        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)
        main_layout.addWidget(left_panel)

        # Create right panel for data display
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Create tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Data table tab
        self.table = QTableWidget()
        self.tab_widget.addTab(self.table, "📋 Data Table")
        
        # Statistics tab
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.tab_widget.addTab(self.stats_text, "📊 Statistics")
        
        right_layout.addWidget(self.tab_widget)
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)

        self.setLayout(main_layout)

    def load_file(self):
        file_type = self.filetype_dropdown.currentText()
        file_filter = {
            "CSV": "CSV Files (*.csv)",
            "Excel": "Excel Files (*.xlsx *.xls)",
            "JSON": "JSON Files (*.json)",
            "SQLite": "SQLite DB Files (*.db *.sqlite *.sqlite3)"
        }[file_type]

        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", file_filter)

        if file_path:
            try:
                if file_type == "CSV":
                    self.df = pd.read_csv(file_path)
                elif file_type == "Excel":
                    self.df = pd.read_excel(file_path)
                elif file_type == "JSON":
                    self.df = pd.read_json(file_path)
                elif file_type == "SQLite":
                    conn = sqlite3.connect(file_path)
                    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
                    table_name = tables.iloc[0, 0]  # Default to first table
                    self.df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    conn.close()
                
                self.original_df = self.df.copy()  # Save original
                self.show_data()
                self.update_column_dropdown()
                self.enable_all_buttons()
                QMessageBox.information(self, "Success", f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def enable_all_buttons(self):
        """Enable all buttons after data is loaded"""
        self.dropna_button.setEnabled(True)
        self.duplicates_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.export_button.setEnabled(True)
        self.filter_button.setEnabled(True)
        self.plot_button.setEnabled(True)
        self.stats_button.setEnabled(True)
        self.correlation_button.setEnabled(True)
        self.fillna_button.setEnabled(True)
        self.rename_button.setEnabled(True)
        self.column_dropdown.setEnabled(True)

    def update_column_dropdown(self):
        """Update column dropdown with current dataframe columns"""
        self.column_dropdown.clear()
        if self.df is not None:
            self.column_dropdown.addItems(self.df.columns.astype(str))

    def show_data(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        if self.df is not None:
            # Show only first 1000 rows for performance
            display_df = self.df.head(1000)
            self.table.setColumnCount(len(display_df.columns))
            self.table.setRowCount(len(display_df.index))
            self.table.setHorizontalHeaderLabels(display_df.columns.astype(str))

            for i in range(len(display_df.index)):
                for j in range(len(display_df.columns)):
                    value = str(display_df.iat[i, j])
                    self.table.setItem(i, j, QTableWidgetItem(value))

    def drop_na(self):
        if self.df is not None:
            before_count = len(self.df)
            self.df.dropna(inplace=True)
            after_count = len(self.df)
            self.show_data()
            QMessageBox.information(self, "Success", f"Dropped {before_count - after_count} rows with null values!")

    def remove_duplicates(self):
        if self.df is not None:
            before_count = len(self.df)
            self.df.drop_duplicates(inplace=True)
            after_count = len(self.df)
            self.show_data()
            QMessageBox.information(self, "Success", f"Removed {before_count - after_count} duplicate rows!")

    def reset_data(self):
        if self.original_df is not None:
            self.df = self.original_df.copy()
            self.show_data()
            self.update_column_dropdown()
            QMessageBox.information(self, "Success", "Data reset to original state!")

    def apply_filter(self):
        condition = self.filter_input.text()
        if self.df is not None and condition:
            try:
                before_count = len(self.df)
                self.df = self.df.query(condition)
                after_count = len(self.df)
                self.show_data()
                QMessageBox.information(self, "Success", f"Filter applied! {after_count} rows remaining (was {before_count})")
            except Exception as e:
                QMessageBox.critical(self, "Filter Error", str(e))

    def fill_null_values(self):
        if self.df is not None and self.column_dropdown.currentText():
            column = self.column_dropdown.currentText()
            try:
                # For numeric columns, fill with mean; for others, fill with mode
                if pd.api.types.is_numeric_dtype(self.df[column]):
                    fill_value = self.df[column].mean()
                else:
                    fill_value = self.df[column].mode().iloc[0] if not self.df[column].mode().empty else "Unknown"
                
                self.df[column].fillna(fill_value, inplace=True)
                self.show_data()
                QMessageBox.information(self, "Success", f"Filled null values in '{column}' with {fill_value}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def rename_column(self):
        if self.df is not None and self.column_dropdown.currentText():
            old_name = self.column_dropdown.currentText()
            new_name, ok = QFileDialog.getText(self, "Rename Column", f"Enter new name for '{old_name}':")
            if ok and new_name:
                try:
                    self.df.rename(columns={old_name: new_name}, inplace=True)
                    self.show_data()
                    self.update_column_dropdown()
                    QMessageBox.information(self, "Success", f"Column '{old_name}' renamed to '{new_name}'")
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def show_statistics(self):
        if self.df is not None:
            stats_text = "📊 DATA STATISTICS\n" + "="*50 + "\n\n"
            
            # Basic info
            stats_text += f"📋 Dataset Info:\n"
            stats_text += f"   • Rows: {len(self.df)}\n"
            stats_text += f"   • Columns: {len(self.df.columns)}\n"
            stats_text += f"   • Memory usage: {self.df.memory_usage(deep=True).sum() / 1024:.2f} KB\n\n"
            
            # Null values
            null_counts = self.df.isnull().sum()
            if null_counts.sum() > 0:
                stats_text += f"🔍 Null Values:\n"
                for col, count in null_counts[null_counts > 0].items():
                    stats_text += f"   • {col}: {count} ({count/len(self.df)*100:.1f}%)\n"
                stats_text += "\n"
            
            # Numeric columns statistics
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                stats_text += f"📈 Numeric Columns Statistics:\n"
                stats_text += self.df[numeric_cols].describe().to_string()
                stats_text += "\n\n"
            
            # Categorical columns
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                stats_text += f"📝 Categorical Columns:\n"
                for col in categorical_cols:
                    unique_count = self.df[col].nunique()
                    stats_text += f"   • {col}: {unique_count} unique values\n"
            
            self.stats_text.setText(stats_text)
            self.tab_widget.setCurrentIndex(1)  # Switch to stats tab

    def show_correlation(self):
        if self.df is not None:
            numeric_df = self.df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                try:
                    correlation_matrix = numeric_df.corr()
                    plt.figure(figsize=(10, 8))
                    plt.imshow(correlation_matrix, cmap='coolwarm', aspect='auto')
                    plt.colorbar()
                    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
                    plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
                    plt.title('Correlation Matrix')
                    plt.tight_layout()
                    plt.show()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not create correlation matrix: {str(e)}")
            else:
                QMessageBox.information(self, "Info", "Need at least 2 numeric columns for correlation matrix")

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "cleaned_data.csv", "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.df.to_csv(file_path, index=False)
                else:
                    self.df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", f"File saved successfully to {file_path}!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def plot_column(self):
        if self.df is not None:
            try:
                column, ok = QFileDialog.getText(self, "Column Name", "Enter column name to plot:")
                if ok and column in self.df.columns:
                    plt.figure(figsize=(10, 6))
                    self.df[column].value_counts().plot(kind='bar')
                    plt.title(f"Bar Chart of {column}")
                    plt.ylabel("Count")
                    plt.xlabel(column)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.show()
                elif ok:
                    QMessageBox.warning(self, "Column Error", f"Column '{column}' not found.")
            except Exception as e:
                QMessageBox.critical(self, "Plot Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataProcessorApp()
    window.show()
    sys.exit(app.exec_())
