# Gradebooker

A Python-based GUI application for processing and analyzing student grades from CSV files.

## Features

- Load and process CSV files containing student grades
- Calculate individual student statistics:
  - Lab averages and completion rates
  - Assessment averages and completion rates
- Display class-wide statistics:
  - Overall class averages
  - Completion rates for all assignments
  - Individual assignment statistics
- Clean, user-friendly interface built with Tkinter

## Requirements

- Python 3.x
- pandas
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alexb0x13/myGradebooker.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python csv_processor.py
```

2. Click "Select CSV File" to choose your gradebook CSV file
3. Click "Process CSV" to analyze the grades

## CSV File Format

The CSV file should have the following structure:
- First column: Student names
- Subsequent columns: Assignment grades (as percentages)
- Column names should start with either "Lab" or "Assessment"

## Author

Alex B
