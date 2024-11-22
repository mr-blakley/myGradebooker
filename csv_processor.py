import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

class CSVProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Processor")
        self.root.geometry("800x600")  # Increased from 600x400
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights to make the window resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        
        # Create and configure widgets
        self.setup_widgets()
        
        # Selected file path
        self.selected_file = None
        
    def setup_widgets(self):
        # File selection button
        self.select_btn = ttk.Button(
            self.main_frame, 
            text="Select CSV File",
            command=self.select_file
        )
        self.select_btn.grid(row=0, column=0, pady=10)
        
        # Display selected file
        self.file_label = ttk.Label(self.main_frame, text="No file selected")
        self.file_label.grid(row=1, column=0, pady=5)
        
        # Process button
        self.process_btn = ttk.Button(
            self.main_frame,
            text="Process CSV",
            command=self.process_csv,
            state="disabled"
        )
        self.process_btn.grid(row=2, column=0, pady=10)
        
        # Results text area with scrollbar
        text_frame = ttk.Frame(self.main_frame)
        text_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure text widget with larger size
        self.results_text = tk.Text(
            text_frame,
            height=25,  # Increased height
            width=80,   # Increased width
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD  # Enable word wrapping
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure scrollbar
        scrollbar.config(command=self.results_text.yview)
        
    def select_file(self):
        filetypes = (
            ('CSV files', '*.csv'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Select a CSV file',
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(text=os.path.basename(filename))
            self.process_btn.config(state="normal")
            
    def process_csv(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a CSV file first")
            return
            
        try:
            # Read the CSV file
            df = pd.read_csv(self.selected_file)
            
            # Print all column names for debugging
            print("All columns in CSV:", df.columns.tolist())
            
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            
            # Get lab and assessment columns (case-insensitive)
            lab_columns = [col for col in df.columns if 'lab' in col.lower()]
            assessment_columns = [col for col in df.columns if 'assessment' in col.lower()]
            
            # Print detected columns
            print("Detected Lab columns:", lab_columns)
            print("Detected Assessment columns:", assessment_columns)
            
            # Convert percentage strings to numeric values
            def convert_percentage(val):
                if pd.isna(val) or str(val).strip() == '':
                    return float('nan')
                try:
                    # Remove '%' sign and convert to float
                    return float(str(val).strip().rstrip('%'))
                except:
                    return float('nan')
            
            # Convert columns to numeric, handling percentage values
            for col in lab_columns + assessment_columns:
                df[col] = df[col].apply(convert_percentage)
            
            # Calculate student averages
            results = "Individual Student Statistics:\n"
            results += "=" * 100 + "\n\n"
            
            # Add column information at the top
            results += "Detected Columns:\n"
            results += f"Lab Columns: {', '.join(lab_columns)}\n"
            results += f"Assessment Columns: {', '.join(assessment_columns)}\n\n"
            
            # Calculate individual student averages
            student_stats = []
            for idx, row in df.iterrows():
                # Get student name from the first column
                student_name = str(row[df.columns[0]]).strip()
                
                # Calculate averages only if valid columns exist and have non-NaN values
                lab_values = row[lab_columns].dropna()
                assessment_values = row[assessment_columns].dropna()
                
                # Calculate averages and completion counts
                lab_avg = lab_values.mean() if not lab_values.empty else float('nan')
                assessment_avg = assessment_values.mean() if not assessment_values.empty else float('nan')
                
                # Count completed assignments
                labs_completed = len(lab_values)
                total_labs = len(lab_columns)
                assessments_completed = len(assessment_values)
                total_assessments = len(assessment_columns)
                
                student_stats.append({
                    'name': student_name,
                    'lab_avg': lab_avg,
                    'lab_completion': (labs_completed, total_labs),
                    'assessment_avg': assessment_avg,
                    'assessment_completion': (assessments_completed, total_assessments)
                })
            
            # Sort students by name
            student_stats.sort(key=lambda x: x['name'])
            
            # Display individual student statistics with completion ratios
            header = f"{'Student Name':<30} {'Lab Average':>15} {'Lab Completion':>15} {'Assessment Average':>20} {'Assessment Completion':>20}\n"
            results += header
            results += "-" * 100 + "\n"
            
            for stat in student_stats:
                lab_str = f"{stat['lab_avg']:.1f}%" if not pd.isna(stat['lab_avg']) else "N/A"
                assessment_str = f"{stat['assessment_avg']:.1f}%" if not pd.isna(stat['assessment_avg']) else "N/A"
                lab_completion = f"{stat['lab_completion'][0]}/{stat['lab_completion'][1]}"
                assessment_completion = f"{stat['assessment_completion'][0]}/{stat['assessment_completion'][1]}"
                
                row = f"{stat['name']:<30} {lab_str:>15} {lab_completion:>15} {assessment_str:>20} {assessment_completion:>20}\n"
                results += row
            
            # Add class summary
            results += "\nClass Summary:\n"
            results += "=" * 100 + "\n"
            
            if lab_columns:
                class_lab_avg = df[lab_columns].mean().mean()
                results += f"Class Lab Average: {class_lab_avg:.1f}%\n"
                
                # Calculate overall lab completion rate
                total_possible_labs = len(df) * len(lab_columns)
                total_completed_labs = df[lab_columns].count().sum()
                completion_rate = (total_completed_labs / total_possible_labs) * 100
                results += f"Class Lab Completion Rate: {completion_rate:.1f}% ({total_completed_labs}/{total_possible_labs} total submissions)\n"
                
                # Show individual lab averages and completion
                results += "\nIndividual Lab Statistics:\n"
                for col in lab_columns:
                    avg = df[col].mean()
                    valid_count = df[col].count()
                    total_count = len(df[col])
                    completion_percent = (valid_count / total_count) * 100
                    results += f"- {col}:\n"
                    results += f"  Average: {avg:.1f}%\n"
                    results += f"  Completion: {valid_count}/{total_count} students ({completion_percent:.1f}%)\n"
            
            if assessment_columns:
                class_assessment_avg = df[assessment_columns].mean().mean()
                results += f"\nClass Assessment Average: {class_assessment_avg:.1f}%\n"
                
                # Calculate overall assessment completion rate
                total_possible_assessments = len(df) * len(assessment_columns)
                total_completed_assessments = df[assessment_columns].count().sum()
                completion_rate = (total_completed_assessments / total_possible_assessments) * 100
                results += f"Class Assessment Completion Rate: {completion_rate:.1f}% ({total_completed_assessments}/{total_possible_assessments} total submissions)\n"
                
                # Show individual assessment averages and completion
                results += "\nIndividual Assessment Statistics:\n"
                for col in assessment_columns:
                    avg = df[col].mean()
                    valid_count = df[col].count()
                    total_count = len(df[col])
                    completion_percent = (valid_count / total_count) * 100
                    results += f"- {col}:\n"
                    results += f"  Average: {avg:.1f}%\n"
                    results += f"  Completion: {valid_count}/{total_count} students ({completion_percent:.1f}%)\n"
            
            self.results_text.insert(tk.END, results)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing CSV: {str(e)}")

def main():
    root = tk.Tk()
    app = CSVProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
