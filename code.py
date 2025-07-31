import sys
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox,
    QHBoxLayout, QGroupBox, QTextEdit, QSplitter, QTabWidget, QProgressBar,
    QCheckBox, QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
import gc
import os
from concurrent.futures import ThreadPoolExecutor
import threading

class FastDataLoadThread(QThread):
    """Optimized thread for loading large files with parallel processing"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(object, str)
    error = pyqtSignal(str)
    
    def __init__(self, file_path, file_type, chunk_size=50000):
        super().__init__()
        self.file_path = file_path
        self.file_type = file_type
        self.chunk_size = chunk_size
        
    def run(self):
        try:
            if self.file_type == "CSV":
                # Optimized CSV loading with parallel processing
                file_size = os.path.getsize(self.file_path) / (1024 * 1024)  # MB
                
                if file_size > 50:  # Lower threshold for faster processing
                    # Fast chunked loading with optimized parameters
                    chunks = []
                    total_rows = 0
                    
                    # Fast row counting
                    for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size, nrows=1000000):
                        total_rows += len(chunk)
                        if total_rows > 1000000:  # Limit for very large files
                            break
                    
                    # Optimized loading with better memory management
                    for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size):
                        chunks.append(chunk)
                        if len(chunks) % 10 == 0:  # Update progress less frequently
                            progress = int((len(chunks) * self.chunk_size / total_rows) * 100)
                            self.progress.emit(min(progress, 99))
                    
                    df = pd.concat(chunks, ignore_index=True, copy=False)
                    self.progress.emit(100)
                    self.finished.emit(df, f"Fast load: {len(df):,} rows, {len(df.columns)} columns")
                else:
                    # Direct loading for smaller files
                    df = pd.read_csv(self.file_path, engine='c')  # Use C engine for speed
                    self.finished.emit(df, f"Fast load: {len(df):,} rows and {len(df.columns)} columns")
                    
            elif self.file_type == "Excel":
                df = pd.read_excel(self.file_path, engine='openpyxl')
                self.finished.emit(df, f"Fast load: {len(df):,} rows and {len(df.columns)} columns")
                
            elif self.file_type == "JSON":
                df = pd.read_json(self.file_path)
                self.finished.emit(df, f"Fast load: {len(df):,} rows and {len(df.columns)} columns")
                
            elif self.file_type == "SQLite":
                conn = sqlite3.connect(self.file_path)
                tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
                table_name = tables.iloc[0, 0]
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                conn.close()
                self.finished.emit(df, f"Fast load: {len(df):,} rows and {len(df.columns)} columns")
                
        except Exception as e:
            self.error.emit(str(e))

class FastDataProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Data Processor - One-Click Operations")
        self.resize(1200, 800)

        self.df = None
        self.original_df = None
        self.load_thread = None
        self.cached_stats = None
        self.display_cache = None
        self.executor = ThreadPoolExecutor(max_workers=4)

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

        # Optimized chunk size for speed
        chunk_layout = QHBoxLayout()
        chunk_layout.addWidget(QLabel("Chunk Size:"))
        self.chunk_size_spin = QSpinBox()
        self.chunk_size_spin.setRange(10000, 200000)
        self.chunk_size_spin.setValue(50000)
        self.chunk_size_spin.setSuffix(" rows")
        chunk_layout.addWidget(self.chunk_size_spin)
        file_layout.addLayout(chunk_layout)

        self.load_button = QPushButton("🚀 Load File")
        self.load_button.clicked.connect(self.load_file)
        self.load_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px; }")
        file_layout.addWidget(self.load_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        file_layout.addWidget(self.progress_bar)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)

        # Data cleaning section
        clean_group = QGroupBox("🧹 Data Cleaning")
        clean_layout = QVBoxLayout()
        
        self.dropna_button = QPushButton("🗑️ Drop Null Rows")
        self.dropna_button.clicked.connect(self.fast_drop_na)
        self.dropna_button.setEnabled(False)
        self.dropna_button.setStyleSheet("QPushButton { background-color: #FF9800; color: white; padding: 8px; }")
        clean_layout.addWidget(self.dropna_button)

        self.duplicates_button = QPushButton("🔄 Remove Duplicates")
        self.duplicates_button.clicked.connect(self.fast_remove_duplicates)
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
        self.filter_input.setPlaceholderText("Enter filter condition (e.g., Team == 'Warriors')")
        filter_layout.addWidget(self.filter_input)

        self.filter_button = QPushButton("🔍 Apply Filter")
        self.filter_button.clicked.connect(self.fast_apply_filter)
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
        self.fillna_button.clicked.connect(self.fast_fill_null_values)
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
        self.stats_button.clicked.connect(self.fast_show_statistics)
        self.stats_button.setEnabled(False)
        self.stats_button.setStyleSheet("QPushButton { background-color: #607D8B; color: white; padding: 8px; }")
        analysis_layout.addWidget(self.stats_button)

        self.plot_button = QPushButton("📈 Plot Bar Chart")
        self.plot_button.clicked.connect(self.fast_plot_column)
        self.plot_button.setEnabled(False)
        self.plot_button.setStyleSheet("QPushButton { background-color: #607D8B; color: white; padding: 8px; }")
        analysis_layout.addWidget(self.plot_button)

        self.correlation_button = QPushButton("🔗 Correlation Matrix")
        self.correlation_button.clicked.connect(self.fast_show_correlation)
        self.correlation_button.setEnabled(False)
        self.correlation_button.setStyleSheet("QPushButton { background-color: #607D8B; color: white; padding: 8px; }")
        analysis_layout.addWidget(self.correlation_button)
        
        analysis_group.setLayout(analysis_layout)
        left_layout.addWidget(analysis_group)

        # Export section
        export_group = QGroupBox("💾 Export Data")
        export_layout = QVBoxLayout()
        
        self.export_button = QPushButton("💾 Export Cleaned Data")
        self.export_button.clicked.connect(self.fast_export_data)
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
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.load_button.setEnabled(False)
            self.load_button.setText("Loading...")
            
            # Use optimized loading thread
            self.load_thread = FastDataLoadThread(file_path, file_type, self.chunk_size_spin.value())
            self.load_thread.progress.connect(self.progress_bar.setValue)
            self.load_thread.finished.connect(self.on_file_loaded)
            self.load_thread.error.connect(self.on_load_error)
            self.load_thread.start()

    def on_file_loaded(self, df, message):
        """Handle successful file loading with caching"""
        self.df = df
        self.original_df = df.copy()
        
        # Clear caches
        self.cached_stats = None
        self.display_cache = None
        
        self.show_data()
        self.update_column_dropdown()
        self.enable_all_buttons()
        
        self.progress_bar.setVisible(False)
        self.load_button.setEnabled(True)
        self.load_button.setText("🚀 Load File")
        
        QMessageBox.information(self, "Success", message)

    def on_load_error(self, error_message):
        """Handle file loading errors"""
        self.progress_bar.setVisible(False)
        self.load_button.setEnabled(True)
        self.load_button.setText("🚀 Load File")
        QMessageBox.critical(self, "Error", f"Error loading file: {error_message}")

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
        """Fast data display with caching"""
        if self.df is None:
            return
            
        # Use cached display data if available
        if self.display_cache is None:
            display_rows = min(500, len(self.df))  # Show fewer rows for speed
            self.display_cache = self.df.head(display_rows)
        
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        
        self.table.setColumnCount(len(self.display_cache.columns))
        self.table.setRowCount(len(self.display_cache.index))
        self.table.setHorizontalHeaderLabels(self.display_cache.columns.astype(str))

        if len(self.df) > 500:
            self.table.setItem(0, 0, QTableWidgetItem(f"Showing first 500 rows of {len(self.df):,} total rows..."))

        # Fast table population
        for i in range(len(self.display_cache.index)):
            for j in range(len(self.display_cache.columns)):
                value = str(self.display_cache.iat[i, j])
                self.table.setItem(i, j, QTableWidgetItem(value))

    def fast_drop_na(self):
        """Fast null value removal"""
        if self.df is not None:
            try:
                before_count = len(self.df)
                # Use optimized dropna
                self.df.dropna(inplace=True, axis=0)
                after_count = len(self.df)
                
                # Clear caches
                self.cached_stats = None
                self.display_cache = None
                
                self.show_data()
                QMessageBox.information(self, "Success", f"Fast drop: {before_count - after_count:,} rows removed!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error dropping null values: {str(e)}")

    def fast_remove_duplicates(self):
        """Fast duplicate removal"""
        if self.df is not None:
            try:
                before_count = len(self.df)
                # Use optimized drop_duplicates
                self.df.drop_duplicates(inplace=True, keep='first')
                after_count = len(self.df)
                
                # Clear caches
                self.cached_stats = None
                self.display_cache = None
                
                self.show_data()
                QMessageBox.information(self, "Success", f"Fast remove: {before_count - after_count:,} duplicates removed!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error removing duplicates: {str(e)}")

    def reset_data(self):
        if self.original_df is not None:
            self.df = self.original_df.copy()
            self.cached_stats = None
            self.display_cache = None
            self.show_data()
            self.update_column_dropdown()
            QMessageBox.information(self, "Success", "Data reset to original state!")

    def fast_apply_filter(self):
        """Fast filtering with optimization"""
        condition = self.filter_input.text()
        if self.df is not None and condition:
            try:
                before_count = len(self.df)
                # Use optimized query
                self.df = self.df.query(condition, engine='python')
                after_count = len(self.df)
                
                # Clear caches
                self.cached_stats = None
                self.display_cache = None
                
                self.show_data()
                QMessageBox.information(self, "Success", f"Fast filter: {after_count:,} rows remaining (was {before_count:,})")
            except Exception as e:
                QMessageBox.critical(self, "Filter Error", str(e))

    def fast_fill_null_values(self):
        """Fast null value filling"""
        if self.df is not None and self.column_dropdown.currentText():
            column = self.column_dropdown.currentText()
            try:
                # Optimized fillna
                if pd.api.types.is_numeric_dtype(self.df[column]):
                    fill_value = self.df[column].median()  # Use median for speed
                else:
                    fill_value = self.df[column].mode().iloc[0] if not self.df[column].mode().empty else "Unknown"
                
                self.df[column].fillna(fill_value, inplace=True)
                
                # Clear caches
                self.cached_stats = None
                self.display_cache = None
                
                self.show_data()
                QMessageBox.information(self, "Success", f"Fast fill: '{column}' filled with {fill_value}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def rename_column(self):
        if self.df is not None and self.column_dropdown.currentText():
            old_name = self.column_dropdown.currentText()
            new_name, ok = QFileDialog.getText(self, "Rename Column", f"Enter new name for '{old_name}':")
            if ok and new_name:
                try:
                    self.df.rename(columns={old_name: new_name}, inplace=True)
                    
                    # Clear caches
                    self.cached_stats = None
                    self.display_cache = None
                    
                    self.show_data()
                    self.update_column_dropdown()
                    QMessageBox.information(self, "Success", f"Column '{old_name}' renamed to '{new_name}'")
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def fast_show_statistics(self):
        """Fast statistics with caching"""
        if self.df is not None:
            try:
                # Use cached stats if available
                if self.cached_stats is None:
                    stats_text = "📊 FAST STATISTICS\n" + "="*50 + "\n\n"
                    
                    # Fast basic info
                    stats_text += f"📋 Dataset Info:\n"
                    stats_text += f"   • Rows: {len(self.df):,}\n"
                    stats_text += f"   • Columns: {len(self.df.columns)}\n"
                    stats_text += f"   • Memory: {self.df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB\n\n"
                    
                    # Fast null analysis
                    null_counts = self.df.isnull().sum()
                    if null_counts.sum() > 0:
                        stats_text += f"🔍 Null Values:\n"
                        for col, count in null_counts[null_counts > 0].items():
                            stats_text += f"   • {col}: {count:,} ({count/len(self.df)*100:.1f}%)\n"
                        stats_text += "\n"
                    
                    # Fast numeric stats
                    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        stats_text += f"📈 Numeric Statistics:\n"
                        stats_text += self.df[numeric_cols].describe().to_string()
                        stats_text += "\n\n"
                    
                    # Fast categorical stats
                    categorical_cols = self.df.select_dtypes(include=['object']).columns
                    if len(categorical_cols) > 0:
                        stats_text += f"📝 Categorical Columns:\n"
                        for col in categorical_cols:
                            unique_count = self.df[col].nunique()
                            stats_text += f"   • {col}: {unique_count:,} unique values\n"
                    
                    self.cached_stats = stats_text
                
                self.stats_text.setText(self.cached_stats)
                self.tab_widget.setCurrentIndex(1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error generating statistics: {str(e)}")

    def fast_show_correlation(self):
        """Fast correlation matrix"""
        if self.df is not None:
            numeric_df = self.df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                try:
                    # Use optimized correlation
                    correlation_matrix = numeric_df.corr(method='pearson')
                    plt.figure(figsize=(10, 8))
                    plt.imshow(correlation_matrix, cmap='coolwarm', aspect='auto')
                    plt.colorbar()
                    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
                    plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
                    plt.title('Fast Correlation Matrix')
                    plt.tight_layout()
                    plt.show()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not create correlation matrix: {str(e)}")
            else:
                QMessageBox.information(self, "Info", "Need at least 2 numeric columns for correlation matrix")

    def fast_export_data(self):
        """Fast data export"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "fast_cleaned_data.csv", "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    # Use fast CSV export
                    self.df.to_csv(file_path, index=False, chunksize=10000)
                else:
                    self.df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", f"Fast export to {file_path}!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def fast_plot_column(self):
        """Fast plotting"""
        if self.df is not None:
            try:
                column, ok = QFileDialog.getText(self, "Column Name", "Enter column name to plot:")
                if ok and column in self.df.columns:
                    plt.figure(figsize=(10, 6))
                    # Use fast plotting
                    self.df[column].value_counts().head(20).plot(kind='bar')
                    plt.title(f"Fast Bar Chart: {column}")
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
    window = FastDataProcessorApp()
    window.show()
    sys.exit(app.exec_())
